from crewai.tools import BaseTool
from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
import pandas as pd
import json
import csv
import math
import os


class ReadCSVToolInput(BaseModel):
    """Input schema for ReadCSVTool."""
    file_path: str = Field(..., description="Path to the CSV file to read")


class ReadCSVTool(BaseTool):
    name: str = "read_csv_tool"
    description: str = (
        "Read a CSV file and return its contents as a list of dictionaries. "
        "Useful for reading supplier catalogs, orders, and other data files."
    )
    args_schema: Type[BaseModel] = ReadCSVToolInput

    def _run(self, file_path: str) -> str:
        try:
            df = pd.read_csv(file_path)
            return json.dumps(df.to_dict('records'), indent=2)
        except Exception as e:
            return f"Error reading CSV file: {str(e)}"


class WriteJSONToolInput(BaseModel):
    """Input schema for WriteJSONTool."""
    file_path: str = Field(..., description="Path where to save the JSON file")
    data: str = Field(..., description="JSON data to write to file")


class WriteJSONTool(BaseTool):
    name: str = "write_json_tool"
    description: str = (
        "Write JSON data to a file. The data should be a valid JSON string."
    )
    args_schema: Type[BaseModel] = WriteJSONToolInput

    def _run(self, file_path: str, data: str) -> str:
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Parse JSON to validate it
            json_data = json.loads(data)
            
            # Write to file
            with open(file_path, 'w') as f:
                json.dump(json_data, f, indent=2)
            
            return f"Successfully wrote JSON data to {file_path}"
        except Exception as e:
            return f"Error writing JSON file: {str(e)}"


class WriteCSVToolInput(BaseModel):
    """Input schema for WriteCSVTool."""
    file_path: str = Field(..., description="Path where to save the CSV file")
    data: str = Field(..., description="JSON data to convert and write as CSV")


class WriteCSVTool(BaseTool):
    name: str = "write_csv_tool"
    description: str = (
        "Write JSON data to a CSV file. The data should be a JSON string representing a list of dictionaries."
    )
    args_schema: Type[BaseModel] = WriteCSVToolInput

    def _run(self, file_path: str, data: str) -> str:
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Parse JSON data
            json_data = json.loads(data)
            
            if not isinstance(json_data, list):
                return "Error: Data must be a list of dictionaries"
            
            if not json_data:
                return "Error: Data list is empty"
            
            # Write to CSV
            df = pd.DataFrame(json_data)
            df.to_csv(file_path, index=False)
            
            return f"Successfully wrote CSV data to {file_path}"
        except Exception as e:
            return f"Error writing CSV file: {str(e)}"


class CalculatePricingToolInput(BaseModel):
    """Input schema for CalculatePricingTool."""
    cost_price: float = Field(..., description="Cost price of the product")
    shipping_cost: float = Field(..., description="Shipping cost for the product")
    country: str = Field(default="Australia", description="Customer country for tax calculation")


class CalculatePricingTool(BaseTool):
    name: str = "calculate_pricing_tool"
    description: str = (
        "Calculate the selling price using the pricing formula: "
        "Platform fee = 2.9% * P + $0.30, GST = 10% * P (AU only), "
        "Margin ≥ 25%, rounded up to nearest $0.50"
    )
    args_schema: Type[BaseModel] = CalculatePricingToolInput

    def _run(self, cost_price: float, shipping_cost: float, country: str = "Australia") -> str:
        try:
            # Calculate minimum price where margin >= 25%
            # Formula: P * (1 - 0.029 - (0.1 if AU else 0)) - 0.30 >= 1.25 * (cost_price + shipping_cost)
            
            platform_fee_rate = 0.029
            platform_fee_fixed = 0.30
            gst_rate = 0.10 if country.lower() == "australia" else 0.0
            min_margin = 1.25  # 25% margin means selling price should be 125% of cost
            
            landed_cost = cost_price + shipping_cost
            target_revenue = min_margin * landed_cost
            
            # P * (1 - platform_fee_rate - gst_rate) - platform_fee_fixed >= target_revenue
            # P >= (target_revenue + platform_fee_fixed) / (1 - platform_fee_rate - gst_rate)
            
            min_price = (target_revenue + platform_fee_fixed) / (1 - platform_fee_rate - gst_rate)
            
            # Round up to nearest $0.50
            rounded_price = math.ceil(min_price * 2) / 2
            
            # Calculate actual margin
            net_revenue = rounded_price * (1 - platform_fee_rate - gst_rate) - platform_fee_fixed
            actual_margin = (net_revenue / landed_cost - 1) * 100
            
            result = {
                "selling_price": rounded_price,
                "cost_price": cost_price,
                "shipping_cost": shipping_cost,
                "landed_cost": landed_cost,
                "platform_fee": rounded_price * platform_fee_rate + platform_fee_fixed,
                "gst": rounded_price * gst_rate if gst_rate > 0 else 0,
                "net_revenue": net_revenue,
                "margin_percentage": round(actual_margin, 2),
                "country": country
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error calculating pricing: {str(e)}"


class FilterProductsToolInput(BaseModel):
    """Input schema for FilterProductsTool."""
    products_json: str = Field(..., description="JSON string containing list of products")
    min_stock: int = Field(default=10, description="Minimum stock level required")
    min_margin: float = Field(default=25.0, description="Minimum margin percentage required")


class FilterProductsTool(BaseTool):
    name: str = "filter_products_tool"
    description: str = (
        "Filter products based on stock level and achievable margin criteria. "
        "Returns products that meet both minimum stock and margin requirements."
    )
    args_schema: Type[BaseModel] = FilterProductsToolInput

    def _run(self, products_json: str, min_stock: int = 10, min_margin: float = 25.0) -> str:
        try:
            products = json.loads(products_json)
            filtered_products = []
            
            for product in products:
                # Check stock requirement
                if product.get('stock', 0) < min_stock:
                    continue
                
                # Calculate if margin is achievable
                cost_price = float(product.get('cost_price', 0))
                shipping_cost = float(product.get('shipping_cost', 0))
                
                # Use pricing calculation
                pricing_tool = CalculatePricingTool()
                pricing_result = pricing_tool._run(cost_price, shipping_cost, "Australia")
                pricing_data = json.loads(pricing_result)
                
                if pricing_data.get('margin_percentage', 0) >= min_margin:
                    # Add calculated pricing to product
                    product['calculated_price'] = pricing_data['selling_price']
                    product['calculated_margin'] = pricing_data['margin_percentage']
                    filtered_products.append(product)
            
            return json.dumps(filtered_products, indent=2)
        except Exception as e:
            return f"Error filtering products: {str(e)}"
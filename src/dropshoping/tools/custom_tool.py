from crewai_tools import BaseTool
import pandas as pd
import json
import math
from typing import Type
from pydantic import BaseModel, Field
import os

#This tool will be useful while user is defing own oparations in the process and files(Human in the loop)
class DataLoaderTool(BaseTool):
    name: str = "Data Loader"
    description: str = "Load CSV data files for processing"
    
    def _run(self, file_path: str) -> str:
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                return df.to_json(orient='records', indent=2)
            else:
                with open(file_path, 'r') as f:
                    return f.read()
        except Exception as e:
            return f"Error loading file {file_path}: {str(e)}"

class ProductSourcingTool(BaseTool):
    name: str = "Product Sourcing Tool"
    description: str = "Analyze supplier catalog and select profitable products with adequate stock"
    
    def _run(self, catalog_path: str) -> str:
        try:
            df = pd.read_csv(catalog_path)
            
            # Filter products with stock >= 10
            adequate_stock = df[df['stock'] >= 10].copy()
            
            # Calculate if 25% margin is achievable
            selected_products = []
            
            for _, row in adequate_stock.iterrows():
                cost_price = float(row['cost_price'])
                shipping_cost = float(row['shipping_cost'])
                
                # Calculate minimum price for 25% margin
                # Platform fee = 2.9% * P + $0.30
                # GST = 10% * P (AU only, assume all AU for simplicity)
                # Landed cost = cost_price + shipping + fee + GST
                # Margin >= 25%
                
                # P = (cost_price + shipping + 0.30) / (1 - 0.029 - 0.10 - 0.25)
                min_price = (cost_price + shipping_cost + 0.30) / 0.621
                
                # Round up to nearest $0.50
                final_price = math.ceil(min_price * 2) / 2
                
                # Calculate actual margin to verify >= 25%
                platform_fee = 0.029 * final_price + 0.30
                gst = 0.10 * final_price
                total_costs = cost_price + shipping_cost + platform_fee + gst
                margin = (final_price - total_costs) / final_price
                
                if margin >= 0.25:
                    selected_products.append({
                        'supplier_sku': row['supplier_sku'],
                        'name': row['name'],
                        'category': row['category'],
                        'cost_price': cost_price,
                        'stock': int(row['stock']),
                        'calculated_price': final_price,
                        'margin': round(margin * 100, 2)
                    })
            
            # Select top 10 products (by margin)
            selected_products = sorted(selected_products, key=lambda x: x['margin'], reverse=True)[:10]
            
            return json.dumps({
                'selected_products': selected_products,
                'total_analyzed': len(adequate_stock),
                'total_selected': len(selected_products)
            }, indent=2)
            
        except Exception as e:
            return f"Error in product sourcing: {str(e)}"

class PricingTool(BaseTool):
    name: str = "Pricing Tool"
    description: str = "Generate price updates for selected products using data from selection.json"
    
    def _run(self, selection_file: str) -> str:
        try:
            # Load selected products from selection.json
            with open(selection_file, 'r') as f:
                selected_products = json.load(f)
            
            # Create price update data
            price_updates = []
            
            for product in selected_products:
                price_updates.append({
                    'supplier_sku': product['supplier_sku'],
                    'name': product['name'],
                    'current_price': product['calculated_price'],
                    'updated_price': product['calculated_price']  # Using the already calculated price
                })
            
            # Save to price_update.csv in the same directory as selection.json
            output_dir = os.path.dirname(selection_file)
            price_update_file = os.path.join(output_dir, 'price_update.csv')
            
            price_df = pd.DataFrame(price_updates)
            price_df.to_csv(price_update_file, index=False)
            
            return json.dumps({
                'price_updates': price_updates,
                'total_products_updated': len(price_updates)
            }, indent=2)
            
        except Exception as e:
            return f"Error in pricing update: {str(e)}"

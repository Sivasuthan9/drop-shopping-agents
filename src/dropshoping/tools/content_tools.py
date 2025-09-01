from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json


class GenerateListingContentToolInput(BaseModel):
    """Input schema for GenerateListingContentTool."""
    product_data: str = Field(..., description="JSON string containing product information")


class GenerateListingContentTool(BaseTool):
    name: str = "generate_listing_content_tool"
    description: str = (
        "Generate optimized product listing content including title, bullet points, "
        "description, tags, and SEO elements based on product data."
    )
    args_schema: Type[BaseModel] = GenerateListingContentToolInput

    def _run(self, product_data: str) -> str:
        try:
            product = json.loads(product_data)
            
            # Extract product info
            name = product.get('name', 'Product')
            category = product.get('category', 'General')
            description = product.get('description', '')
            brand = product.get('brand', 'Brand')
            
            # Generate optimized content
            title = f"{name} - Premium {category}"
            if len(title) > 80:
                title = name[:77] + "..."
            
            bullet_points = [
                f"High-quality {category.lower()} from trusted {brand} brand",
                f"Durable construction with premium materials",
                f"Perfect for daily use and long-lasting performance",
                f"Easy to use design with user-friendly features",
                f"Excellent value for money with reliable quality"
            ]
            
            # Generate description based on original
            enhanced_description = f"Discover the premium quality of {name}. {description} This exceptional {category.lower()} combines innovative design with superior functionality to deliver outstanding performance. Whether for personal use or professional applications, this product meets the highest standards of quality and reliability."
            
            # Generate tags
            tags = [
                category.lower().replace(' & ', ' ').replace(' ', '_'),
                brand.lower(),
                'premium',
                'quality',
                'durable',
                'reliable'
            ]
            
            # SEO optimization
            seo_title = f"{name} - Premium {category} | {brand}"
            if len(seo_title) > 60:
                seo_title = f"{name} | {brand}"[:60]
            
            meta_description = f"Shop {name} from {brand}. Premium {category.lower()} with superior quality and performance. Free shipping available."
            if len(meta_description) > 160:
                meta_description = meta_description[:157] + "..."
            
            result = {
                "supplier_sku": product.get('supplier_sku'),
                "title": title,
                "bullet_points": bullet_points,
                "description": enhanced_description,
                "tags": tags,
                "seo_title": seo_title,
                "meta_description": meta_description
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error generating listing content: {str(e)}"


class GenerateQAReviewToolInput(BaseModel):
    """Input schema for GenerateQAReviewTool."""
    listing_data: str = Field(..., description="JSON string containing product listing data")


class GenerateQAReviewTool(BaseTool):
    name: str = "generate_qa_review_tool"
    description: str = (
        "Review product listings for potential issues, exaggerated claims, "
        "and compliance problems."
    )
    args_schema: Type[BaseModel] = GenerateQAReviewToolInput

    def _run(self, listing_data: str) -> str:
        try:
            listing = json.loads(listing_data)
            
            issues_found = []
            severity = "low"
            recommendations = []
            
            title = listing.get('title', '')
            description = listing.get('description', '')
            bullet_points = listing.get('bullet_points', [])
            
            # Check for exaggerated claims
            exaggerated_words = ['amazing', 'incredible', 'revolutionary', 'life-changing', 'miraculous', 'unbelievable']
            all_text = f"{title} {description} {' '.join(bullet_points)}".lower()
            
            for word in exaggerated_words:
                if word in all_text:
                    issues_found.append(f"Potentially exaggerated claim using word '{word}'")
                    severity = "medium"
                    recommendations.append(f"Consider replacing '{word}' with more factual language")
            
            # Check for vague claims
            vague_phrases = ['premium quality', 'superior performance', 'exceptional', 'outstanding']
            for phrase in vague_phrases:
                if phrase.lower() in all_text:
                    recommendations.append(f"Provide specific details instead of vague claim '{phrase}'")
            
            # Check for missing specifics
            if 'premium' in all_text and 'materials' in all_text:
                recommendations.append("Specify what materials make this product premium")
            
            if not issues_found:
                issues_found.append("No major compliance issues found")
                severity = "low"
                recommendations.append("Content appears compliant with standard e-commerce guidelines")
            
            result = {
                "supplier_sku": listing.get('supplier_sku'),
                "issues_found": issues_found,
                "severity": severity,
                "recommendations": recommendations,
                "revised_content_suggestions": "Consider being more specific about product features and benefits"
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error generating QA review: {str(e)}"
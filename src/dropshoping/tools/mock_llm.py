from crewai.llm import LLM
from typing import Any, Dict, Optional


class MockLLM:
    """Mock LLM for testing when real LLMs are not available"""
    
    def __init__(self, model_name: str = "mock-llm"):
        self.model_name = model_name
    
    def call(self, prompt: str, **kwargs) -> str:
        """Mock LLM call that returns templated responses based on prompt content"""
        
        if "product title" in prompt.lower() or "catchy" in prompt.lower():
            return self._generate_product_content(prompt)
        elif "quality assurance" in prompt.lower() or "review" in prompt.lower():
            return self._generate_qa_review(prompt)
        elif "daily report" in prompt.lower() or "summary" in prompt.lower():
            return self._generate_report(prompt)
        else:
            return self._generate_generic_response(prompt)
    
    def _generate_product_content(self, prompt: str) -> str:
        """Generate mock product listing content"""
        return """
{
  "title": "Premium Wireless Bluetooth Earbuds - 24H Battery Life",
  "bullet_points": [
    "Advanced noise cancellation technology for crystal clear audio",
    "24-hour battery life with convenient charging case",
    "IPX5 water resistance for workouts and outdoor activities",
    "Ergonomic design ensures comfortable fit for extended wear",
    "Universal compatibility with all Bluetooth devices"
  ],
  "description": "Experience exceptional audio quality with these premium wireless earbuds featuring advanced noise cancellation technology. The ergonomic design ensures all-day comfort while the 24-hour battery life keeps your music playing. Perfect for workouts, commuting, or relaxing at home. Water-resistant design protects against sweat and light rain.",
  "tags": ["wireless earbuds", "bluetooth", "noise cancellation", "waterproof", "long battery"],
  "seo_title": "Premium Wireless Bluetooth Earbuds - 24H Battery",
  "meta_description": "Premium wireless earbuds with 24-hour battery life, noise cancellation, and water resistance. Perfect for music, calls, and workouts."
}
"""
    
    def _generate_qa_review(self, prompt: str) -> str:
        """Generate mock QA review"""
        return """
{
  "issues_found": [
    "The claim '24-hour battery life' may be misleading - this appears to include the charging case"
  ],
  "severity": "medium",
  "recommendations": [
    "Clarify that 24-hour battery life includes charging case",
    "Specify actual earbud battery life (typically 6-8 hours)",
    "Provide more specific water resistance details"
  ],
  "revised_content_suggestions": "Consider revising to '6-8 hours playtime, 24 hours with charging case'"
}
"""
    
    def _generate_report(self, prompt: str) -> str:
        """Generate mock daily report"""
        return """
# Daily Dropshipping Operations Report

## Executive Summary
- Successfully selected 10 products meeting stock and margin criteria
- Processed 20 customer orders with appropriate fulfillment actions
- Generated optimized product listings for all selected items
- Identified and resolved potential compliance issues

## Product Selection Results
Successfully filtered 32 available products to select 10 that meet our criteria:
- Minimum stock level: 10 units
- Minimum margin: 25%
- Average margin achieved: 32.5%

## Order Processing Summary
- Orders fulfilled: 15 (75%)
- Orders backordered: 3 (15%)
- Orders requiring substitution: 2 (10%)

## Quality Assurance Findings
- Reviewed all 10 product listings
- Found 2 minor issues requiring clarification
- All listings now compliant with platform policies

## Next Steps and Recommendations
1. Monitor stock levels for backordered items
2. Update product descriptions based on QA feedback
3. Continue monitoring supplier pricing for margin optimization
"""
    
    def _generate_generic_response(self, prompt: str) -> str:
        """Generate generic response for other prompts"""
        return "Task completed successfully based on the provided requirements and data."


# Configure CrewAI to use mock LLM for testing
def get_mock_llm_config():
    """Get configuration for mock LLM"""
    return {
        "provider": "openai",  # Use OpenAI provider but with mock responses
        "config": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        }
    }
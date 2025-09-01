#!/usr/bin/env python
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to Python path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from dropshoping.crew import Dropshoping


def main():
    parser = argparse.ArgumentParser(description='Shopify Dropshipping Operations Agent')
    parser.add_argument('--catalog', required=True, help='Path to supplier catalog CSV file')
    parser.add_argument('--orders', required=True, help='Path to orders CSV file')
    parser.add_argument('--out', required=True, help='Output directory for results')
    
    args = parser.parse_args()
    
    # Validate input files exist
    if not os.path.exists(args.catalog):
        print(f"Error: Catalog file not found: {args.catalog}")
        sys.exit(1)
    
    if not os.path.exists(args.orders):
        print(f"Error: Orders file not found: {args.orders}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.out, exist_ok=True)
    
    # Convert to absolute paths
    catalog_file = os.path.abspath(args.catalog)
    orders_file = os.path.abspath(args.orders)
    output_dir = os.path.abspath(args.out)
    
    print(f"Starting Shopify Dropshipping Operations...")
    print(f"Catalog: {catalog_file}")
    print(f"Orders: {orders_file}")
    print(f"Output: {output_dir}")
    print("-" * 50)
    
    # Prepare inputs for the crew
    inputs = {
        'catalog_file': catalog_file,
        'orders_file': orders_file,
        'output_dir': output_dir,
        'current_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        # Initialize and run the crew
        crew = Dropshoping()
        result = crew.crew().kickoff(inputs=inputs)
        
        print("\n" + "=" * 50)
        print("Dropshipping Operations Completed Successfully!")
        print("=" * 50)
        print(f"\nCheck the following files in {output_dir}:")
        print("- selection.json")
        print("- listings.json") 
        print("- price_update.csv")
        print("- stock_update.csv")
        print("- order_actions.json")
        print("- listing_redlines.json")
        print("- daily_report.md")
        
        return result
        
    except Exception as e:
        print(f"\nError running dropshipping operations: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
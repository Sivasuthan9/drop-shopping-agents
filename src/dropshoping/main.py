#!/usr/bin/env python
import sys
import warnings
import os
from pathlib import Path
from datetime import datetime

from dropshoping.crew import Dropshoping

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew with default test data.
    """
    # Default paths for testing
    current_dir = Path(__file__).parent
    catalog_file = current_dir / "data" / "supplier_catalog.csv"
    orders_file = current_dir / "data" / "orders.csv"
    output_dir = current_dir / "out"
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    inputs = {
        'catalog_file': str(catalog_file.absolute()),
        'orders_file': str(orders_file.absolute()),
        'output_dir': str(output_dir.absolute()),
        'current_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        Dropshoping().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    # Default test inputs
    current_dir = Path(__file__).parent
    catalog_file = current_dir / "data" / "supplier_catalog.csv"
    orders_file = current_dir / "data" / "orders.csv"
    output_dir = current_dir / "out"
    
    inputs = {
        'catalog_file': str(catalog_file.absolute()),
        'orders_file': str(orders_file.absolute()),
        'output_dir': str(output_dir.absolute()),
        'current_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        Dropshoping().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Dropshoping().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    # Default test inputs
    current_dir = Path(__file__).parent
    catalog_file = current_dir / "data" / "supplier_catalog.csv"
    orders_file = current_dir / "data" / "orders.csv"
    output_dir = current_dir / "out"
    
    inputs = {
        'catalog_file': str(catalog_file.absolute()),
        'orders_file': str(orders_file.absolute()),
        'output_dir': str(output_dir.absolute()),
        'current_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        Dropshoping().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

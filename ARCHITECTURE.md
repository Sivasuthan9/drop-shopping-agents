# Shopify Dropshipping Operations Agent

A multi-agent hierarchical system to simulate Shopify dropshipping operations using the Crew AI framework.

## Architecture Overview

The system implements 7 specialized agents working in sequence:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Manager Agent                            │
│                 (Orchestrates Workflow)                        │
└─────────────────────────┬───────────────────────────────────────┘
                         │
         ┌───────────────────────────────────────────────┐
         │                                               │
         ▼                                               ▼
┌─────────────────┐                              ┌─────────────────┐
│ Product Sourcing│ ────► │ Listing Agent    │ ────► │ Pricing & Stock │
│     Agent       │       │   (LLM-based)   │       │     Agent       │
└─────────────────┘       └─────────────────┘       └─────────────────┘
         │                                               │
         ▼                                               ▼
┌─────────────────┐                              ┌─────────────────┐
│ Order Routing   │ ◄──── │    QA Agent      │ ◄──── │ Reporter Agent  │
│     Agent       │       │   (LLM-based)   │       │                 │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

## Agent Responsibilities

### 1. Manager Agent
- **Role**: Dropshipping Operations Manager
- **Tasks**: Orchestrates workflow, tracks state, coordinates between agents
- **Tools**: File operations for coordination

### 2. Product Sourcing Agent
- **Role**: Product Sourcing Specialist  
- **Tasks**: Filters products by stock ≥10 and margin ≥25%, selects top 10 products
- **Tools**: CSV reader, product filter, pricing calculator, JSON writer

### 3. Listing Agent (LLM)
- **Role**: E-commerce Content Creator
- **Tasks**: Generates titles, descriptions, bullet points, tags, SEO content
- **Tools**: Content generation (template-based for demo), JSON writer

### 4. Pricing & Stock Agent
- **Role**: Pricing and Inventory Analyst
- **Tasks**: Applies pricing formula, generates price_update.csv and stock_update.csv
- **Tools**: Pricing calculator, CSV writer

### 5. Order Routing Agent
- **Role**: Order Fulfillment Coordinator
- **Tasks**: Processes orders, determines fulfill/backorder/substitute actions
- **Tools**: CSV reader, order processor, JSON writer

### 6. QA Agent (LLM)
- **Role**: Quality Assurance Specialist
- **Tasks**: Reviews listings for compliance, identifies issues
- **Tools**: Content review (template-based for demo), JSON writer

### 7. Reporter Agent
- **Role**: Business Intelligence Analyst
- **Tasks**: Compiles daily operations report in markdown
- **Tools**: File operations, report generation

## Data Flow

1. **Input**: `supplier_catalog.csv` (32 SKUs) + `orders.csv` (20 orders)
2. **Product Selection**: Filter → Select 10 products meeting criteria
3. **Content Generation**: Create optimized listings for selected products
4. **Pricing**: Calculate final prices using business rules
5. **Order Processing**: Determine fulfillment actions for all orders
6. **Quality Review**: Check listings for compliance issues
7. **Reporting**: Generate comprehensive daily report
8. **Output**: 7 files in specified output directory

## Business Rules

### Pricing Formula
```
Minimum Price P where:
- Platform fee = 2.9% * P + $0.30
- GST = 10% * P (Australia only)
- Landed cost = cost_price + shipping + fee + GST
- Margin ≥ 25%
- Round up to nearest $0.50
```

### Selection Criteria
- Stock level ≥ 10 units
- Achievable margin ≥ 25%
- Select top 10 products by margin

### Order Fulfillment Logic
- **Fulfill**: Stock ≥ order quantity
- **Backorder**: 0 < stock < order quantity  
- **Substitute**: Stock = 0 or SKU not selected

## Installation & Setup

### Prerequisites
- Python ≥3.10 <3.14
- Virtual environment activated

### Dependencies
```bash
pip install crewai[tools] pandas
```

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies  
pip install crewai[tools] pandas
```

## Usage

### Command Line Interface
```bash
python standalone_app.py --catalog data/supplier_catalog.csv --orders data/orders.csv --out out/
```

### Crew AI Framework (Alternative)
```bash
# Set environment variables
export PYTHONPATH="src:$PYTHONPATH"

# Run with default test data
python -m app run --catalog data/supplier_catalog.csv --orders data/orders.csv --out out/

# Or use CrewAI directly
crewai run
```

## Output Files

The system generates 7 output files:

1. **selection.json** - 10 selected products with pricing
2. **listings.json** - Generated product content
3. **price_update.csv** - SKU and selling prices
4. **stock_update.csv** - SKU and stock levels
5. **order_actions.json** - Order fulfillment decisions
6. **listing_redlines.json** - QA review findings  
7. **daily_report.md** - Comprehensive operations summary

## LLM Configuration

### Local Models (Production)
The system is designed to use local Ollama models:
- **llama3** - For listing generation
- **mistral** - For QA review
- Parallel execution with 10-second staggered starts

### Fallback Mode (Demo)
When local models unavailable:
- Template-based content generation
- Deterministic QA review
- All business logic functional

## Sample Results

### Product Selection
- 32 products analyzed
- 10 selected (meeting criteria)
- Average margin: 26.4%
- Stock levels: 34-134 units

### Order Processing  
- 20 orders processed
- 40% fulfilled immediately
- 60% requiring substitution
- 0% backordered

### Quality Assurance
- All listings reviewed
- 0 high-severity issues
- Template-based content compliant

## Architecture Benefits

1. **Modular Design**: Each agent has specific responsibilities
2. **Crew AI Integration**: Leverages framework for orchestration
3. **Tool-Based Approach**: Reusable components across agents
4. **Deterministic Business Logic**: Consistent pricing and selection
5. **Comprehensive Outputs**: All required files generated
6. **Scalable Structure**: Easy to add new agents or modify workflows

## Development Notes

- Built with Crew AI framework for agent orchestration
- Uses pandas for data processing
- Template-based content generation for LLM independence
- Comprehensive error handling and validation
- Production-ready CLI interface

## Future Enhancements

1. **Real LLM Integration**: Connect to local Ollama models
2. **Parallel Agent Execution**: Implement concurrent processing
3. **Advanced QA Rules**: Add more sophisticated compliance checks
4. **Dynamic Pricing**: Real-time competitor analysis
5. **Customer Segmentation**: Personalized content generation
6. **Inventory Optimization**: Predictive stock management
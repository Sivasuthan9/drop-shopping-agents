# Shopify Dropshipping Operations Agent

A multi-agent hierarchical system for simulating Shopify dropshipping operations, built with the [CrewAI](https://crewai.com) framework.

## Overview

This system implements a complete dropshipping workflow using 7 specialized agents:
- **Manager Agent** - Orchestrates the entire workflow
- **Product Sourcing Agent** - Selects profitable products
- **Listing Agent** - Generates optimized product content
- **Pricing & Stock Agent** - Calculates prices and manages inventory
- **Order Routing Agent** - Processes orders and determines fulfillment
- **QA Agent** - Reviews content for compliance
- **Reporter Agent** - Generates daily operations reports

## Quick Start

### Prerequisites
- Python ≥3.10 <3.14
- Virtual environment activated

### Installation

1. **Clone and setup environment:**
```bash
git clone <repository-url>
cd drop-shopping-agents
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install crewai[tools] pandas
```

3. **Run the system:**
```bash
# Using standalone implementation (recommended)
python standalone_app.py --catalog data/supplier_catalog.csv --orders data/orders.csv --out out/

# Using CrewAI framework (requires LLM setup)
export PYTHONPATH="src:$PYTHONPATH"
python app.py --catalog data/supplier_catalog.csv --orders data/orders.csv --out out/
```

## Sample Data

The project includes sample data:
- **supplier_catalog.csv** - 32 products across multiple categories
- **orders.csv** - 20 customer orders for testing

## Output Files

The system generates 7 output files:
- `selection.json` - Selected products with pricing
- `listings.json` - Generated product content  
- `price_update.csv` - SKU pricing data
- `stock_update.csv` - Inventory levels
- `order_actions.json` - Order fulfillment decisions
- `listing_redlines.json` - QA review findings
- `daily_report.md` - Comprehensive operations summary

## Business Logic

### Product Selection Criteria
- Stock level ≥ 10 units
- Achievable margin ≥ 25%
- Selects top 10 products by margin

### Pricing Formula
- Platform fee: 2.9% + $0.30
- GST: 10% (Australia only)
- Minimum 25% margin
- Rounded to nearest $0.50

### Order Fulfillment
- **Fulfill**: Sufficient stock available
- **Backorder**: Partial stock available
- **Substitute**: No stock or SKU not selected

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design and agent specifications.

## LLM Configuration

### Local Models (Production)
The system is designed for local Ollama models:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama3
ollama pull mistral
```

### Environment Variables
```bash
# For local Ollama setup
OLLAMA_BASE_URL=http://localhost:11434

# For fallback/testing (not recommended for production)
OPENAI_API_KEY=your_key_here
```

## Development

### Project Structure
```
drop-shopping-agents/
├── src/dropshoping/          # CrewAI implementation
│   ├── config/               # Agent and task configurations
│   ├── tools/                # Custom tools for data processing
│   └── crew.py              # Main crew definition
├── data/                     # Sample input data
├── standalone_app.py         # Standalone implementation
├── app.py                   # CLI interface for CrewAI
└── ARCHITECTURE.md          # Detailed documentation
```

### Running with CrewAI

The CrewAI implementation requires proper LLM configuration:

```bash
# Set up environment
export PYTHONPATH="src:$PYTHONPATH"

# Run with default data
crewai run

# Run with custom data
python app.py --catalog your_catalog.csv --orders your_orders.csv --out output/
```

### Customizing Agents

Modify agent configurations in:
- `src/dropshoping/config/agents.yaml` - Agent roles and capabilities
- `src/dropshoping/config/tasks.yaml` - Task definitions and workflows

### Adding Tools

Create new tools in `src/dropshoping/tools/` and import them in `crew.py`.

## Sample Results

### Product Selection
- 32 products analyzed → 10 selected
- Average margin: 26.4%
- Stock range: 34-134 units

### Order Processing
- 20 orders processed
- 40% fulfilled, 60% substituted
- Customer emails generated

### Quality Assurance
- All listings reviewed
- Compliance issues identified
- Improvement recommendations provided

## Troubleshooting

### Common Issues

1. **LLM Connection Errors**
   - Use `standalone_app.py` for testing without LLM requirements
   - Verify Ollama is running: `ollama list`

2. **Import Errors**
   - Ensure PYTHONPATH includes `src/`: `export PYTHONPATH="src:$PYTHONPATH"`
   - Install in development mode: `pip install -e .`

3. **Data File Errors**
   - Verify CSV file paths and formats
   - Check sample data in `data/` directory

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check [CrewAI Documentation](https://docs.crewai.com)
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for detailed specifications
- Open an issue for bugs or feature requests

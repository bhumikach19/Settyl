# HSN Code Validation Agent

This project implements an HSN (Harmonized System Nomenclature) code validation system with a FastAPI webhook integration. It allows validation of HSN codes against a master database and provides detailed information about the codes including their hierarchical relationships.

## Features

- HSN code validation against master data
- Hierarchical code information
- FastAPI webhook integration
- Support for single and multiple code validation
- Built-in format validation (2-8 digits)

## Prerequisites

- Python 3.11 or higher
- Excel file containing HSN master data (`HSN_SAC.xlsx`)
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
├── HSN_SAC.xlsx              # Master data file
├── requirements.txt          # Python dependencies
├── hsn_adk_agent/           # Main project directory
│   ├── agent.yaml           # Agent configuration
│   ├── test_api.py         # API test script
│   ├── entities/           # Entity definitions
│   │   └── hsn_code.yaml   # HSN code entity
│   ├── intents/           # Intent definitions
│   │   └── validate_hsn_code.yaml
│   └── validator and webhook/
│       ├── hsn_agent.py    # Main agent logic
│       ├── hsn_validator_api.py  # Validation logic
│       └── hsn_webhook_api.py    # FastAPI webhook
```

## Configuration

1. Ensure your `HSN_SAC.xlsx` file is in the correct location and contains the required columns:
   - HSNCode
   - Description

## Running the Application

1. Start the FastAPI webhook server:
```bash
cd "hsn_adk_agent/validator and webhook"
uvicorn hsn_webhook_api:app --reload
```

2. The webhook will be available at `http://localhost:8000/webhook`

## Testing

You can test the API using the provided `test_api.py` script:

```bash
cd hsn_adk_agent
python test_api.py
```

Or use the interactive command-line interface:

```bash
cd "hsn_adk_agent/validator and webhook"
python hsn_agent.py
```

## API Usage

The webhook accepts POST requests with the following format:

```json
{
    "sessionInfo": {
        "parameters": {
            "hsn_code": ["01011090"]
        }
    }
}
```

Response format:

```json
{
    "fulfillment_response": {
        "messages": [
            {
                "text": {
                    "text": ["Response message with validation results"]
                }
            }
        ]
    }
}
```

## Features

1. **Code Validation**
   - Format checking (2-8 digits)
   - Existence validation against master data
   - Detailed description retrieval

2. **Hierarchical Information**
   - Parent code identification
   - Complete hierarchical chain

3. **Multiple Code Support**
   - Batch validation
   - Individual responses for each code

## Error Handling

The system provides clear error messages for:
- Invalid code formats
- Non-existent codes
- Missing or invalid input data
- Internal processing errors
  

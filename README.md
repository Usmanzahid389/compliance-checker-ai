# Compliance Checker

A sophisticated compliance checking system that uses ChatGPT and advanced matching algorithms to evaluate entries against worldcheck lists.

## Features

- Integration with ChatGPT API for sophisticated entry assessment
- Advanced matching algorithms beyond simple substring matching
- Risk scoring based on multiple factors:
  - Match quality
  - Category-based risk assessment
  - Geographic factors
  - Political exposure
  - AI-powered analysis
- Confidence scoring for match reliability
- Detailed explanations for each evaluation

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

The system requires an OpenAI API key. You can provide it in two ways:

1. Environment variable:
```bash
export OPENAI_API_KEY='your-api-key'
```

2. Direct initialization:
```python
evaluator = ComplianceEvaluator(api_key='your-api-key')
```

## Usage

```python
from compliance_checker.evaluator import ComplianceEvaluator
from compliance_checker.models import RefinitivBlacklistEntry, Match

# Initialize the evaluator
evaluator = ComplianceEvaluator()

# Create a match
match = Match(
    name="John Doe",
    birth_country="USA",
    category="POLITICAL INDIVIDUAL",
    match_score=0.85,
    type="PRIMARY",
    provider_id="refinitiv",
    reference_id="ref123"
)

# Create an entry
entry = RefinitivBlacklistEntry(
    step_id="step123",
    step_category="enrichment",
    provider_id="provider123",
    data_creation=datetime.utcnow(),
    information_object_id="info123",
    status="completed",
    time=-1,
    found=True,
    number_matches=1,
    matches=[match]
)

# Evaluate the entry
results = evaluator.evaluate_entry(entry)

# Process results
for result in results:
    print(f"Risk Score: {result.risk_score}")
    print(f"Confidence Score: {result.confidence_score}")
    print(f"Explanation: {result.explanation}")
    print(f"GPT Assessment: {result.gpt_assessment}")
```

## Testing

Run the tests using pytest:

```bash
pytest tests/
```

## Evaluation Criteria

The system evaluates entries based on multiple factors:

1. **Match Quality**: How well the entry matches against worldcheck lists
2. **Category Risk**: Risk level associated with the match category
3. **Geographic Risk**: Risk factors based on geographic location
4. **Political Exposure**: Assessment of political exposure level
5. **AI Analysis**: ChatGPT-powered analysis of the overall risk profile

## Output Format

Each evaluation produces a structured result containing:
- Risk score (0.0 to 1.0)
- Confidence score (0.0 to 1.0)
- Category classification
- Detailed explanation
- ChatGPT assessment
- Match details

## License

MIT License 
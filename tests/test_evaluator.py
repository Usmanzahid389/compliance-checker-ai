import pytest
from datetime import datetime
from compliance_checker.models import Match, RefinitivBlacklistEntry
from compliance_checker.evaluator import ComplianceEvaluator

@pytest.fixture
def sample_match():
    return Match(
        name="John",
        surname="Doe",
        birth_country="USA",
        identification_number=["123456"],
        comments="POLITICAL INDIVIDUAL, provider: WATCHLISTdetails: PEP",
        match_score=0.85,
        type="PRIMARY",
        provider_id="refinitiv",
        reference_id="ref123",
        category="POLITICAL INDIVIDUAL"
    )

@pytest.fixture
def sample_entry(sample_match):
    return RefinitivBlacklistEntry(
        step_id="step123",
        step_category="enrichment",
        provider_id="provider123",
        custom_groups=["group1"],
        data_creation=datetime.utcnow(),
        information_object_id="info123",
        status="completed",
        time=-1,
        found=True,
        number_matches=1,
        matches=[sample_match]
    )

def test_evaluator_initialization():
    """Test that evaluator raises error without API key."""
    with pytest.raises(ValueError):
        ComplianceEvaluator()

def test_category_score():
    """Test category risk scoring."""
    evaluator = ComplianceEvaluator(api_key="dummy_key")
    
    # Test high risk category
    assert evaluator._get_category_score("POLITICAL INDIVIDUAL") == 0.8
    
    # Test medium risk category
    assert evaluator._get_category_score("WATCH LIST") == 0.5
    
    # Test low risk category
    assert evaluator._get_category_score("OTHER") == 0.3
    
    # Test None category
    assert evaluator._get_category_score(None) == 0.5

def test_confidence_score(sample_match):
    """Test confidence score calculation."""
    evaluator = ComplianceEvaluator(api_key="dummy_key")
    
    confidence_score = evaluator._calculate_confidence_score(sample_match)
    assert 0 <= confidence_score <= 1.0
    
    # Test with minimal data
    minimal_match = Match(
        name="John",
        type="PRIMARY",
        provider_id="test",
        reference_id="test123",
        match_score=0.5
    )
    minimal_score = evaluator._calculate_confidence_score(minimal_match)
    assert minimal_score == 0.3  # Should be match_score * 0.6

def test_risk_score(sample_match):
    """Test risk score calculation."""
    evaluator = ComplianceEvaluator(api_key="dummy_key")
    
    risk_score = evaluator._calculate_risk_score(
        sample_match,
        "This appears to be a high risk individual."
    )
    assert 0 <= risk_score <= 1.0

def test_gpt_risk_extraction():
    """Test GPT assessment risk extraction."""
    evaluator = ComplianceEvaluator(api_key="dummy_key")
    
    assert evaluator._extract_gpt_risk_score("This is a high risk case.") == 0.8
    assert evaluator._extract_gpt_risk_score("This is a medium risk case.") == 0.5
    assert evaluator._extract_gpt_risk_score("This is a low risk case.") == 0.3
    assert evaluator._extract_gpt_risk_score("No clear risk level mentioned.") == 0.5 
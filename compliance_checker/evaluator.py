from typing import List, Optional
import os
from openai import OpenAI
from datetime import datetime

from .models import RefinitivBlacklistEntry, EvaluationResult, Match

class ComplianceEvaluator:
    """Main class for evaluating compliance entries using ChatGPT and sophisticated matching."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the evaluator with OpenAI API key."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")
        self.client = OpenAI(api_key=self.api_key)

    def _get_gpt_assessment(self, entry: RefinitivBlacklistEntry, match: Match) -> str:
        """Get assessment from ChatGPT for a specific match."""
        prompt = f"""
        Please assess the following potential match for compliance risk:
        
        Subject Information:
        - Name: {match.name} {match.surname or ''}
        - Birth Country: {match.birth_country or 'Unknown'}
        - Category: {match.category or 'Unknown'}
        - Comments: {match.comments or 'None'}
        
        Please provide a risk assessment considering:
        1. Political exposure level
        2. Geographic risk factors
        3. Category-based risk factors
        4. Any red flags in the comments
        
        Provide your assessment in a structured format.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a compliance risk assessment expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def evaluate_entry(self, entry: RefinitivBlacklistEntry) -> List[EvaluationResult]:
        """Evaluate a blacklist entry and return evaluation results."""
        results = []
        
        for match in entry.matches:
            # Get GPT assessment
            gpt_assessment = self._get_gpt_assessment(entry, match)
            
            # Calculate risk score based on multiple factors
            risk_score = self._calculate_risk_score(match, gpt_assessment)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(match)
            
            # Create evaluation result
            result = EvaluationResult(
                match_id=match.reference_id,
                evaluation_date=datetime.utcnow(),
                risk_score=risk_score,
                confidence_score=confidence_score,
                category=match.category or "UNKNOWN",
                explanation=self._generate_explanation(match, risk_score, confidence_score),
                gpt_assessment=gpt_assessment,
                matches=[match]
            )
            results.append(result)
        
        return results

    def _calculate_risk_score(self, match: Match, gpt_assessment: str) -> float:
        """Calculate risk score based on match data and GPT assessment."""
        # Base score from match score
        base_score = match.match_score * 0.4
        
        # Category-based score
        category_score = self._get_category_score(match.category) * 0.3
        
        # GPT assessment score
        gpt_score = self._extract_gpt_risk_score(gpt_assessment) * 0.3
        
        return min(1.0, base_score + category_score + gpt_score)

    def _calculate_confidence_score(self, match: Match) -> float:
        """Calculate confidence score for the match."""
        confidence = match.match_score * 0.6
        
        # Add confidence based on available data
        if match.birth_country:
            confidence += 0.1
        if match.identification_number:
            confidence += 0.2
        if match.comments:
            confidence += 0.1
            
        return min(1.0, confidence)

    def _get_category_score(self, category: Optional[str]) -> float:
        """Get risk score based on category."""
        high_risk_categories = {"POLITICAL INDIVIDUAL", "PEP", "SANCTIONS"}
        medium_risk_categories = {"WATCH LIST", "REGULATORY"}
        
        if not category:
            return 0.5
        
        category = category.upper()
        if category in high_risk_categories:
            return 0.8
        elif category in medium_risk_categories:
            return 0.5
        return 0.3

    def _extract_gpt_risk_score(self, assessment: str) -> float:
        """Extract risk score from GPT assessment."""
        # This is a simple implementation - could be made more sophisticated
        if "high risk" in assessment.lower():
            return 0.8
        elif "medium risk" in assessment.lower():
            return 0.5
        elif "low risk" in assessment.lower():
            return 0.3
        return 0.5

    def _generate_explanation(self, match: Match, risk_score: float, confidence_score: float) -> str:
        """Generate human-readable explanation for the evaluation."""
        risk_level = "HIGH" if risk_score >= 0.7 else "MEDIUM" if risk_score >= 0.4 else "LOW"
        confidence_level = "HIGH" if confidence_score >= 0.7 else "MEDIUM" if confidence_score >= 0.4 else "LOW"
        
        return f"""
        Risk Level: {risk_level} (Score: {risk_score:.2f})
        Confidence Level: {confidence_level} (Score: {confidence_score:.2f})
        Category: {match.category or 'Unknown'}
        Match Score: {match.match_score:.2f}
        Additional Factors: {match.comments or 'None'}
        """ 
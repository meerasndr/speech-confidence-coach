"""
Test script for OpenAI GPT API functionality
Tests structured feedback generation for the coaching system
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

class CoachingFeedback(BaseModel):
    """Pydantic model for structured coaching feedback"""
    strengths: List[str] = Field(description="List of positive aspects observed")
    improvements: List[str] = Field(description="List of specific areas to improve") 
    practice_drills: List[str] = Field(description="List of specific practice exercises")
    overall_score: int = Field(description="Overall score from 1-5", ge=1, le=5)

def test_basic_openai_api():
    """Test basic OpenAI API connectivity"""
    
    # Load environment variables
    load_dotenv()
    
    print("🤖 Testing OpenAI API connectivity...")
    
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ ERROR: OPENAI_API_KEY not found in environment variables")
        return False
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Simple test completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say 'API connection successful' if you can read this."}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ Basic API connection successful")
        print(f"   Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        return False

def test_structured_feedback():
    """Test structured JSON response for coaching feedback"""
    
    print("\n📝 Testing structured feedback generation...")
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Sample metrics that would come from audio analysis
        sample_metrics = {
            "words_per_minute": 145,
            "filler_word_count": 8,
            "filler_words": ["um", "uh", "like"],
            "total_duration": 90,  # seconds
            "average_pause": 0.8,
            "long_pauses": 3
        }
        
        # Sample transcript excerpt
        sample_transcript = "Um, so I think, uh, my biggest strength is definitely, like, problem-solving. I really enjoy, um, working through complex challenges and, uh, finding creative solutions."
        
        prompt = f"""
        You are a speech coach analyzing an interview response. Based on the metrics and transcript provided, generate structured feedback.
        
        METRICS:
        - Speaking pace: {sample_metrics['words_per_minute']} words per minute
        - Filler words: {sample_metrics['filler_word_count']} total ({', '.join(sample_metrics['filler_words'])})
        - Duration: {sample_metrics['total_duration']} seconds
        - Average pause: {sample_metrics['average_pause']} seconds
        - Long pauses (>1s): {sample_metrics['long_pauses']}
        
        TRANSCRIPT EXCERPT:
        "{sample_transcript}"
        
        Provide coaching feedback focusing on measurable speech delivery aspects only.
        """
        
        # Test with structured output
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional speech coach focused on measurable delivery aspects."},
                {"role": "user", "content": prompt}
            ],
            response_format=CoachingFeedback,
        )
        
        feedback = response.choices[0].message.parsed
        
        print("✅ Structured feedback generation successful:")
        print(f"   Overall Score: {feedback.overall_score}/5")
        print(f"   Strengths ({len(feedback.strengths)}): {feedback.strengths[0] if feedback.strengths else 'None'}")
        print(f"   Improvements ({len(feedback.improvements)}): {feedback.improvements[0] if feedback.improvements else 'None'}")
        print(f"   Practice Drills ({len(feedback.practice_drills)}): {feedback.practice_drills[0] if feedback.practice_drills else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Structured feedback test failed: {str(e)}")
        return False

def test_json_schema_validation():
    """Test that the response follows the expected JSON structure"""
    
    print("\n🔍 Testing JSON schema validation...")
    
    try:
        # This tests that our Pydantic model works correctly
        test_data = {
            "strengths": ["Clear articulation", "Good pace"],
            "improvements": ["Reduce filler words", "Shorter pauses"],
            "practice_drills": ["Record 30-second response without filler words"],
            "overall_score": 3
        }
        
        feedback = CoachingFeedback(**test_data)
        print("✅ Pydantic model validation successful")
        print(f"   Model created: {feedback.overall_score}/5 score")
        
        # Test invalid data
        try:
            invalid_data = {
                "strengths": ["Good"],
                "improvements": ["Better"],
                "practice_drills": ["Practice"],
                "overall_score": 10  # Invalid - should be 1-5
            }
            CoachingFeedback(**invalid_data)
            print("❌ Schema validation failed - should have rejected invalid score")
            return False
        except:
            print("✅ Schema properly rejects invalid data")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== OpenAI GPT API Test ===\n")
    
    basic_success = test_basic_openai_api()
    structured_success = test_structured_feedback() if basic_success else False
    schema_success = test_json_schema_validation()
    
    print(f"\n=== Test Results ===")
    print(f"Basic API: {'✅ PASS' if basic_success else '❌ FAIL'}")
    print(f"Structured Feedback: {'✅ PASS' if structured_success else '❌ FAIL'}")
    print(f"Schema Validation: {'✅ PASS' if schema_success else '❌ FAIL'}")
    
    if basic_success and structured_success and schema_success:
        print("\n🎉 All OpenAI tests passed! Ready for feedback generation.")
    else:
        print("\n⚠️  Some tests failed. Please resolve issues before continuing.")
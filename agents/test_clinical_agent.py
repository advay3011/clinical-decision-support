"""
Test script for Clinical Decision Support Agent
Demonstrates the chatbot with sample conversations
"""

from strands import Agent, tool
from clinical_decision_support_agent import (
    assess_vitals,
    check_symptoms,
    check_drug_interaction,
    get_treatment_guidelines,
    summarize_patient_session,
    search_medical_knowledge,
    agent
)


def test_sample_conversation():
    """
    Test the agent with the sample conversation flow:
    - Blood pressure reading
    - Symptom check
    - Stress discussion
    - Medication check
    - Session summary
    """
    print("\n" + "="*70)
    print("CLINICAL DECISION SUPPORT AGENT - TEST CONVERSATION")
    print("="*70 + "\n")
    
    test_inputs = [
        "hey my blood pressure is 160 over 90",
        "no dizziness or anything",
        "i've also been stressed lately",
        "i take metformin, just started lisinopril too",
        "can you summarize what we talked about?"
    ]
    
    print("Running sample conversation...\n")
    print("-"*70)
    
    for user_input in test_inputs:
        print(f"\nYou: {user_input}")
        print("-"*70)
        
        try:
            result = agent(user_input)
            
            # Extract text from AgentResult object
            if hasattr(result, 'message'):
                # It's an AgentResult object
                content = result.message.get('content', [])
                if isinstance(content, list) and len(content) > 0:
                    response = content[0].get('text', str(result))
                else:
                    response = str(result)
            else:
                # It's already a string
                response = str(result)
            
            print(f"Agent: {response}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")


def test_tools_directly():
    """Test individual tools to verify they work correctly."""
    print("\n" + "="*70)
    print("TESTING INDIVIDUAL TOOLS")
    print("="*70 + "\n")
    
    # Test assess_vitals
    print("1. Testing assess_vitals(160, 90, 85):")
    result = assess_vitals(160, 90, 85)
    print(f"   BP Status: {result['bp_status']}")
    print(f"   HR Status: {result['hr_status']}")
    print(f"   Flags: {result['flags']}\n")
    
    # Test check_symptoms
    print("2. Testing check_symptoms(['headache', 'fatigue']):")
    result = check_symptoms(['headache', 'fatigue'])
    print(f"   Possible conditions: {[c['condition'] for c in result['possible_conditions']]}\n")
    
    # Test check_drug_interaction
    print("3. Testing check_drug_interaction(['metformin', 'lisinopril']):")
    result = check_drug_interaction(['metformin', 'lisinopril'])
    print(f"   Safe: {result['safe']}")
    print(f"   Interactions: {result['interactions']}\n")
    
    # Test get_treatment_guidelines
    print("4. Testing get_treatment_guidelines('high blood pressure'):")
    result = get_treatment_guidelines('high blood pressure')
    print(f"   Condition: {result['condition']}")
    print(f"   Explanation: {result['simple_explanation']}\n")
    
    # Test search_medical_knowledge
    print("5. Testing search_medical_knowledge('blood pressure'):")
    result = search_medical_knowledge('blood pressure')
    print(f"   Result: {result['result']}\n")


if __name__ == "__main__":
    # Run tool tests first
    test_tools_directly()
    
    # Then run sample conversation
    test_sample_conversation()
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print("\nTo run the interactive chatbot, use:")
    print("  python agents/clinical_decision_support_agent.py")

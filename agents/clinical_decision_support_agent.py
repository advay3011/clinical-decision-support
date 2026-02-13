"""
Clinical Decision Support Chatbot Agent
A friendly, knowledgeable clinical assistant that helps patients understand their health.
"""

from strands import Agent, tool
import json
from datetime import datetime


# ============================================================================
# TOOLS
# ============================================================================

@tool
def assess_vitals(systolic: int, diastolic: int, heart_rate: int) -> dict:
    """
    Evaluates blood pressure and heart rate, flags if abnormal.
    Returns assessment with status and recommendations.
    """
    assessment = {
        "timestamp": datetime.now().isoformat(),
        "systolic": systolic,
        "diastolic": diastolic,
        "heart_rate": heart_rate,
        "bp_status": "",
        "hr_status": "",
        "flags": []
    }
    
    # Blood pressure assessment
    if systolic < 90 or diastolic < 60:
        assessment["bp_status"] = "low"
        assessment["flags"].append("Low blood pressure - may cause dizziness")
    elif systolic < 120 and diastolic < 80:
        assessment["bp_status"] = "normal"
    elif systolic < 130 and diastolic < 80:
        assessment["bp_status"] = "elevated"
        assessment["flags"].append("Slightly elevated - monitor and manage stress")
    elif systolic < 140 or diastolic < 90:
        assessment["bp_status"] = "stage1_hypertension"
        assessment["flags"].append("Stage 1 hypertension - lifestyle changes recommended")
    else:
        assessment["bp_status"] = "stage2_hypertension"
        assessment["flags"].append("Stage 2 hypertension - medical attention recommended")
    
    # Heart rate assessment
    if heart_rate < 60:
        assessment["hr_status"] = "low"
        assessment["flags"].append("Resting heart rate is low - may be normal for athletes")
    elif heart_rate <= 100:
        assessment["hr_status"] = "normal"
    else:
        assessment["hr_status"] = "elevated"
        assessment["flags"].append("Elevated heart rate - check if stressed or unwell")
    
    return assessment


@tool
def check_symptoms(symptoms: list[str]) -> dict:
    """
    Cross-references symptoms and returns possible conditions ranked by likelihood.
    """
    # Simplified symptom-condition mapping
    symptom_conditions = {
        "headache": ["tension headache", "migraine", "dehydration", "high blood pressure"],
        "chest pain": ["anxiety", "muscle strain", "heartburn", "heart condition"],
        "shortness of breath": ["anxiety", "asthma", "heart condition", "infection"],
        "dizziness": ["low blood pressure", "dehydration", "inner ear issue", "anxiety"],
        "fatigue": ["anemia", "thyroid issue", "depression", "sleep deprivation"],
        "nausea": ["food poisoning", "medication side effect", "anxiety", "infection"],
        "fever": ["infection", "flu", "cold", "inflammation"],
        "cough": ["cold", "flu", "asthma", "allergies"],
        "sore throat": ["strep throat", "cold", "flu", "allergies"],
        "joint pain": ["arthritis", "injury", "inflammation", "overuse"],
    }
    
    conditions_found = {}
    for symptom in symptoms:
        symptom_lower = symptom.lower()
        if symptom_lower in symptom_conditions:
            for condition in symptom_conditions[symptom_lower]:
                conditions_found[condition] = conditions_found.get(condition, 0) + 1
    
    # Rank by frequency
    ranked = sorted(conditions_found.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "symptoms_checked": symptoms,
        "possible_conditions": [{"condition": c, "relevance": r} for c, r in ranked[:5]],
        "disclaimer": "These are possibilities only - a real doctor needs to examine you for diagnosis"
    }


@tool
def check_drug_interaction(drugs: list[str]) -> dict:
    """
    Checks for known dangerous interactions between medications.
    """
    # Simplified interaction database
    interactions = {
        ("metformin", "lisinopril"): {"severity": "low", "note": "No major interaction"},
        ("aspirin", "warfarin"): {"severity": "high", "note": "Increased bleeding risk"},
        ("metformin", "alcohol"): {"severity": "moderate", "note": "May increase lactic acidosis risk"},
        ("lisinopril", "potassium"): {"severity": "moderate", "note": "May raise potassium levels"},
    }
    
    result = {
        "drugs_checked": drugs,
        "interactions": [],
        "safe": True
    }
    
    # Check all pairs
    for i, drug1 in enumerate(drugs):
        for drug2 in drugs[i+1:]:
            key1 = (drug1.lower(), drug2.lower())
            key2 = (drug2.lower(), drug1.lower())
            
            if key1 in interactions:
                result["interactions"].append({
                    "drugs": [drug1, drug2],
                    **interactions[key1]
                })
                if interactions[key1]["severity"] in ["high", "moderate"]:
                    result["safe"] = False
            elif key2 in interactions:
                result["interactions"].append({
                    "drugs": [drug2, drug1],
                    **interactions[key2]
                })
                if interactions[key2]["severity"] in ["high", "moderate"]:
                    result["safe"] = False
    
    return result


@tool
def get_treatment_guidelines(condition: str) -> dict:
    """
    Pulls plain English treatment guidelines for a given condition.
    """
    guidelines = {
        "high blood pressure": {
            "condition": "High Blood Pressure (Hypertension)",
            "simple_explanation": "Your heart is working harder than it needs to, which can strain your blood vessels over time.",
            "lifestyle_changes": [
                "Cut back on salt - aim for less than 2,300mg per day",
                "Drink more water - helps your kidneys regulate pressure",
                "Move your body - even 20-30 min walks most days help",
                "Manage stress - try deep breathing or meditation",
                "Limit alcohol - no more than 1-2 drinks per day"
            ],
            "when_to_see_doctor": "If readings stay above 140/90 or you feel chest pain, shortness of breath, or severe headaches"
        },
        "anxiety": {
            "condition": "Anxiety",
            "simple_explanation": "Your body is in 'alert mode' even when there's no real danger. This is treatable.",
            "lifestyle_changes": [
                "Deep breathing - try 4 counts in, 4 counts out",
                "Regular exercise - helps burn off nervous energy",
                "Limit caffeine - can make anxiety worse",
                "Get good sleep - aim for 7-9 hours",
                "Talk to someone - friends, family, or a therapist"
            ],
            "when_to_see_doctor": "If anxiety interferes with daily life or doesn't improve with lifestyle changes"
        },
        "tension headache": {
            "condition": "Tension Headache",
            "simple_explanation": "Muscles in your neck and scalp are tight, usually from stress or poor posture.",
            "lifestyle_changes": [
                "Relax your shoulders - they're probably tense",
                "Take breaks from screens - every 30 minutes",
                "Stretch your neck gently - slow, no bouncing",
                "Stay hydrated - dehydration triggers headaches",
                "Apply heat or cold - whatever feels better"
            ],
            "when_to_see_doctor": "If headaches are severe, frequent, or different from your usual pattern"
        }
    }
    
    condition_lower = condition.lower()
    if condition_lower in guidelines:
        return guidelines[condition_lower]
    else:
        return {
            "condition": condition,
            "note": "I don't have specific guidelines for this condition. Please consult a healthcare provider.",
            "disclaimer": "Always see a real doctor for proper diagnosis and treatment"
        }


@tool
def summarize_patient_session(notes: str) -> dict:
    """
    Summarizes everything discussed in the conversation into a clean health report.
    """
    return {
        "session_date": datetime.now().isoformat(),
        "session_summary": notes,
        "next_steps": [
            "Follow up with your primary care doctor",
            "Monitor any changes in symptoms",
            "Keep track of vital signs if applicable",
            "Note any new symptoms that develop"
        ],
        "disclaimer": "This summary is for your records only and does not replace professional medical advice"
    }


@tool
def search_medical_knowledge(query: str) -> dict:
    """
    Searches medical knowledge base for relevant information.
    """
    # Simplified knowledge base
    knowledge_base = {
        "blood pressure": "Blood pressure is the force of blood pushing against artery walls. Normal is below 120/80. High blood pressure (hypertension) increases risk of heart disease and stroke.",
        "heart rate": "Normal resting heart rate is 60-100 beats per minute. Athletes may have lower rates. Stress, caffeine, and illness can raise it.",
        "stress": "Chronic stress can raise blood pressure, weaken immunity, and cause headaches. Managing stress through exercise, sleep, and relaxation helps.",
        "metformin": "A diabetes medication that helps control blood sugar. Take with food to avoid stomach upset. Can interact with alcohol.",
        "lisinopril": "A blood pressure medication (ACE inhibitor). May cause a dry cough. Take at the same time each day.",
    }
    
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return {
                "query": query,
                "result": value,
                "source": "Clinical knowledge base"
            }
    
    return {
        "query": query,
        "result": "No specific information found. Please consult a healthcare provider.",
        "source": "Clinical knowledge base"
    }


# ============================================================================
# AGENT SETUP
# ============================================================================

system_prompt = """You are a friendly and knowledgeable clinical assistant. You talk to patients in simple, warm, plain English — never cold or robotic.

KEY BEHAVIORS:
1. When someone shares a symptom or vital, acknowledge how they feel first, then ask ONE natural follow-up question
2. Listen carefully and remember everything they tell you
3. Once you have enough context, transition smoothly into simple practical advice
4. Never keep asking questions without eventually giving guidance
5. If a patient says "no" to a symptom, acknowledge it and either ask one more relevant question OR move into advice naturally
6. Mirror the patient's energy - if casual, be casual; if worried, be warm and reassuring
7. Always remind users to see a real doctor for anything serious
8. End responses with a natural follow-up question to keep conversation going
9. Never dump all information at once - share one key insight at a time

TONE: Like a friendly, experienced doctor who actually listens and explains things clearly.

DISCLAIMER: Always remind patients that you're a clinical assistant, not a replacement for real medical care. For serious concerns, they need to see a real doctor."""

agent = Agent(
    tools=[
        assess_vitals,
        check_symptoms,
        check_drug_interaction,
        get_treatment_guidelines,
        summarize_patient_session,
        search_medical_knowledge
    ],
    system_prompt=system_prompt
)


# ============================================================================
# CONVERSATION LOOP
# ============================================================================

def run_chatbot():
    """Run the clinical decision support chatbot."""
    print("\n" + "="*70)
    print("CLINICAL DECISION SUPPORT CHATBOT")
    print("="*70)
    print("\nHi! I'm your clinical assistant. I'm here to listen and help you")
    print("understand what's going on with your health. Remember, I'm not a")
    print("replacement for a real doctor — just a friendly guide.\n")
    print("Type 'quit' to exit.\n")
    print("-"*70 + "\n")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nAgent: Take care of yourself! Remember to follow up with your doctor if needed. Bye!")
                break
            
            if not user_input:
                continue
            
            # Get response from agent
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
            
            print(f"\nAgent: {response}\n")
            
            # Store in history
            conversation_history.append({
                "user": user_input,
                "agent": response
            })
            
        except KeyboardInterrupt:
            print("\n\nAgent: Take care! Remember to see your doctor if needed.")
            break
        except Exception as e:
            print(f"\nAgent: I encountered an issue: {str(e)}")
            print("Let's try again.\n")


if __name__ == "__main__":
    run_chatbot()

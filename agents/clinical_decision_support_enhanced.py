"""
Clinical Decision Support Chatbot - Enhanced with Real Medical Data
Integrates RxNorm API for real drug information and interactions
"""

from strands import Agent, tool
import requests
from datetime import datetime
import json

# ============================================================================
# REAL MEDICAL DATA TOOLS (RxNorm API)
# ============================================================================

@tool
def get_real_drug_info(drug_name: str) -> dict:
    """Get real drug information from RxNorm API (NIH)."""
    try:
        # Search for drug
        search_url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={drug_name}"
        search_response = requests.get(search_url, timeout=5)
        search_data = search_response.json()
        
        if not search_data.get('drugGroup', {}).get('conceptGroup'):
            return {"error": f"Drug '{drug_name}' not found in RxNorm database"}
        
        # Get first result
        concept = search_data['drugGroup']['conceptGroup'][0]['conceptProperties'][0]
        rxcui = concept['rxcui']
        
        # Get drug properties
        props_url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/properties.json"
        props_response = requests.get(props_url, timeout=5)
        props_data = props_response.json()
        
        return {
            "name": concept['name'],
            "rxcui": rxcui,
            "tty": concept['tty'],
            "found": True,
            "source": "RxNorm (NIH)"
        }
    except Exception as e:
        return {"error": str(e), "found": False}


@tool
def check_real_drug_interactions(drug_names: list[str]) -> dict:
    """Check real drug interactions from RxNorm API."""
    try:
        # Get RXCUIs for all drugs
        rxcuis = []
        drug_info = {}
        
        for drug in drug_names:
            search_url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={drug}"
            response = requests.get(search_url, timeout=5)
            data = response.json()
            
            if data.get('drugGroup', {}).get('conceptGroup'):
                concept = data['drugGroup']['conceptGroup'][0]['conceptProperties'][0]
                rxcui = concept['rxcui']
                rxcuis.append(rxcui)
                drug_info[drug] = concept['name']
        
        if len(rxcuis) < 2:
            return {
                "safe": True,
                "interactions": [],
                "note": "Need at least 2 valid drugs to check interactions"
            }
        
        # Check interactions
        interaction_url = "https://rxnav.nlm.nih.gov/REST/interaction/list.json"
        params = {"rxcuis": "+".join(rxcuis)}
        response = requests.get(interaction_url, params=params, timeout=5)
        interaction_data = response.json()
        
        interactions = []
        if 'fullInteractionTypeGroup' in interaction_data:
            for group in interaction_data['fullInteractionTypeGroup']:
                for interaction in group.get('fullInteractionType', []):
                    for pair in interaction.get('interactionPair', []):
                        interactions.append({
                            "drugs": [pair['interactionConcept'][0]['sourceConceptItem']['name'],
                                     pair['interactionConcept'][1]['sourceConceptItem']['name']],
                            "severity": pair.get('severity', 'Unknown'),
                            "description": pair.get('description', 'No description available')
                        })
        
        return {
            "safe": len(interactions) == 0,
            "interactions": interactions,
            "drugs_checked": drug_info,
            "source": "RxNorm (NIH)"
        }
    except Exception as e:
        return {"error": str(e), "safe": True, "interactions": []}


@tool
def get_drug_adverse_events(drug_name: str) -> dict:
    """Get real adverse events from OpenFDA API."""
    try:
        url = "https://api.fda.gov/drug/event.json"
        params = {
            "search": f'patient.drug.openfda.generic_name:"{drug_name}"',
            "limit": 5,
            "count": "patient.reaction.reactionmeddrapt.exact"
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if 'results' in data and data['results']:
            adverse_events = []
            for result in data['results'][:5]:
                adverse_events.append({
                    "reaction": result.get('term', 'Unknown'),
                    "count": result.get('count', 0)
                })
            
            return {
                "drug": drug_name,
                "adverse_events": adverse_events,
                "source": "OpenFDA"
            }
        return {
            "drug": drug_name,
            "adverse_events": [],
            "note": "No adverse event data found"
        }
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# ORIGINAL TOOLS (Kept for compatibility)
# ============================================================================

@tool
def assess_vitals(systolic: int, diastolic: int, heart_rate: int) -> dict:
    """Evaluates blood pressure and heart rate, flags if abnormal."""
    assessment = {
        "timestamp": datetime.now().isoformat(),
        "systolic": systolic,
        "diastolic": diastolic,
        "heart_rate": heart_rate,
        "bp_status": "",
        "hr_status": "",
        "flags": []
    }
    
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
    """Cross-references symptoms and returns possible conditions ranked by likelihood."""
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
    
    ranked = sorted(conditions_found.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "symptoms_checked": symptoms,
        "possible_conditions": [{"condition": c, "relevance": r} for c, r in ranked[:5]],
        "disclaimer": "These are possibilities only - a real doctor needs to examine you for diagnosis"
    }


@tool
def get_treatment_guidelines(condition: str) -> dict:
    """Pulls plain English treatment guidelines for a given condition."""
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
    """Summarizes everything discussed in the conversation into a clean health report."""
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
    """Searches medical knowledge base for relevant information."""
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
10. When checking medications, use real drug data from RxNorm API
11. When checking interactions, provide real data from medical databases

TONE: Like a friendly, experienced doctor who actually listens and explains things clearly.

DISCLAIMER: Always remind patients that you're a clinical assistant, not a replacement for real medical care. For serious concerns, they need to see a real doctor."""

agent = Agent(
    model="us.amazon.nova-2-lite-v1:0",
    tools=[
        # Real medical data tools
        get_real_drug_info,
        check_real_drug_interactions,
        get_drug_adverse_events,
        # Original tools
        assess_vitals,
        check_symptoms,
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
    """Run the enhanced clinical decision support chatbot."""
    print("\n" + "="*70)
    print("CLINICAL DECISION SUPPORT CHATBOT - ENHANCED WITH REAL MEDICAL DATA")
    print("="*70)
    print("\nHi! I'm your clinical assistant. I'm here to listen and help you")
    print("understand what's going on with your health. I now have access to")
    print("real medical data from NIH and FDA databases.\n")
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
                content = result.message.get('content', [])
                if isinstance(content, list) and len(content) > 0:
                    response = content[0].get('text', str(result))
                else:
                    response = str(result)
            else:
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

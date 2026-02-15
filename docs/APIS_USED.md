# APIs Used in Clinical Decision Support Chatbot

## Quick Answer

**Yes, the chatbot uses 2 real medical APIs:**

1. **RxNorm API** (from NIH)
2. **OpenFDA API** (from FDA)

## Which Tools Use APIs?

### Tools That Use APIs (Real Data)

| Tool | API | Source | Data |
|------|-----|--------|------|
| `get_real_drug_info()` | RxNorm | NIH | Real drug information |
| `check_real_drug_interactions()` | RxNorm | NIH | Real drug interactions |
| `get_drug_adverse_events()` | OpenFDA | FDA | Real adverse events |

### Tools That DON'T Use APIs (Local Logic)

| Tool | Type | Data |
|------|------|------|
| `assess_vitals()` | Local logic | Hardcoded medical standards |
| `check_symptoms()` | Local logic | Hardcoded symptom database |
| `check_drug_interaction()` | Local logic | Hardcoded interaction database |
| `get_treatment_guidelines()` | Local logic | Hardcoded guidelines |
| `summarize_patient_session()` | Local logic | Summarizes conversation |
| `search_medical_knowledge()` | Local logic | Hardcoded knowledge base |

## The APIs Explained

### 1. RxNorm API (NIH)

**What it is:** National Institutes of Health drug database

**What it provides:**
- Real drug names and information
- Real drug interactions
- Drug codes (RxCUI)
- Drug properties

**URL:** `https://rxnav.nlm.nih.gov/REST/`

**Example:**
```
Request: https://rxnav.nlm.nih.gov/REST/drugs.json?name=aspirin
Response: {
  "drugGroup": {
    "conceptGroup": [{
      "conceptProperties": [{
        "name": "Aspirin",
        "rxcui": "7682"
      }]
    }]
  }
}
```

**Cost:** FREE - No API key needed

**Rate Limit:** Unlimited

### 2. OpenFDA API (FDA)

**What it is:** Food and Drug Administration adverse event database

**What it provides:**
- Real adverse events (side effects)
- Number of reports for each adverse event
- Drug safety information
- Recall information

**URL:** `https://api.fda.gov/drug/event.json`

**Example:**
```
Request: https://api.fda.gov/drug/event.json?search=aspirin
Response: {
  "results": [
    {
      "term": "FATIGUE",
      "count": 32886
    },
    {
      "term": "NAUSEA",
      "count": 27987
    }
  ]
}
```

**Cost:** FREE - No API key needed

**Rate Limit:** 240 requests per minute

## How They're Used

### Example 1: Drug Information

```
User: "Tell me about aspirin"
     ↓
Agent: "I'll use get_real_drug_info()"
     ↓
Tool calls RxNorm API:
  GET https://rxnav.nlm.nih.gov/REST/drugs.json?name=aspirin
     ↓
API returns: Real drug data from NIH
     ↓
Agent: "Aspirin is a common pain reliever..."
```

### Example 2: Drug Interactions

```
User: "Is aspirin safe with warfarin?"
     ↓
Agent: "I'll use check_real_drug_interactions()"
     ↓
Tool calls RxNorm API:
  GET https://rxnav.nlm.nih.gov/REST/interaction/list.json
     ↓
API returns: Real interaction data from NIH
     ↓
Agent: "These have a HIGH severity interaction..."
```

### Example 3: Adverse Events

```
User: "What are the side effects of aspirin?"
     ↓
Agent: "I'll use get_drug_adverse_events()"
     ↓
Tool calls OpenFDA API:
  GET https://api.fda.gov/drug/event.json?search=aspirin
     ↓
API returns: Real adverse events from FDA
     ↓
Agent: "The most reported side effects are fatigue (32,886 reports)..."
```

## API Comparison

| Feature | RxNorm | OpenFDA |
|---------|--------|---------|
| Source | NIH | FDA |
| Data | Drug info, interactions | Adverse events |
| Cost | FREE | FREE |
| API Key | Not needed | Not needed |
| Rate Limit | Unlimited | 240/min |
| Reliability | Excellent | Excellent |
| Data Quality | Excellent | Excellent |

## Local vs Real Data

### Local Data (Hardcoded)

```python
# In assess_vitals()
if systolic < 120 and diastolic < 80:
    status = "normal"
```

**Pros:**
- Fast (no API call)
- Always available
- No rate limits

**Cons:**
- Limited data
- Can't be updated easily
- Not comprehensive

### Real Data (API)

```python
# In get_drug_adverse_events()
response = requests.get("https://api.fda.gov/drug/event.json?search=aspirin")
```

**Pros:**
- Real, up-to-date data
- Comprehensive
- From trusted sources (NIH, FDA)

**Cons:**
- Slower (API call takes time)
- Requires internet
- Rate limits

## Which Tools Use Which?

### RxNorm API Tools

```python
@tool
def get_real_drug_info(drug_name: str) -> dict:
    # Calls RxNorm API
    url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={drug_name}"
    response = requests.get(url)
    return response.json()

@tool
def check_real_drug_interactions(drug_names: list[str]) -> dict:
    # Calls RxNorm API
    url = "https://rxnav.nlm.nih.gov/REST/interaction/list.json"
    response = requests.get(url, params={"rxcuis": "+".join(rxcuis)})
    return response.json()
```

### OpenFDA API Tools

```python
@tool
def get_drug_adverse_events(drug_name: str) -> dict:
    # Calls OpenFDA API
    url = "https://api.fda.gov/drug/event.json"
    params = {"search": f'patient.drug.openfda.generic_name:"{drug_name}"'}
    response = requests.get(url, params=params)
    return response.json()
```

## Real Data Examples

### From RxNorm

```
Drug: Aspirin
RxCUI: 7682
Type: Branded Drug
```

### From OpenFDA

```
Drug: Aspirin
Adverse Events:
- Fatigue: 32,886 reports
- Nausea: 27,987 reports
- Dyspnoea: 27,807 reports
```

## Summary

**APIs Used:**
- ✅ RxNorm API (NIH) - Drug information and interactions
- ✅ OpenFDA API (FDA) - Adverse events

**Cost:**
- ✅ Both completely FREE
- ✅ No API keys needed
- ✅ No authentication required

**Tools Using APIs:**
- ✅ get_real_drug_info()
- ✅ check_real_drug_interactions()
- ✅ get_drug_adverse_events()

**Tools NOT Using APIs:**
- ✅ assess_vitals() - Local logic
- ✅ check_symptoms() - Local database
- ✅ check_drug_interaction() - Local database
- ✅ get_treatment_guidelines() - Local database
- ✅ summarize_patient_session() - Local logic
- ✅ search_medical_knowledge() - Local database

**Why APIs?**
- Real, trusted medical data
- Always up-to-date
- From official sources (NIH, FDA)
- More accurate than hardcoded data

---

**Want to test the APIs?** Run:
```bash
python agents/test_real_medical_data.py
```

This will show you real data from both APIs! 🏥

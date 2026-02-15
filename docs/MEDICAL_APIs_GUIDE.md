# Real Medical Data APIs - Integration Guide

Integrate real medical data into your Clinical Decision Support chatbot.

## 🏥 Top Free Medical APIs

### 1. **RxNorm API** (Drug Information) ⭐ BEST
- **What**: Comprehensive drug database from NIH
- **Free**: Yes, completely free
- **Data**: Drug names, interactions, side effects, dosages
- **Use**: Replace hardcoded medication database
- **Docs**: https://rxnav.nlm.nih.gov/APIs_RxNorm.html

```python
# Example: Get drug info
import requests

def get_drug_info(drug_name):
    url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={drug_name}"
    response = requests.get(url)
    return response.json()

# Example: Check drug interactions
def check_interactions(rxcui_list):
    url = "https://rxnav.nlm.nih.gov/REST/interaction/list.json"
    params = {"rxcuis": "+".join(rxcui_list)}
    response = requests.get(url, params=params)
    return response.json()
```

### 2. **OpenFDA API** (Drug & Device Data)
- **What**: FDA drug and device database
- **Free**: Yes, with rate limits
- **Data**: Adverse events, recalls, drug labels
- **Use**: Real drug side effects and warnings
- **Docs**: https://open.fda.gov/

```python
def get_drug_adverse_events(drug_name):
    url = "https://api.fda.gov/drug/event.json"
    params = {
        "search": f"patient.drug.openfda.generic_name:{drug_name}",
        "limit": 10
    }
    response = requests.get(url, params=params)
    return response.json()
```

### 3. **SNOMED CT Browser API** (Medical Terminology)
- **What**: Standardized medical terminology
- **Free**: Yes
- **Data**: Disease codes, symptoms, conditions
- **Use**: Standardize symptom/condition names
- **Docs**: https://browser.ihtsdotools.org/

```python
def search_snomed(query):
    url = "https://browser.ihtsdotools.org/api/v1/concepts"
    params = {"query": query}
    response = requests.get(url, params=params)
    return response.json()
```

### 4. **PubMed API** (Medical Research)
- **What**: Access to medical literature
- **Free**: Yes
- **Data**: Research papers, clinical trials
- **Use**: Get evidence-based treatment info
- **Docs**: https://www.ncbi.nlm.nih.gov/books/NBK25499/

```python
def search_pubmed(query):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "rettype": "json"
    }
    response = requests.get(url, params=params)
    return response.json()
```

### 5. **ICD-10 API** (Disease Codes)
- **What**: International disease classification
- **Free**: Yes (some providers)
- **Data**: Disease codes and descriptions
- **Use**: Standardize condition names
- **Docs**: https://www.cms.gov/medicare/coding-billing/icd-10-codes

### 6. **LOINC API** (Lab Tests)
- **What**: Laboratory test codes
- **Free**: Yes
- **Data**: Lab test names, codes, normal ranges
- **Use**: Understand lab results
- **Docs**: https://loinc.org/

### 7. **MeSH API** (Medical Subject Headings)
- **What**: NIH medical terminology
- **Free**: Yes
- **Data**: Medical terms and relationships
- **Use**: Better symptom understanding
- **Docs**: https://www.nlm.nih.gov/mesh/

## 🚀 Recommended Integration Plan

### Phase 1: Drug Information (Easiest)
1. Integrate RxNorm API
2. Replace hardcoded drug database
3. Add real drug interactions
4. Add real side effects

### Phase 2: Adverse Events
1. Integrate OpenFDA API
2. Show real adverse event data
3. Add warning levels

### Phase 3: Conditions & Symptoms
1. Integrate SNOMED CT
2. Standardize symptom names
3. Better condition matching

### Phase 4: Research & Evidence
1. Integrate PubMed API
2. Show evidence-based treatments
3. Link to research papers

## 💻 Implementation Example

Here's how to integrate RxNorm into your chatbot:

```python
import requests
from strands import tool

@tool
def get_real_drug_info(drug_name: str) -> dict:
    """Get real drug information from RxNorm API."""
    try:
        # Search for drug
        search_url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={drug_name}"
        search_response = requests.get(search_url)
        search_data = search_response.json()
        
        if not search_data.get('drugGroup', {}).get('conceptGroup'):
            return {"error": f"Drug '{drug_name}' not found"}
        
        # Get first result
        concept = search_data['drugGroup']['conceptGroup'][0]['conceptProperties'][0]
        rxcui = concept['rxcui']
        
        # Get drug properties
        props_url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/properties.json"
        props_response = requests.get(props_url)
        props_data = props_response.json()
        
        return {
            "name": concept['name'],
            "rxcui": rxcui,
            "tty": concept['tty'],
            "properties": props_data.get('properties', {})
        }
    except Exception as e:
        return {"error": str(e)}

@tool
def check_real_drug_interactions(drug_names: list[str]) -> dict:
    """Check real drug interactions from RxNorm API."""
    try:
        # Get RXCUIs for all drugs
        rxcuis = []
        for drug in drug_names:
            search_url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={drug}"
            response = requests.get(search_url)
            data = response.json()
            
            if data.get('drugGroup', {}).get('conceptGroup'):
                rxcui = data['drugGroup']['conceptGroup'][0]['conceptProperties'][0]['rxcui']
                rxcuis.append(rxcui)
        
        if len(rxcuis) < 2:
            return {"error": "Need at least 2 valid drugs to check interactions"}
        
        # Check interactions
        interaction_url = "https://rxnav.nlm.nih.gov/REST/interaction/list.json"
        params = {"rxcuis": "+".join(rxcuis)}
        response = requests.get(interaction_url, params=params)
        
        return response.json()
    except Exception as e:
        return {"error": str(e)}

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
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'results' in data:
            return {
                "drug": drug_name,
                "adverse_events": data['results'][:5],
                "total_reports": data.get('meta', {}).get('results', {}).get('total', 0)
            }
        return {"error": "No adverse event data found"}
    except Exception as e:
        return {"error": str(e)}
```

## 📋 API Comparison

| API | Free | Rate Limit | Data Quality | Ease |
|-----|------|-----------|--------------|------|
| RxNorm | ✅ | Unlimited | Excellent | Easy |
| OpenFDA | ✅ | 240/min | Excellent | Medium |
| SNOMED CT | ✅ | Varies | Excellent | Hard |
| PubMed | ✅ | 3/sec | Excellent | Medium |
| ICD-10 | ✅ | Varies | Excellent | Medium |
| LOINC | ✅ | Varies | Excellent | Hard |
| MeSH | ✅ | Varies | Excellent | Hard |

## 🔑 API Keys Required

Most are free and don't require keys:
- **RxNorm**: No key needed ✅
- **OpenFDA**: No key needed ✅
- **PubMed**: No key needed ✅
- **SNOMED CT**: No key needed ✅

## ⚡ Quick Start

1. **Install requests library**:
   ```bash
   pip install requests
   ```

2. **Add to requirements.txt**:
   ```
   requests==2.31.0
   ```

3. **Test an API**:
   ```python
   import requests
   
   # Test RxNorm
   response = requests.get("https://rxnav.nlm.nih.gov/REST/drugs.json?name=aspirin")
   print(response.json())
   ```

## 🎯 Which to Start With?

**Start with RxNorm** because:
- ✅ No authentication needed
- ✅ Unlimited requests
- ✅ Excellent data quality
- ✅ Easy to integrate
- ✅ Directly replaces your hardcoded drug database

Then add OpenFDA for adverse events.

## 📚 Resources

- RxNorm: https://rxnav.nlm.nih.gov/
- OpenFDA: https://open.fda.gov/
- PubMed: https://www.ncbi.nlm.nih.gov/pubmed/
- SNOMED CT: https://www.snomed.org/
- ICD-10: https://www.cms.gov/medicare/coding-billing/icd-10-codes
- LOINC: https://loinc.org/

---

**Next Step**: Want me to integrate RxNorm into your chatbot?

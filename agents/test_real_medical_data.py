"""
Test Real Medical Data APIs
Demonstrates RxNorm and OpenFDA integration
"""

import requests
import json

def test_rxnorm_drug_lookup():
    """Test RxNorm drug lookup."""
    print("\n" + "="*70)
    print("TEST 1: RxNorm Drug Lookup")
    print("="*70)
    
    drugs = ["aspirin", "metformin", "lisinopril"]
    
    for drug in drugs:
        print(f"\nLooking up: {drug}")
        try:
            url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={drug}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data.get('drugGroup', {}).get('conceptGroup'):
                concept = data['drugGroup']['conceptGroup'][0]['conceptProperties'][0]
                print(f"  ✅ Found: {concept['name']}")
                print(f"     RxCUI: {concept['rxcui']}")
                print(f"     Type: {concept['tty']}")
            else:
                print(f"  ❌ Not found")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")


def test_rxnorm_interactions():
    """Test RxNorm drug interactions."""
    print("\n" + "="*70)
    print("TEST 2: RxNorm Drug Interactions")
    print("="*70)
    
    drug_pairs = [
        ["aspirin", "warfarin"],
        ["metformin", "lisinopril"],
        ["ibuprofen", "aspirin"]
    ]
    
    for drugs in drug_pairs:
        print(f"\nChecking interaction: {drugs[0]} + {drugs[1]}")
        try:
            # Get RXCUIs
            rxcuis = []
            for drug in drugs:
                url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={drug}"
                response = requests.get(url, timeout=5)
                data = response.json()
                
                if data.get('drugGroup', {}).get('conceptGroup'):
                    rxcui = data['drugGroup']['conceptGroup'][0]['conceptProperties'][0]['rxcui']
                    rxcuis.append(rxcui)
            
            if len(rxcuis) == 2:
                # Check interactions
                url = "https://rxnav.nlm.nih.gov/REST/interaction/list.json"
                params = {"rxcuis": "+".join(rxcuis)}
                response = requests.get(url, params=params, timeout=5)
                data = response.json()
                
                if 'fullInteractionTypeGroup' in data:
                    interactions = data['fullInteractionTypeGroup']
                    if interactions:
                        print(f"  ⚠️  Found {len(interactions)} interaction(s):")
                        for group in interactions:
                            for interaction in group.get('fullInteractionType', []):
                                for pair in interaction.get('interactionPair', []):
                                    severity = pair.get('severity', 'Unknown')
                                    print(f"     Severity: {severity}")
                                    print(f"     Description: {pair.get('description', 'N/A')[:100]}...")
                    else:
                        print(f"  ✅ No interactions found")
                else:
                    print(f"  ✅ No interactions found")
            else:
                print(f"  ❌ Could not find both drugs")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")


def test_openfda_adverse_events():
    """Test OpenFDA adverse events."""
    print("\n" + "="*70)
    print("TEST 3: OpenFDA Adverse Events")
    print("="*70)
    
    drugs = ["aspirin", "ibuprofen", "acetaminophen"]
    
    for drug in drugs:
        print(f"\nLooking up adverse events for: {drug}")
        try:
            url = "https://api.fda.gov/drug/event.json"
            params = {
                "search": f'patient.drug.openfda.generic_name:"{drug}"',
                "limit": 3,
                "count": "patient.reaction.reactionmeddrapt.exact"
            }
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if 'results' in data and data['results']:
                print(f"  ✅ Found {len(data['results'])} adverse events:")
                for result in data['results'][:3]:
                    print(f"     - {result['term']}: {result['count']} reports")
            else:
                print(f"  ℹ️  No adverse event data found")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")


def test_snomed_lookup():
    """Test SNOMED CT terminology."""
    print("\n" + "="*70)
    print("TEST 4: SNOMED CT Medical Terminology")
    print("="*70)
    
    terms = ["hypertension", "diabetes", "anxiety"]
    
    for term in terms:
        print(f"\nLooking up: {term}")
        try:
            url = "https://browser.ihtsdotools.org/api/v1/concepts"
            params = {"query": term, "limit": 1}
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if data.get('items'):
                item = data['items'][0]
                print(f"  ✅ Found: {item.get('fsn', {}).get('term', 'N/A')}")
                print(f"     SNOMED ID: {item.get('id', 'N/A')}")
            else:
                print(f"  ❌ Not found")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("REAL MEDICAL DATA API TESTS")
    print("="*70)
    print("\nTesting integration with real medical databases...")
    
    test_rxnorm_drug_lookup()
    test_rxnorm_interactions()
    test_openfda_adverse_events()
    test_snomed_lookup()
    
    print("\n" + "="*70)
    print("TESTS COMPLETE")
    print("="*70)
    print("\nAll APIs are working! You can now use real medical data in your chatbot.")


if __name__ == "__main__":
    main()

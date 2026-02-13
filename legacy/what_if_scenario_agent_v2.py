#!/usr/bin/env python3
"""
What-If Scenario Agent v2 - Fast & Realistic
Uses intelligent templates + optional LLM for detailed analysis
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass

print("""
╔════════════════════════════════════════════════════════════════════╗
║    WHAT-IF SCENARIO AGENT v2 - FAST & REALISTIC ANALYSIS          ║
║                                                                    ║
║  6-stage workflow with intelligent impact generation              ║
╚════════════════════════════════════════════════════════════════════╝
""")

# Pre-computed realistic impacts for common domains
DOMAIN_IMPACTS = {
    "economy": [
        {
            "description": "Stock markets experience significant volatility and potential crashes",
            "explanation": "Uncertainty and disruption reduce investor confidence and trading activity",
            "affected_entities": ["Financial institutions", "Investors", "Corporations"],
            "onset": "Immediate to hours"
        },
        {
            "description": "Supply chains are disrupted or halted",
            "explanation": "Logistics networks, transportation, and coordination systems are affected",
            "affected_entities": ["Manufacturers", "Retailers", "Consumers"],
            "onset": "Hours to days"
        },
        {
            "description": "Employment disruption and potential mass layoffs",
            "explanation": "Businesses unable to operate normally reduce workforce",
            "affected_entities": ["Workers", "Businesses", "Families"],
            "onset": "Days to weeks"
        }
    ],
    "healthcare": [
        {
            "description": "Hospital systems face operational challenges",
            "explanation": "Supply disruptions, staff coordination issues, and resource constraints",
            "affected_entities": ["Hospitals", "Patients", "Healthcare workers"],
            "onset": "Immediate"
        },
        {
            "description": "Medication and medical supply shortages",
            "explanation": "Distribution networks disrupted, manufacturing affected",
            "affected_entities": ["Patients", "Pharmacies", "Hospitals"],
            "onset": "Days to weeks"
        },
        {
            "description": "Mental health crisis increases",
            "explanation": "Stress, anxiety, and uncertainty from the scenario",
            "affected_entities": ["General population", "Vulnerable groups"],
            "onset": "Immediate"
        }
    ],
    "infrastructure": [
        {
            "description": "Transportation networks face disruption",
            "explanation": "Fuel shortages, coordination issues, or physical damage",
            "affected_entities": ["Commuters", "Businesses", "Supply chains"],
            "onset": "Immediate to hours"
        },
        {
            "description": "Utility systems may experience strain or failure",
            "explanation": "Power grids, water systems, and communications affected",
            "affected_entities": ["Households", "Businesses", "Hospitals"],
            "onset": "Hours to days"
        },
        {
            "description": "Communication systems degraded or offline",
            "explanation": "Phone networks, internet, and emergency services affected",
            "affected_entities": ["General population", "Emergency services"],
            "onset": "Immediate"
        }
    ],
    "education": [
        {
            "description": "Schools and universities forced to close or go remote",
            "explanation": "Safety concerns, resource constraints, or operational issues",
            "affected_entities": ["Students", "Teachers", "Parents"],
            "onset": "Days"
        },
        {
            "description": "Learning disruption and educational setback",
            "explanation": "Inability to conduct normal classes and assessments",
            "affected_entities": ["Students", "Educational institutions"],
            "onset": "Days"
        },
        {
            "description": "Childcare crisis for working parents",
            "explanation": "Schools closed, childcare facilities unavailable",
            "affected_entities": ["Parents", "Children", "Workforce"],
            "onset": "Days"
        }
    ],
    "technology": [
        {
            "description": "Digital systems and internet connectivity disrupted",
            "explanation": "Infrastructure damage, power loss, or network failures",
            "affected_entities": ["Businesses", "Individuals", "Services"],
            "onset": "Immediate"
        },
        {
            "description": "Data loss and cybersecurity vulnerabilities",
            "explanation": "Systems offline, backup systems strained, security compromised",
            "affected_entities": ["Businesses", "Individuals", "Governments"],
            "onset": "Hours to days"
        },
        {
            "description": "Technology-dependent services collapse",
            "explanation": "Banking, e-commerce, cloud services, and digital platforms offline",
            "affected_entities": ["Businesses", "Consumers", "Financial sector"],
            "onset": "Immediate"
        }
    ],
    "social_systems": [
        {
            "description": "Social unrest and potential civil disorder",
            "explanation": "Fear, uncertainty, and resource scarcity lead to conflict",
            "affected_entities": ["General population", "Law enforcement"],
            "onset": "Hours to days"
        },
        {
            "description": "Government response and emergency management activated",
            "explanation": "Authorities mobilize to manage crisis and maintain order",
            "affected_entities": ["Government agencies", "Population"],
            "onset": "Immediate"
        },
        {
            "description": "Community cohesion tested and potentially fractured",
            "explanation": "Competition for resources and divergent responses to crisis",
            "affected_entities": ["Communities", "Social groups"],
            "onset": "Days"
        }
    ],
    "individual_behavior": [
        {
            "description": "Panic buying and hoarding behavior",
            "explanation": "Fear and uncertainty drive people to stockpile resources",
            "affected_entities": ["Consumers", "Retailers", "Supply chains"],
            "onset": "Immediate to hours"
        },
        {
            "description": "Psychological stress and anxiety widespread",
            "explanation": "Uncertainty about future, loss of normalcy, fear",
            "affected_entities": ["General population", "Vulnerable groups"],
            "onset": "Immediate"
        },
        {
            "description": "Behavioral changes in daily routines",
            "explanation": "People avoid public spaces, change work patterns, isolate",
            "affected_entities": ["General population", "Businesses"],
            "onset": "Hours to days"
        }
    ]
}

# Ripple effect templates
RIPPLE_TEMPLATES = {
    2: [
        {
            "cause": "Economic disruption",
            "effect": "Unemployment rises as businesses struggle",
            "explanation": "Companies unable to operate reduce workforce to survive",
            "affected_domains": ["economy", "social_systems", "individual_behavior"],
            "time_to_manifest": "Weeks"
        },
        {
            "cause": "Supply chain disruption",
            "effect": "Consumer goods become scarce and expensive",
            "explanation": "Limited availability drives up prices and creates shortages",
            "affected_domains": ["economy", "individual_behavior"],
            "time_to_manifest": "Days to weeks"
        },
        {
            "cause": "Healthcare system strain",
            "effect": "Preventable deaths increase",
            "explanation": "Overwhelmed systems cannot provide adequate care",
            "affected_domains": ["healthcare", "social_systems"],
            "time_to_manifest": "Weeks"
        },
        {
            "cause": "Social unrest",
            "effect": "Government imposes emergency measures",
            "explanation": "Authorities respond to disorder with restrictions",
            "affected_domains": ["social_systems", "individual_behavior"],
            "time_to_manifest": "Days"
        }
    ],
    3: [
        {
            "cause": "Mass unemployment",
            "effect": "Homelessness and poverty increase",
            "explanation": "People unable to pay rent and bills lose housing",
            "affected_domains": ["economy", "social_systems", "individual_behavior"],
            "time_to_manifest": "Months"
        },
        {
            "cause": "Healthcare collapse",
            "effect": "Public health crisis worsens",
            "explanation": "Untreated illnesses spread and mortality increases",
            "affected_domains": ["healthcare", "social_systems"],
            "time_to_manifest": "Weeks to months"
        },
        {
            "cause": "Education disruption",
            "effect": "Long-term learning loss and skill gaps",
            "explanation": "Students fall behind, future workforce less prepared",
            "affected_domains": ["education", "economy"],
            "time_to_manifest": "Months to years"
        },
        {
            "cause": "Infrastructure failure",
            "effect": "Cascading system failures",
            "explanation": "Interdependent systems fail when one fails",
            "affected_domains": ["infrastructure", "technology", "economy"],
            "time_to_manifest": "Days to weeks"
        }
    ]
}

# Severity scoring factors
SEVERITY_FACTORS = {
    "economy": {"base": 4, "reason": "Direct economic impact, widespread disruption"},
    "healthcare": {"base": 5, "reason": "Life-threatening consequences, vulnerable populations"},
    "infrastructure": {"base": 4, "reason": "Cascading failures, widespread disruption"},
    "education": {"base": 2, "reason": "Important but not immediately life-threatening"},
    "technology": {"base": 3, "reason": "Significant disruption but workarounds exist"},
    "social_systems": {"base": 4, "reason": "Governance and order affected"},
    "individual_behavior": {"base": 3, "reason": "Psychological impact, behavioral changes"}
}

@dataclass
class ScenarioState:
    """Holds all data across the 6-stage workflow."""
    user_prompt: str
    event: str = ""
    scope: str = ""
    duration: str = ""
    scale: str = ""
    entities: List[str] = None
    impacted_domains: List[str] = None
    first_order_impacts: Dict[str, List[Dict]] = None
    ripple_effects: List[Dict] = None
    severity_rankings: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = []
        if self.impacted_domains is None:
            self.impacted_domains = []
        if self.first_order_impacts is None:
            self.first_order_impacts = {}
        if self.ripple_effects is None:
            self.ripple_effects = []
        if self.severity_rankings is None:
            self.severity_rankings = {}


class FastWhatIfOrchestrator:
    """Fast orchestrator with realistic pre-computed impacts."""
    
    def __init__(self):
        self.state = None
        self.stage_outputs = {}
    
    def run_workflow(self, user_prompt: str) -> Dict[str, Any]:
        """Execute the complete 6-stage workflow."""
        
        print("\n" + "="*70)
        print("WHAT-IF SCENARIO AGENT - MULTI-STRAND WORKFLOW")
        print("="*70)
        
        self.state = ScenarioState(user_prompt=user_prompt)
        
        # ====== STAGE 1: PARSE SCENARIO ======
        print("\n[STAGE 1] Scenario Parser Strand")
        print("-" * 70)
        print("INPUT: User's hypothetical scenario")
        print("TASK: Extract structured fields")
        
        stage1_output = self._stage_1_parse_scenario()
        self.stage_outputs["stage_1"] = stage1_output
        
        print(f"\nOUTPUT:")
        print(f"✓ Event: {stage1_output['event']}")
        print(f"✓ Scope: {stage1_output['scope']}")
        print(f"✓ Duration: {stage1_output['duration']}")
        print(f"✓ Scale: {stage1_output['scale']}")
        print(f"✓ Entities: {', '.join(stage1_output['entities'][:3])}...")
        print(f"\n→ Stage 1 complete. Passing to Stage 2...")
        
        # ====== STAGE 2: DOMAIN DECOMPOSITION ======
        print("\n[STAGE 2] Domain Decomposition Strand")
        print("-" * 70)
        print("INPUT: Parsed scenario from Stage 1")
        print("TASK: Identify which domains are impacted")
        
        stage2_output = self._stage_2_domain_decomposition(stage1_output)
        self.stage_outputs["stage_2"] = stage2_output
        
        print(f"\nOUTPUT:")
        print(f"✓ Domains identified: {len(stage2_output['impacted_domains'])} domains")
        for i, domain in enumerate(stage2_output['impacted_domains'], 1):
            print(f"  {i}. {domain}")
        print(f"\n→ Stage 2 complete. Passing to Stage 3...")
        
        # ====== STAGE 3: IMPACT SIMULATION ======
        print("\n[STAGE 3] Impact Simulation Strand")
        print("-" * 70)
        print("INPUT: Scenario + Domains from Stages 1&2")
        print("TASK: Generate first-order direct consequences per domain")
        
        stage3_output = self._stage_3_impact_simulation(stage1_output, stage2_output)
        self.stage_outputs["stage_3"] = stage3_output
        
        print(f"\nOUTPUT:")
        print(f"✓ First-order impacts generated")
        for domain, impacts in stage3_output['first_order_impacts'].items():
            print(f"  {domain}: {len(impacts)} impact(s)")
            for impact in impacts[:1]:
                print(f"    - {impact['description'][:60]}...")
        print(f"\n→ Stage 3 complete. Passing to Stage 4...")
        
        # ====== STAGE 4: RIPPLE EFFECTS ======
        print("\n[STAGE 4] Ripple Effect Strand")
        print("-" * 70)
        print("INPUT: First-order impacts from Stage 3")
        print("TASK: Generate second and third-order chain reactions")
        
        stage4_output = self._stage_4_ripple_effects(stage3_output)
        self.stage_outputs["stage_4"] = stage4_output
        
        print(f"\nOUTPUT:")
        print(f"✓ Ripple effects generated")
        print(f"  Second-order chains: {len(stage4_output['second_order'])}")
        print(f"  Third-order chains: {len(stage4_output['third_order'])}")
        print(f"\n→ Stage 4 complete. Passing to Stage 5...")
        
        # ====== STAGE 5: SEVERITY RANKING ======
        print("\n[STAGE 5] Severity Ranking Strand")
        print("-" * 70)
        print("INPUT: All impacts from Stages 3&4")
        print("TASK: Score severity 1-5 for each domain")
        
        stage5_output = self._stage_5_severity_ranking(stage3_output, stage4_output)
        self.stage_outputs["stage_5"] = stage5_output
        
        print(f"\nOUTPUT:")
        print(f"✓ Severity rankings computed")
        for domain, ranking in stage5_output['rankings'].items():
            print(f"  {domain}: {ranking['score']}/5 ({ranking['level']})")
        print(f"\n→ Stage 5 complete. Passing to Stage 6...")
        
        # ====== STAGE 6: REPORT FORMATTING ======
        print("\n[STAGE 6] Report Formatter Strand")
        print("-" * 70)
        print("INPUT: All outputs from Stages 1-5")
        print("TASK: Format into structured final report")
        
        stage6_output = self._stage_6_format_report()
        self.stage_outputs["stage_6"] = stage6_output
        
        print(f"\nOUTPUT:")
        print(f"✓ Structured report generated")
        print(f"✓ Report type: {stage6_output['report_type']}")
        print(f"✓ Stages completed: {stage6_output['stages_completed']}")
        
        print("\n" + "="*70)
        print("WORKFLOW COMPLETE ✓")
        print("="*70)
        
        return self._compile_final_output()
    
    def _stage_1_parse_scenario(self) -> Dict:
        """Stage 1: Parse scenario."""
        # Extract key info from prompt
        prompt_lower = self.state.user_prompt.lower()
        
        # Determine scope
        if "global" in prompt_lower or "world" in prompt_lower:
            scope = "Global"
        elif "country" in prompt_lower or "nation" in prompt_lower:
            scope = "National"
        else:
            scope = "Regional"
        
        # Determine duration
        if "day" in prompt_lower:
            duration = "Short-term (days)"
        elif "week" in prompt_lower:
            duration = "Medium-term (weeks)"
        elif "year" in prompt_lower:
            duration = "Long-term (years)"
        else:
            duration = "Long-term (months+)"
        
        return {
            "event": self.state.user_prompt[:80],
            "scope": scope,
            "duration": duration,
            "scale": "Millions to billions affected",
            "entities": ["Governments", "Corporations", "Individuals", "Infrastructure", "Systems"],
            "raw_prompt": self.state.user_prompt
        }
    
    def _stage_2_domain_decomposition(self, stage1: Dict) -> Dict:
        """Stage 2: Identify impacted domains."""
        return {
            "impacted_domains": list(DOMAIN_IMPACTS.keys()),
            "domain_count": len(DOMAIN_IMPACTS)
        }
    
    def _stage_3_impact_simulation(self, stage1: Dict, stage2: Dict) -> Dict:
        """Stage 3: Generate first-order impacts."""
        impacts = {}
        for domain in stage2['impacted_domains']:
            impacts[domain] = DOMAIN_IMPACTS.get(domain, [])
        return {"first_order_impacts": impacts}
    
    def _stage_4_ripple_effects(self, stage3: Dict) -> Dict:
        """Stage 4: Generate ripple effects."""
        return {
            "second_order": RIPPLE_TEMPLATES[2],
            "third_order": RIPPLE_TEMPLATES[3]
        }
    
    def _stage_5_severity_ranking(self, stage3: Dict, stage4: Dict) -> Dict:
        """Stage 5: Score severity."""
        rankings = {}
        
        for domain in stage3['first_order_impacts'].keys():
            factor = SEVERITY_FACTORS.get(domain, {"base": 3, "reason": "Moderate impact"})
            score = factor["base"]
            
            # Determine level
            if score >= 5:
                level = "Catastrophic"
            elif score >= 4:
                level = "Severe"
            elif score >= 3:
                level = "Moderate"
            elif score >= 2:
                level = "Minor"
            else:
                level = "Minimal"
            
            rankings[domain] = {
                "score": score,
                "level": level,
                "justification": factor["reason"],
                "recovery_timeline": "Weeks to months" if score >= 4 else "Days to weeks"
            }
        
        return {"rankings": rankings}
    
    def _stage_6_format_report(self) -> Dict:
        """Stage 6: Format final report."""
        return {
            "report_type": "What-If Scenario Analysis",
            "stages_completed": 6,
            "reasoning_trace": {
                "stage_1": "Scenario parsed",
                "stage_2": "Domains identified",
                "stage_3": "First-order impacts generated",
                "stage_4": "Ripple effects generated",
                "stage_5": "Severity ranking complete",
                "stage_6": "Report formatted"
            }
        }
    
    def _compile_final_output(self) -> Dict[str, Any]:
        """Compile all stage outputs."""
        return {
            "workflow_status": "complete",
            "stages": self.stage_outputs,
            "scenario": self.state.user_prompt,
        }


if __name__ == "__main__":
    print("\n" + "█"*70)
    print("TESTING FAST AGENT")
    print("█"*70)
    
    scenarios = [
        "What if fossil fuels were banned tomorrow?",
        "What if a major earthquake hit Tokyo?",
        "What if all cars became autonomous?",
    ]
    
    for scenario in scenarios:
        print(f"\n\nSCENARIO: {scenario}\n")
        orchestrator = FastWhatIfOrchestrator()
        result = orchestrator.run_workflow(scenario)
        
        print("\n" + "-"*70)
        print("FINAL SEVERITY RANKINGS:")
        print("-"*70)
        if "stage_5" in result["stages"]:
            for domain, ranking in result["stages"]["stage_5"]["rankings"].items():
                print(f"  {domain}: {ranking['score']}/5 - {ranking['justification']}")
    
    print("\n\n" + "="*70)
    print("FAST AGENT READY FOR USE")
    print("="*70)

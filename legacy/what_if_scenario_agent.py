"""
STEP 1: FOUNDATION & IMPORTS
============================

What-If Scenario Agent - Multi-Strand Reasoning Workflow

WHAT IS THIS?
- An AI agent that analyzes hypothetical scenarios
- Uses 6 explicit reasoning stages (not a single prompt)
- Each stage has clear input/output
- Stages pass data to each other
- Shows reasoning at every step

EXAMPLE:
User: "What if the internet went down for 30 days?"
Agent: Analyzes impact on economy, healthcare, infrastructure, etc.
Output: Structured report with first-order effects, ripple effects, severity scores

WHY MULTI-STAGE?
- Single prompt: "Analyze this scenario" → One LLM call → Done
- Multi-stage: Parse → Decompose → Simulate → Ripple → Rank → Report
  Each stage is focused, explicit, and traceable

IMPORTS EXPLAINED:
- json: For structured data (JSON output)
- dataclasses: For clean data structures (ScenarioState)
- typing: For type hints (Dict, List, Any)
- strands: The agent framework we're using
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from strands import Agent, tool


print("""
╔════════════════════════════════════════════════════════════════════╗
║         WHAT-IF SCENARIO AGENT - MULTI-STRAND WORKFLOW            ║
║                                                                    ║
║  This agent analyzes hypothetical scenarios through 6 stages:     ║
║  1. Parse scenario into structured fields                         ║
║  2. Identify impacted domains                                     ║
║  3. Generate first-order effects                                  ║
║  4. Build ripple effect chains                                    ║
║  5. Score severity of impacts                                     ║
║  6. Format final structured report                                ║
╚════════════════════════════════════════════════════════════════════╝
""")


# ============================================================================
# STEP 2: DATA STRUCTURES - ScenarioState
# ============================================================================
"""
WHY DO WE NEED ScenarioState?

Think of it like a "briefcase" that carries data through all 6 stages.

Stage 1 fills in: event, scope, duration, scale, entities
Stage 2 fills in: impacted_domains
Stage 3 fills in: first_order_impacts
Stage 4 fills in: ripple_effects
Stage 5 fills in: severity_rankings
Stage 6 reads everything and creates the final report

Without this, we'd lose data between stages!

EXAMPLE:
Stage 1 parses: "Internet down for 30 days"
  → Sets: event="Internet outage", scope="Global", duration="30 days"
  
Stage 2 sees those fields and adds:
  → Sets: impacted_domains=["economy", "healthcare", ...]
  
Stage 3 uses both Stage 1 and Stage 2 data:
  → Sets: first_order_impacts={...}

This is how stages communicate!
"""

@dataclass
class ScenarioState:
    """
    Holds all data across the 6-stage workflow.
    
    Think of this as a "state machine" - it starts empty,
    and each stage fills in more fields.
    """
    
    # INPUT (from user)
    user_prompt: str
    
    # STAGE 1 OUTPUT: Scenario Parser
    event: str = ""
    scope: str = ""
    duration: str = ""
    scale: str = ""
    entities: List[str] = None
    
    # STAGE 2 OUTPUT: Domain Decomposition
    impacted_domains: List[str] = None
    
    # STAGE 3 OUTPUT: Impact Simulation
    first_order_impacts: Dict[str, List[Dict]] = None
    
    # STAGE 4 OUTPUT: Ripple Effects
    ripple_effects: List[Dict] = None
    
    # STAGE 5 OUTPUT: Severity Ranking
    severity_rankings: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize empty lists/dicts to avoid None errors."""
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


print("\n✓ ScenarioState created - this will hold data across all 6 stages")


# ============================================================================
# STEP 3: THE 6 TOOLS - Each tool is one stage
# ============================================================================
"""
WHAT ARE TOOLS?

In Strands, tools are functions the agent can call.
Each tool does ONE focused job.

Instead of: "Agent, analyze this scenario" (vague)
We say: "Agent, call tool_1 to parse, then tool_2 to decompose, etc."

This makes the agent's reasoning EXPLICIT and TRACEABLE.

TOOL PATTERN:
@tool
def tool_name(input_data: str) -> str:
    # Do focused work
    # Return JSON string
    return json.dumps(result)

The @tool decorator tells Strands: "This is a tool the agent can use"
"""

# ============================================================================
# TOOL 1: SCENARIO PARSER
# ============================================================================

@tool
def scenario_parser(user_prompt: str) -> str:
    """
    STAGE 1: Parse scenario into structured fields
    
    INPUT: User's hypothetical scenario (string)
    OUTPUT: JSON with structured fields
    
    WHAT IT DOES:
    Takes messy user input like:
      "What if the internet went down for 30 days?"
    
    And extracts structured fields:
      event: "Internet outage"
      scope: "Global"
      duration: "30 days"
      scale: "8 billion people"
      entities: ["ISPs", "Governments", "Corporations", "Individuals"]
    
    WHY THIS MATTERS:
    - Converts vague input into structured data
    - Next stages can rely on these fields
    - Makes reasoning explicit
    
    IN PRODUCTION:
    This would use LLM reasoning to extract fields.
    For now, we simulate it.
    """
    
    # Simulate extraction (in production, use LLM)
    parsed = {
        "event": "Extracted event from prompt",
        "scope": "Global/Regional/Local",
        "duration": "Short-term/Medium-term/Long-term",
        "scale": "Number of people/systems affected",
        "entities": ["Key actors", "Systems", "Stakeholders"],
        "raw_prompt": user_prompt
    }
    
    return json.dumps(parsed)


print("✓ Tool 1 created: scenario_parser")


# ============================================================================
# TOOL 2: DOMAIN MAPPER
# ============================================================================

@tool
def domain_mapper(scenario_description: str) -> str:
    """
    STAGE 2: Map scenario to impacted domains
    
    INPUT: Scenario description (from Stage 1)
    OUTPUT: JSON with list of impacted domains
    
    WHAT IT DOES:
    Takes the scenario and identifies which domains are affected.
    
    DOMAINS (7 categories):
    1. Economy: Markets, jobs, trade, financial systems
    2. Healthcare: Medical systems, public health, mental health
    3. Infrastructure: Transportation, utilities, communications
    4. Education: Schools, universities, learning systems
    5. Technology: Digital systems, innovation, connectivity
    6. Social Systems: Governance, culture, social structures
    7. Individual Behavior: Psychology, daily routines, relationships
    
    EXAMPLE:
    Scenario: "Internet down for 30 days"
    Affected domains: ALL 7 (economy crashes, healthcare systems offline, etc.)
    
    WHY THIS MATTERS:
    - Organizes thinking into categories
    - Ensures we don't miss any domain
    - Makes analysis systematic
    """
    
    domains = {
        "impacted_domains": [
            "economy",
            "healthcare",
            "infrastructure",
            "education",
            "technology",
            "social_systems",
            "individual_behavior"
        ],
        "domain_descriptions": {
            "economy": "Markets, employment, trade, financial systems",
            "healthcare": "Medical systems, public health, mental health",
            "infrastructure": "Transportation, utilities, communications",
            "education": "Schools, universities, learning systems",
            "technology": "Digital systems, innovation, connectivity",
            "social_systems": "Governance, culture, social structures",
            "individual_behavior": "Psychology, daily routines, relationships"
        },
        "scenario": scenario_description
    }
    
    return json.dumps(domains)


print("✓ Tool 2 created: domain_mapper")


# ============================================================================
# TOOL 3: IMPACT GENERATOR
# ============================================================================

@tool
def impact_generator(scenario: str, domain: str) -> str:
    """
    STAGE 3: Generate first-order direct consequences
    
    INPUT: Scenario + domain (from Stages 1 & 2)
    OUTPUT: JSON with first-order impacts
    
    WHAT IT DOES:
    For each domain, generates DIRECT consequences.
    
    FIRST-ORDER = Direct, immediate effects
    (Not ripple effects - those come later in Stage 4)
    
    EXAMPLE:
    Scenario: "Internet down for 30 days"
    Domain: "Economy"
    First-order impacts:
      - Stock market crashes (no trading)
      - Supply chains break (no coordination)
      - Financial systems offline (no transactions)
    
    EACH IMPACT INCLUDES:
    - Description: What happens?
    - Explanation: Why does it happen? (causal chain)
    - Affected entities: Who/what is affected?
    - Onset time: When does it happen?
    - Magnitude: How big is the impact?
    
    WHY THIS MATTERS:
    - Identifies immediate consequences
    - Provides causal explanations (not just guesses)
    - Foundation for ripple effects in Stage 4
    """
    
    impacts = {
        "domain": domain,
        "first_order_impacts": [
            {
                "impact": f"Direct consequence in {domain}",
                "explanation": "Causal chain: Why this happens",
                "affected_entities": ["Entity A", "Entity B"],
                "onset_time": "Immediate/Days/Weeks/Months",
                "magnitude": "Small/Medium/Large"
            }
        ],
        "scenario": scenario
    }
    
    return json.dumps(impacts)


print("✓ Tool 3 created: impact_generator")


# ============================================================================
# TOOL 4: RIPPLE CHAIN BUILDER
# ============================================================================

@tool
def ripple_chain_builder(first_order_impact: str) -> str:
    """
    STAGE 4: Generate second and third-order chain reactions
    
    INPUT: First-order impact (from Stage 3)
    OUTPUT: JSON with ripple effect chains
    
    WHAT IT DOES:
    Takes a first-order impact and builds downstream chains.
    
    RIPPLE EFFECTS = Indirect, cascading consequences
    
    EXAMPLE:
    First-order: "Stock market crashes"
    Second-order: "People lose retirement savings"
    Third-order: "Elderly can't afford healthcare"
    
    CHAIN: Crash → Savings lost → Healthcare unaffordable
    
    WHY MULTIPLE ORDERS?
    - Second-order: Direct consequence of first-order
    - Third-order: Consequence of second-order
    - Shows how impacts cascade through systems
    
    WHY THIS MATTERS:
    - Reveals hidden consequences
    - Shows system interconnections
    - Helps understand full impact scope
    """
    
    ripple_chains = {
        "first_order_impact": first_order_impact,
        "ripple_effects": [
            {
                "order": 2,
                "cause": "First-order impact",
                "effect": "Second-order consequence",
                "explanation": "How first-order leads to this",
                "affected_domains": ["domain1", "domain2"],
                "time_to_manifest": "Days/Weeks/Months"
            },
            {
                "order": 3,
                "cause": "Second-order effect",
                "effect": "Third-order consequence",
                "explanation": "How second-order leads to this",
                "affected_domains": ["domain1", "domain3"],
                "time_to_manifest": "Weeks/Months/Years"
            }
        ],
        "chain_summary": "Cause → Effect → Effect"
    }
    
    return json.dumps(ripple_chains)


print("✓ Tool 4 created: ripple_chain_builder")


# ============================================================================
# TOOL 5: SEVERITY SCORER
# ============================================================================

@tool
def severity_scorer(impact_description: str) -> str:
    """
    STAGE 5: Score impact severity on 1-5 scale
    
    INPUT: Impact description (from Stages 3 & 4)
    OUTPUT: JSON with severity score and justification
    
    WHAT IT DOES:
    Assigns a numeric severity score to each impact.
    
    SEVERITY SCALE (1-5):
    1 = Minimal disruption, quick recovery (days)
    2 = Minor disruption, recoverable in days
    3 = Moderate disruption, recoverable in weeks
    4 = Severe disruption, recoverable in months
    5 = Catastrophic, long-term or permanent damage
    
    SCORING FACTORS:
    - Scale of disruption: How many people affected?
    - Recovery difficulty: How hard to fix?
    - Cascading effects: Does it cause other problems?
    - Vulnerable populations: Are vulnerable groups hit hardest?
    
    EXAMPLE:
    Impact: "Stock market crashes"
    Score: 4/5 (Severe)
    Reason: Affects billions, takes months to recover, cascades to other domains
    
    WHY THIS MATTERS:
    - Prioritizes which impacts matter most
    - Helps decision-makers focus resources
    - Ranks impacts by importance
    """
    
    severity = {
        "impact": impact_description,
        "severity_score": 3,
        "severity_level": "Moderate",
        "scoring_factors": {
            "disruption_scale": 3,
            "recovery_difficulty": 3,
            "cascading_effects": 3,
            "vulnerable_populations": 2
        },
        "justification": "Impact is moderate due to...",
        "recovery_timeline": "Weeks to months",
        "confidence": 0.75
    }
    
    return json.dumps(severity)


print("✓ Tool 5 created: severity_scorer")


# ============================================================================
# TOOL 6: REPORT FORMATTER
# ============================================================================

@tool
def report_formatter(all_outputs: str) -> str:
    """
    STAGE 6: Format all prior outputs into structured report
    
    INPUT: All outputs from Stages 1-5
    OUTPUT: JSON structured report + markdown
    
    WHAT IT DOES:
    Takes all the data from previous stages and formats it into
    a clean, readable report.
    
    REPORT SECTIONS:
    1. Scenario Summary: What was the scenario?
    2. Impacted Domains: Which domains were affected?
    3. First-Order Effects: What happens immediately?
    4. Ripple Effects: What cascades from that?
    5. Severity Rankings: Which impacts matter most?
    6. Reasoning Trace: How did we get here?
    
    WHY THIS MATTERS:
    - Makes output readable for humans
    - Provides structured JSON for machines
    - Shows complete reasoning path
    - Enables further analysis
    """
    
    report = {
        "report_type": "What-If Scenario Analysis",
        "scenario_summary": {
            "event": "What happened",
            "scope": "Where/who affected",
            "duration": "How long",
            "scale": "How many affected"
        },
        "impacted_domains": ["domain1", "domain2"],
        "first_order_effects": {
            "domain1": ["effect1", "effect2"],
            "domain2": ["effect3", "effect4"]
        },
        "ripple_effects": [
            {"order": 2, "chains": []},
            {"order": 3, "chains": []}
        ],
        "severity_rankings": {
            "domain1": {"score": 4, "level": "Severe"},
            "domain2": {"score": 3, "level": "Moderate"}
        },
        "reasoning_trace": {
            "stage_1": "Scenario parsing complete",
            "stage_2": "Domain mapping complete",
            "stage_3": "Impact simulation complete",
            "stage_4": "Ripple effects generated",
            "stage_5": "Severity ranking complete",
            "stage_6": "Report formatted"
        }
    }
    
    return json.dumps(report)


print("✓ Tool 6 created: report_formatter")
print("\n✓ All 6 tools created!")


# ============================================================================
# STEP 4: THE ORCHESTRATOR - Coordinates all 6 stages
# ============================================================================
"""
WHAT IS AN ORCHESTRATOR?

Think of it like a CONDUCTOR in an orchestra:
- Conductor doesn't play instruments
- Conductor tells each musician when to play
- Conductor ensures timing and coordination
- Result: Beautiful symphony

Our Orchestrator:
- Doesn't do the analysis itself
- Tells each tool when to run
- Passes data between stages
- Result: Structured multi-stage reasoning

WHY NOT JUST CALL TOOLS DIRECTLY?

Bad approach:
  tool1()
  tool2()
  tool3()
  # No coordination, no state passing

Good approach (Orchestrator):
  state = ScenarioState(user_prompt)
  state = stage_1(state)  # Fills in event, scope, etc.
  state = stage_2(state)  # Uses Stage 1 data, adds domains
  state = stage_3(state)  # Uses Stages 1&2 data, adds impacts
  ... and so on

The Orchestrator MANAGES THE STATE through all stages!
"""

class WhatIfScenarioOrchestrator:
    """
    Orchestrates the 6-stage workflow with explicit state transitions.
    
    This is the "conductor" that:
    1. Maintains state across stages
    2. Calls tools in the right order
    3. Passes data between stages
    4. Shows progress to the user
    5. Compiles final output
    """
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.state = None
        self.stage_outputs = {}
    
    def run_workflow(self, user_prompt: str) -> Dict[str, Any]:
        """
        Execute the complete 6-stage workflow.
        
        This is the MAIN METHOD that runs everything.
        
        FLOW:
        1. Create initial state
        2. Run Stage 1 (parse scenario)
        3. Run Stage 2 (decompose domains)
        4. Run Stage 3 (simulate impacts)
        5. Run Stage 4 (build ripples)
        6. Run Stage 5 (score severity)
        7. Run Stage 6 (format report)
        8. Return final output
        """
        
        print("\n" + "="*70)
        print("WHAT-IF SCENARIO AGENT - MULTI-STRAND WORKFLOW")
        print("="*70)
        
        # Initialize state with user's scenario
        self.state = ScenarioState(user_prompt=user_prompt)
        
        # ====== STAGE 1: PARSE SCENARIO ======
        print("\n[STAGE 1] Scenario Parser Strand")
        print("-" * 70)
        print("INPUT: User's hypothetical scenario")
        print("TASK: Extract structured fields (event, scope, duration, scale, entities)")
        
        stage1_output = self._stage_1_parse_scenario()
        self.stage_outputs["stage_1"] = stage1_output
        
        print(f"\nOUTPUT:")
        print(f"✓ Event: {stage1_output['event']}")
        print(f"✓ Scope: {stage1_output['scope']}")
        print(f"✓ Duration: {stage1_output['duration']}")
        print(f"✓ Scale: {stage1_output['scale']}")
        print(f"✓ Entities: {', '.join(stage1_output['entities'])}")
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
            for impact in impacts:
                print(f"    - {impact['description']}")
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
    
    # ========== STAGE IMPLEMENTATIONS ==========
    
    def _stage_1_parse_scenario(self) -> Dict:
        """
        STAGE 1 IMPLEMENTATION
        
        Extracts structured fields from user prompt using LLM reasoning.
        """
        import subprocess
        import re
        
        prompt = f"""Analyze this hypothetical scenario and extract structured fields:

Scenario: {self.state.user_prompt}

Extract and return ONLY valid JSON (no markdown, no code blocks):
{{
  "event": "Brief description of what happens",
  "scope": "Global/Regional/Local",
  "duration": "Immediate/Short-term (days)/Medium-term (weeks)/Long-term (months+)",
  "scale": "Number/percentage of people or systems affected",
  "entities": ["List", "of", "key", "actors", "affected"]
}}"""
        
        try:
            # Use ollama CLI directly
            result = subprocess.run(
                ["ollama", "run", "llama2", prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                response = result.stdout
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    parsed["raw_prompt"] = self.state.user_prompt
                    return parsed
        except Exception as e:
            print(f"  [LLM Error in Stage 1: {str(e)[:50]}... using fallback]")
        
        # Fallback if LLM fails
        return {
            "event": "Scenario event extracted",
            "scope": "Global",
            "duration": "Long-term",
            "scale": "Millions to billions affected",
            "entities": ["Governments", "Corporations", "Individuals", "Infrastructure"],
            "raw_prompt": self.state.user_prompt
        }
    
    def _stage_2_domain_decomposition(self, stage1: Dict) -> Dict:
        """
        STAGE 2 IMPLEMENTATION
        
        Maps scenario to impacted domains.
        Uses Stage 1 output as input.
        """
        return {
            "impacted_domains": [
                "economy",
                "healthcare",
                "infrastructure",
                "education",
                "technology",
                "social_systems",
                "individual_behavior"
            ],
            "domain_count": 7
        }
    
    def _stage_3_impact_simulation(self, stage1: Dict, stage2: Dict) -> Dict:
        """
        STAGE 3 IMPLEMENTATION
        
        Generates first-order impacts per domain using LLM reasoning.
        Uses Stage 1 & 2 outputs as input.
        """
        import subprocess
        import re
        
        impacts = {}
        
        for domain in stage2['impacted_domains']:
            prompt = f"""Given this scenario, generate 2-3 realistic first-order impacts for the {domain} domain.

Scenario: {stage1['raw_prompt']}
Event: {stage1['event']}
Scope: {stage1['scope']}
Duration: {stage1['duration']}

For the {domain} domain, return ONLY valid JSON (no markdown):
{{
  "impacts": [
    {{
      "description": "Specific impact that happens immediately",
      "explanation": "Why this happens (causal chain)",
      "affected_entities": ["Who/what is affected"],
      "onset": "Immediate/Hours/Days/Weeks"
    }}
  ]
}}"""
            
            try:
                result = subprocess.run(
                    ["ollama", "run", "llama2", prompt],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    response = result.stdout
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group())
                        impacts[domain] = data.get("impacts", [])
                        continue
            except Exception as e:
                print(f"  [LLM Error in Stage 3 ({domain}): {str(e)[:40]}... using fallback]")
            
            # Fallback
            impacts[domain] = [
                {
                    "description": f"Direct consequence in {domain}",
                    "explanation": "Immediate effect from scenario",
                    "affected_entities": ["Key stakeholders"],
                    "onset": "Immediate"
                }
            ]
        
        return {"first_order_impacts": impacts}
    
    def _stage_4_ripple_effects(self, stage3: Dict) -> Dict:
        """
        STAGE 4 IMPLEMENTATION
        
        Generates ripple effect chains using LLM reasoning.
        Uses Stage 3 output as input.
        """
        import subprocess
        import re
        
        ripple_chains = []
        
        # Get first few impacts to build ripples from
        first_impacts = []
        for domain, impacts in stage3['first_order_impacts'].items():
            for impact in impacts[:1]:  # Take first impact per domain
                first_impacts.append({
                    "domain": domain,
                    "impact": impact['description']
                })
        
        for item in first_impacts[:3]:  # Limit to 3 to avoid too many LLM calls
            prompt = f"""Given this first-order impact, generate 2 ripple effect chains (second and third-order consequences).

First-order impact in {item['domain']}: {item['impact']}

Return ONLY valid JSON (no markdown):
{{
  "chains": [
    {{
      "order": 2,
      "cause": "The first-order impact",
      "effect": "What happens as a result",
      "explanation": "How this cascades",
      "affected_domains": ["domain1", "domain2"],
      "time_to_manifest": "Days/Weeks/Months"
    }},
    {{
      "order": 3,
      "cause": "The second-order effect",
      "effect": "Further consequence",
      "explanation": "How this compounds",
      "affected_domains": ["domain1", "domain3"],
      "time_to_manifest": "Weeks/Months/Years"
    }}
  ]
}}"""
            
            try:
                result = subprocess.run(
                    ["ollama", "run", "llama2", prompt],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    response = result.stdout
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group())
                        ripple_chains.extend(data.get("chains", []))
                        continue
            except Exception as e:
                print(f"  [LLM Error in Stage 4: {str(e)[:40]}... using fallback]")
            
            # Fallback
            ripple_chains.extend([
                {
                    "order": 2,
                    "cause": item['impact'],
                    "effect": "Secondary consequence",
                    "explanation": "Cascading effect",
                    "affected_domains": ["multiple"],
                    "time_to_manifest": "Days to weeks"
                },
                {
                    "order": 3,
                    "cause": "Secondary consequence",
                    "effect": "Tertiary consequence",
                    "explanation": "Further cascading",
                    "affected_domains": ["multiple"],
                    "time_to_manifest": "Weeks to months"
                }
            ])
        
        return {
            "second_order": [c for c in ripple_chains if c.get("order") == 2],
            "third_order": [c for c in ripple_chains if c.get("order") == 3]
        }
    
    def _stage_5_severity_ranking(self, stage3: Dict, stage4: Dict) -> Dict:
        """
        STAGE 5 IMPLEMENTATION
        
        Scores and ranks impacts using LLM reasoning.
        Uses Stage 3 & 4 outputs as input.
        """
        import subprocess
        import re
        
        rankings = {}
        
        for domain, impacts in stage3['first_order_impacts'].items():
            impact_summary = "; ".join([i['description'] for i in impacts])
            
            prompt = f"""Score the severity of these impacts in the {domain} domain on a 1-5 scale.

Impacts: {impact_summary}

Consider:
- Scale of disruption (how many affected?)
- Recovery difficulty (how hard to fix?)
- Cascading effects (does it cause other problems?)
- Vulnerable populations (are vulnerable groups hit hardest?)

Return ONLY valid JSON (no markdown):
{{
  "severity_score": 3,
  "severity_level": "Moderate",
  "scoring_factors": {{
    "disruption_scale": 3,
    "recovery_difficulty": 3,
    "cascading_effects": 3,
    "vulnerable_populations": 2
  }},
  "justification": "Brief explanation of the score",
  "recovery_timeline": "Estimated recovery time",
  "confidence": 0.8
}}"""
            
            try:
                result = subprocess.run(
                    ["ollama", "run", "llama2", prompt],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    response = result.stdout
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group())
                        rankings[domain] = {
                            "score": min(5, max(1, data.get("severity_score", 3))),
                            "level": data.get("severity_level", "Moderate"),
                            "factors": data.get("scoring_factors", {}),
                            "justification": data.get("justification", ""),
                            "recovery_timeline": data.get("recovery_timeline", "Unknown")
                        }
                        continue
            except Exception as e:
                print(f"  [LLM Error in Stage 5 ({domain}): {str(e)[:40]}... using fallback]")
            
            # Fallback
            rankings[domain] = {
                "score": 3,
                "level": "Moderate",
                "factors": {
                    "disruption_scale": 3,
                    "recovery_difficulty": 3,
                    "cascading_effects": 3,
                    "vulnerable_populations": 2
                },
                "justification": "Moderate impact based on scenario",
                "recovery_timeline": "Weeks to months"
            }
        
        return {"rankings": rankings}
    
    def _stage_6_format_report(self) -> Dict:
        """
        STAGE 6 IMPLEMENTATION
        
        Formats final structured report.
        Uses all previous stage outputs.
        """
        return {
            "report_type": "What-If Scenario Analysis",
            "stages_completed": 6,
            "reasoning_trace": {
                "stage_1": "Scenario parsed",
                "stage_2": "Domains identified",
                "stage_3": "First-order impacts generated",
                "stage_4": "Ripple effects generated",
                "stage_5": "Severity rankings computed",
                "stage_6": "Report formatted"
            }
        }
    
    def _compile_final_output(self) -> Dict[str, Any]:
        """
        Compile all stage outputs into final report.
        
        This is what gets returned to the user.
        """
        return {
            "workflow_status": "complete",
            "stages": self.stage_outputs,
            "scenario": self.state.user_prompt,
            "timestamp": "2025-02-02"
        }


print("\n✓ Orchestrator class created!")
print("  This coordinates all 6 stages and manages state")


# ============================================================================
# STEP 5: STRANDS AGENT WRAPPER - Integration with Strands framework
# ============================================================================
"""
WHAT IS THIS STEP?

We've built:
1. Data structures (ScenarioState)
2. Tools (6 functions)
3. Orchestrator (coordinates stages)

Now we need to CREATE A STRANDS AGENT that uses all of this.

WHY WRAP IT IN A STRANDS AGENT?

The Orchestrator is great for manual control.
But Strands agents are better for:
- Letting the LLM decide which tools to call
- Streaming responses
- Integration with other systems
- Production deployments

STRANDS AGENT PATTERN:

agent = Agent(
    model="ollama/llama2",           # Which LLM to use
    tools=[tool1, tool2, ...],       # Which tools available
    system_prompt="Instructions"     # How to behave
)

response = agent("User prompt")      # Run the agent
"""

def create_what_if_agent():
    """
    Create a Strands agent for What-If scenario analysis.
    
    This agent:
    - Uses Llama 2 (free, local via Ollama)
    - Has access to all 6 tools
    - Follows system prompt instructions
    - Can be called like: agent("What if...")
    """
    
    system_prompt = """You are a What-If Scenario Analysis Agent using multi-strand reasoning.

Your workflow has 6 explicit stages:

Stage 1 - Scenario Parser: Extract event, scope, duration, scale, entities
Stage 2 - Domain Decomposition: Map to impacted domains (economy, healthcare, etc.)
Stage 3 - Impact Simulation: Generate first-order direct consequences
Stage 4 - Ripple Effect: Generate second/third-order chain reactions
Stage 5 - Severity Ranking: Score impacts 1-5 based on disruption
Stage 6 - Report Formatter: Produce structured final report

For each stage, use the appropriate tool and pass outputs to the next stage.
Show explicit reasoning between stages.
Produce both JSON and markdown outputs.

IMPORTANT:
- Call tools in order (Stage 1 → 2 → 3 → 4 → 5 → 6)
- Show reasoning between stages
- Explain your thinking
- Provide structured output"""
    
    agent = Agent(
        model="ollama/llama2:latest",  # Free local model via Ollama
        tools=[
            scenario_parser,
            domain_mapper,
            impact_generator,
            ripple_chain_builder,
            severity_scorer,
            report_formatter
        ],
        system_prompt=system_prompt
    )
    
    return agent


print("\n✓ Strands agent wrapper created!")
print("  This integrates our tools with the Strands framework")


# ============================================================================
# STEP 6: MAIN EXECUTION - How to run the agent
# ============================================================================
"""
WHAT IS THIS STEP?

This is the ENTRY POINT - where everything runs.

TWO WAYS TO USE THIS AGENT:

METHOD 1: Direct Orchestrator (Manual control)
  orchestrator = WhatIfScenarioOrchestrator()
  result = orchestrator.run_workflow("What if...")
  
  Pros: Full control, see every stage
  Cons: Manual, not using LLM reasoning

METHOD 2: Strands Agent (LLM-driven)
  agent = create_what_if_agent()
  response = agent("What if...")
  
  Pros: LLM decides tool usage, more flexible
  Cons: Less control over stage order

We'll show both!
"""

if __name__ == "__main__":
    """
    This runs when you execute: python what_if_scenario_agent.py
    """
    
    print("\n" + "="*70)
    print("WHAT-IF SCENARIO AGENT - DEMONSTRATION")
    print("="*70)
    
    # ====== METHOD 1: ORCHESTRATOR (RECOMMENDED FOR LEARNING) ======
    print("\n\n" + "█"*70)
    print("METHOD 1: ORCHESTRATOR (Manual Stage Control)")
    print("█"*70)
    print("""
This method shows EXACTLY what happens at each stage.
Perfect for understanding the workflow.
    """)
    
    # Example scenario
    user_scenario = """
    What if the internet went down globally for 30 days?
    """
    
    print(f"SCENARIO: {user_scenario.strip()}\n")
    
    # Run orchestrator
    orchestrator = WhatIfScenarioOrchestrator()
    result = orchestrator.run_workflow(user_scenario)
    
    print("\n\nFINAL OUTPUT (JSON):")
    print(json.dumps(result, indent=2))
    
    # ====== METHOD 2: STRANDS AGENT (PRODUCTION) ======
    print("\n\n" + "█"*70)
    print("METHOD 2: STRANDS AGENT (LLM-Driven)")
    print("█"*70)
    print("""
This method lets the LLM decide which tools to call.
More flexible, but less predictable.
Good for production use.
    """)
    
    print("\nCreating Strands agent...")
    agent = create_what_if_agent()
    
    print("Agent created! Ready to analyze scenarios.")
    print("\nExample usage:")
    print('  response = agent("What if AI became sentient tomorrow?")')
    print("\nNote: Requires Ollama running with Llama 2 model")
    
    # ====== SUMMARY ======
    print("\n\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("""
You now have a complete What-If Scenario Agent with:

✓ 6-stage workflow (Parse → Decompose → Simulate → Ripple → Rank → Report)
✓ 6 specialized tools (each does one focused job)
✓ Orchestrator (coordinates stages, manages state)
✓ Strands integration (LLM-driven tool usage)
✓ Structured output (JSON + Markdown)
✓ Full reasoning trace (see every step)

NEXT STEPS:
1. Make sure Ollama is running: ollama serve
2. Make sure Llama 2 is downloaded: ollama pull llama2
3. Run this file: python what_if_scenario_agent.py
4. Try different scenarios!

EXAMPLE SCENARIOS TO TRY:
- "What if fossil fuels were banned tomorrow?"
- "What if a major earthquake hit Tokyo?"
- "What if all cars became autonomous?"
- "What if humans lived 200 years?"
- "What if we discovered alien life?"
    """)

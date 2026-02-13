# Design Document: Fake News Immunity Agent

## Overview

The Fake News Immunity Agent is a Strands-based AI system that helps users evaluate social media claims through a structured "verification kit." Rather than claiming to verify claims, the agent teaches critical evaluation by identifying key elements, potential red flags, and actionable verification tests.

The agent implements the Strands workflow pattern (Sense → Classify → Generate tests → Score reliability → Next actions) as five sequential phases, each building on outputs from previous phases. The system accepts user input (claim text, platform, confidence), processes it through the workflow, and returns a comprehensive JSON verification kit.

### Key Design Principles

- **Non-judgmental**: The agent never claims to verify or judge truth; it teaches evaluation
- **Structured workflow**: Five distinct phases executed in order, each with clear inputs/outputs
- **Actionable output**: Every element (tests, questions, actions) is specific and executable
- **Neutral tone**: Language is objective, avoiding bias or moral judgment
- **Comprehensive coverage**: All 15 requirements addressed through tool-based architecture

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INPUT (Web Form)                        │
│              claim_text, platform, user_confidence              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STRANDS AGENT ORCHESTRATOR                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ System Prompt: Neutral, non-judgmental claim evaluator   │  │
│  │ Maintains conversation context across phases             │  │
│  │ Coordinates tool execution in workflow order             │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │ PHASE 1 │          │ PHASE 2 │          │ PHASE 3 │
   │ SENSE   │          │CLASSIFY │          │GENERATE │
   │         │          │         │          │ TESTS   │
   └─────────┘          └─────────┘          └─────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │ PHASE 4 │          │ PHASE 5 │          │ OUTPUT  │
   │ SCORE   │          │ ACTIONS │          │FORMATTER│
   │         │          │         │          │         │
   └─────────┘          └─────────┘          └─────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    JSON VERIFICATION KIT                        │
│  All required fields, valid enums, proper structure             │
└─────────────────────────────────────────────────────────────────┘
```

### Strands Workflow Integration

The agent uses Strands' tool-calling mechanism to execute each phase:

1. **Agent receives input** → Validates via InputNormalizerTool
2. **Phase 1 (Sense)** → ClaimParserTool extracts elements, RedFlagDetectorTool identifies warnings
3. **Phase 2 (Classify)** → ClaimClassifierTool assigns type, form, risk
4. **Phase 3 (Generate tests)** → VerificationTestPlannerTool creates tests based on classification
5. **Phase 4 (Score)** → ReliabilityScorerTool calculates confidence with reasoning
6. **Phase 5 (Actions)** → ActionPlanTool orders next steps
7. **Output** → OutputFormatterTool ensures valid JSON schema

Each tool is defined with clear docstrings so the LLM understands when and how to use it.

---

## Components and Interfaces

### Input Validation

**InputNormalizerTool**
- Validates claim_text: non-empty, ≤5000 characters
- Validates platform: one of [TikTok, Instagram, YouTube, X, Other]
- Validates user_confidence: integer 0-100
- Returns: normalized input or validation error with specific field

### Phase 1: Sense (Claim Parsing & Element Extraction)

**ClaimParserTool**
- Input: claim_text (string)
- Extracts: claim_summary (neutral one-sentence restatement)
- Identifies missing_details: who/what/when/where, numbers, absolutes, context gaps
- Handles multiple assertions as separate elements
- Notes temporal information gaps explicitly
- Returns: structured claim analysis

**RedFlagDetectorTool**
- Input: claim_text, claim_summary
- Identifies red_flags with two fields each:
  - flag: the observation
  - why_it_matters: explanation of significance
- Detects: absolutes (always/never/100%), lack of sources, emotional language, fear appeals
- Returns: list of red flags (may be empty)

### Phase 2: Classify (Categorization)

**ClaimClassifierTool**
- Input: claim_text, claim_summary, missing_details
- Assigns claim_type: one of [health, politics, finance, science, crime, product, celebrity, history, other]
- Assigns claim_form: one of [statistic, causal, conspiracy, anecdote, quote, before_after, prediction, other]
- Assigns risk_level: one of [low, medium, high]
  - Based on potential harm if believed, not truth value
  - Health claims with dangerous implications → high
  - Minor factual disputes → low
- Returns: classification with reasoning

### Phase 3: Generate Tests (Verification Test Planning)

**VerificationTestPlannerTool**
- Input: claim_type, claim_form, claim_text
- Generates 3-7 tests tailored to classification
- Each test includes:
  - test: what to do
  - how: how to do it
  - time_minutes: realistic time estimate
- Draws from: reverse image search, search exact quote, check primary sources, look for reputable outlet coverage, check for satire
- Omits inapplicable tests, provides alternatives
- Returns: list of verification tests

**EvidenceStandardTool**
- Input: claim_type, claim_form, claim_text
- Identifies evidence_to_settle: specific evidence types and best_sources
- Prioritizes primary sources (original research, official statements, primary data)
- Suggests reputable outlets appropriate to claim_type
- Notes if claim cannot be settled with available evidence
- Returns: evidence requirements and source recommendations

### Phase 4: Score Reliability (Confidence Scoring)

**ReliabilityScorerTool**
- Input: claim_text, red_flags, missing_details, claim_type, risk_level
- Outputs confidence_score: 0-100 representing reliability confidence
- Generates confidence_reasoning: 3-6 bullet points explaining score
- Identifies what_would_change_my_mind: evidence that would increase/decrease score
- Lower scores for insufficient information with gap explanations
- Returns: confidence assessment with reasoning

### Phase 5: Next Actions (Action Planning)

**ActionPlanTool**
- Input: tests_to_run, evidence_to_settle, questions_to_ask, risk_level
- Generates next_actions ordered by: easiest first, highest-value checks early
- Ensures first 2-3 actions provide maximum value
- Each action includes: step number and description
- Returns: prioritized action list

### Output Formatting

**OutputFormatterTool**
- Input: all phase outputs
- Generates share_safe_summary: copyable summary for sharing
  - Frames as "here's how to evaluate" not "this is false"
  - Avoids claiming verification or truth
  - Includes professional consultation reminder for health claims
- Validates all required fields present
- Ensures all enum fields contain valid values
- Returns: valid JSON matching schema or error object

---

## Data Models

### Input Schema

```json
{
  "claim_text": "string (1-5000 characters)",
  "platform": "TikTok | Instagram | YouTube | X | Other",
  "user_confidence": "integer (0-100)"
}
```

### Internal Claim Representation

```json
{
  "claim_summary": "string (neutral one-sentence restatement)",
  "missing_details": ["string"],
  "claim_type": "health | politics | finance | science | crime | product | celebrity | history | other",
  "claim_form": "statistic | causal | conspiracy | anecdote | quote | before_after | prediction | other",
  "risk_level": "low | medium | high",
  "red_flags": [
    {
      "flag": "string (observation)",
      "why_it_matters": "string (explanation)"
    }
  ],
  "tests_to_run": [
    {
      "test": "string (what to do)",
      "how": "string (how to do it)",
      "time_minutes": "integer"
    }
  ],
  "evidence_to_settle": [
    {
      "evidence_type": "string",
      "best_sources": ["string"]
    }
  ],
  "questions_to_ask": ["string (open-ended, non-leading)"],
  "confidence_score": "integer (0-100)",
  "confidence_reasoning": ["string (3-6 bullets)"],
  "what_would_change_my_mind": ["string (evidence types)"],
  "next_actions": [
    {
      "step": "integer",
      "action": "string"
    }
  ]
}
```

### Output JSON Schema

```json
{
  "claim_summary": "string",
  "missing_details": ["string"],
  "claim_type": "health | politics | finance | science | crime | product | celebrity | history | other",
  "claim_form": "statistic | causal | conspiracy | anecdote | quote | before_after | prediction | other",
  "risk_level": "low | medium | high",
  "red_flags": [
    {
      "flag": "string",
      "why_it_matters": "string"
    }
  ],
  "tests_to_run": [
    {
      "test": "string",
      "how": "string",
      "time_minutes": "integer"
    }
  ],
  "evidence_to_settle": [
    {
      "evidence_type": "string",
      "best_sources": ["string"]
    }
  ],
  "questions_to_ask": ["string"],
  "confidence_score": "integer",
  "confidence_reasoning": ["string"],
  "what_would_change_my_mind": ["string"],
  "next_actions": [
    {
      "step": "integer",
      "action": "string"
    }
  ],
  "share_safe_summary": "string"
}
```

### Error Response Schema

```json
{
  "error_message": "string (specific error description)",
  "error_code": "string (VALIDATION_ERROR | PROCESSING_ERROR | LANGUAGE_ERROR | etc)"
}
```

---

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Input Validation Completeness
*For any* user input with missing required fields, the agent SHALL return a validation error specifying which fields are required.
**Validates: Requirements 1.2**

### Property 2: Claim Text Length Enforcement
*For any* claim_text longer than 5000 characters, the agent SHALL either truncate it or reject it with a clear message.
**Validates: Requirements 1.3**

### Property 3: Confidence Range Validation
*For any* user_confidence value outside the 0-100 range, the agent SHALL return a validation error.
**Validates: Requirements 1.4**

### Property 4: Neutral Claim Summarization
*For any* claim, the claim_summary SHALL be a single neutral sentence that restates the claim without bias or editorializing.
**Validates: Requirements 2.1**

### Property 5: Missing Details Extraction
*For any* claim, missing_details SHALL include identified gaps in who/what/when/where, numbers, absolutes, and context.
**Validates: Requirements 2.2, 2.3, 2.4**

### Property 6: Claim Type Assignment
*For any* claim, exactly one claim_type SHALL be assigned from the valid enum, with "other" used for ambiguous claims.
**Validates: Requirements 3.1, 3.3**

### Property 7: Claim Form Assignment
*For any* claim, exactly one claim_form SHALL be assigned from the valid enum.
**Validates: Requirements 3.2**

### Property 8: Consistent Categorization
*For any* two similar claims, the agent SHALL assign the same claim_type and claim_form using consistent rules.
**Validates: Requirements 3.4**

### Property 9: Risk Level Assignment
*For any* claim, exactly one risk_level SHALL be assigned from [low, medium, high] based on potential harm, not truth.
**Validates: Requirements 4.1, 4.2**

### Property 10: Health Claim Risk Escalation
*For any* health claim that could lead to dangerous medical decisions, risk_level SHALL be "high".
**Validates: Requirements 4.3**

### Property 11: Verification Test Count
*For any* claim, the agent SHALL generate between 3 and 7 verification tests.
**Validates: Requirements 5.1**

### Property 12: Test Field Completeness
*For any* verification test, it SHALL include test (what), how (how), and time_minutes (estimated time).
**Validates: Requirements 5.2**

### Property 13: Test Source Validity
*For any* verification test, it SHALL be from the allowed set or a reasonable alternative.
**Validates: Requirements 5.3, 5.4**

### Property 14: Realistic Time Estimates
*For any* verification test, time_minutes SHALL be realistic and conservative for the test type.
**Validates: Requirements 5.5**

### Property 15: Red Flag Identification
*For any* claim, red_flags SHALL be identified with both flag (observation) and why_it_matters (explanation).
**Validates: Requirements 6.1, 6.2**

### Property 16: Absolute Detection
*For any* claim containing absolutes (always, never, 100%), the agent SHALL flag this as a red flag.
**Validates: Requirements 6.3**

### Property 17: Source Attribution Detection
*For any* claim lacking sources or attribution, the agent SHALL flag this as a red flag.
**Validates: Requirements 6.4**

### Property 18: Emotional Language Detection
*For any* claim using emotional language or fear appeals, the agent SHALL flag this as a red flag.
**Validates: Requirements 6.5**

### Property 19: Confidence Score Range
*For any* claim, confidence_score SHALL be an integer between 0 and 100.
**Validates: Requirements 7.1**

### Property 20: Confidence Score Language
*For any* confidence_score output, the agent SHALL NOT use terms like "truth score" or "verified".
**Validates: Requirements 7.2**

### Property 21: Confidence Reasoning Completeness
*For any* confidence_score, confidence_reasoning SHALL contain 3-6 bullet points explaining the score.
**Validates: Requirements 7.3**

### Property 22: Change Factors Identification
*For any* claim, what_would_change_my_mind SHALL list evidence that would increase or decrease the score.
**Validates: Requirements 7.4**

### Property 23: Low Confidence for Insufficient Information
*For any* claim lacking sufficient information to assess, confidence_score SHALL be lower with gap explanations.
**Validates: Requirements 7.5**

### Property 24: Evidence Requirements Specification
*For any* claim, evidence_to_settle SHALL specify evidence types and best_sources for settling the claim.
**Validates: Requirements 8.1**

### Property 25: Primary Source Prioritization
*For any* evidence_to_settle, primary sources (original research, official statements, primary data) SHALL be prioritized.
**Validates: Requirements 8.2**

### Property 26: Source Appropriateness
*For any* claim, suggested sources in evidence_to_settle SHALL be reputable and appropriate to claim_type.
**Validates: Requirements 8.3**

### Property 27: Unsettleable Claim Handling
*For any* claim that cannot be settled with available evidence, this SHALL be noted with explanation.
**Validates: Requirements 8.4**

### Property 28: Clarifying Questions Generation
*For any* claim, questions_to_ask SHALL contain 3-6 open-ended, non-leading questions.
**Validates: Requirements 9.1, 9.2**

### Property 29: Distinguishing Questions
*For any* claim, questions_to_ask SHALL include questions that help distinguish between similar claims.
**Validates: Requirements 9.3**

### Property 30: Action Ordering
*For any* next_actions, they SHALL be ordered by ease first, then highest-value checks early.
**Validates: Requirements 10.1**

### Property 31: Action Field Completeness
*For any* next_action, it SHALL include step number and action description.
**Validates: Requirements 10.2**

### Property 32: High-Value Action Prioritization
*For any* next_actions, the first 2-3 actions SHALL provide the most value for time-limited users.
**Validates: Requirements 10.3**

### Property 33: Share Safe Summary Generation
*For any* verification kit, share_safe_summary SHALL be present and copyable.
**Validates: Requirements 11.1**

### Property 34: Share Summary Language
*For any* share_safe_summary, it SHALL avoid claiming verification or truth.
**Validates: Requirements 11.2**

### Property 35: Share Summary Framing
*For any* share_safe_summary, it SHALL frame as "here's how to evaluate" not "this is false".
**Validates: Requirements 11.3**

### Property 36: Health Claim Professional Reminder
*For any* health claim, share_safe_summary SHALL include a reminder to consult qualified professionals.
**Validates: Requirements 11.4**

### Property 37: JSON Output Validity
*For any* successful analysis, the agent SHALL return only valid JSON matching the specified schema.
**Validates: Requirements 12.1**

### Property 38: Required Fields Presence
*For any* JSON output, all required fields SHALL be present: claim_summary, missing_details, claim_type, claim_form, risk_level, red_flags, tests_to_run, evidence_to_settle, questions_to_ask, confidence_score, confidence_reasoning, what_would_change_my_mind, next_actions, share_safe_summary.
**Validates: Requirements 12.2**

### Property 39: Enum Field Validity
*For any* JSON output, all enum fields SHALL contain only valid values from the specification.
**Validates: Requirements 12.3**

### Property 40: Error Response Format
*For any* error condition, the agent SHALL return a JSON error object with error_message and error_code.
**Validates: Requirements 12.4**

### Property 41: Neutral Language
*For any* analysis output, the agent SHALL use neutral, non-judgmental language.
**Validates: Requirements 13.1**

### Property 42: Political Neutrality
*For any* political claim, the agent SHALL not show political bias or persuasion.
**Validates: Requirements 13.2**

### Property 43: Health Claim Professional Guidance
*For any* health claim analysis, the agent SHALL remind users to consult qualified professionals.
**Validates: Requirements 13.3**

### Property 44: Objective Red Flag Explanation
*For any* red_flag, the explanation SHALL be objective without moral judgment.
**Validates: Requirements 13.4**

### Property 45: Workflow Phase Order
*For any* claim processing, the agent SHALL execute phases in order: Sense → Classify → Generate tests → Score reliability → Next actions.
**Validates: Requirements 14.1**

### Property 46: Phase Dependency
*For any* phase execution, later phases SHALL use outputs from previous phases to inform their analysis.
**Validates: Requirements 14.2**

### Property 47: Test Tailoring to Classification
*For any* verification tests, test selection SHALL be based on claim_type and claim_form from the Classify phase.
**Validates: Requirements 14.3**

### Property 48: Scoring Uses Earlier Phases
*For any* confidence_score, the reasoning SHALL reference red_flags and missing_details from earlier phases.
**Validates: Requirements 14.4**

### Property 49: Empty Claim Rejection
*For any* empty claim submission, the agent SHALL return a validation error.
**Validates: Requirements 15.1**

### Property 50: Language Handling
*For any* non-English claim, the agent SHALL either process it or return a clear message that only English is supported.
**Validates: Requirements 15.2**

### Property 51: Satire Detection
*For any* claim that is clearly satire or a joke, the agent SHALL identify this and adjust confidence_score accordingly.
**Validates: Requirements 15.3**

### Property 52: Vague Claim Handling
*For any* claim that is too vague to analyze, the agent SHALL note this and include clarification questions.
**Validates: Requirements 15.4**

---

## Error Handling

### Validation Errors

**Empty or Missing Fields**
- Return: `{"error_message": "claim_text is required", "error_code": "VALIDATION_ERROR"}`
- Specify which field is missing

**Invalid Platform**
- Return: `{"error_message": "platform must be one of: TikTok, Instagram, YouTube, X, Other", "error_code": "VALIDATION_ERROR"}`

**Confidence Out of Range**
- Return: `{"error_message": "user_confidence must be between 0 and 100", "error_code": "VALIDATION_ERROR"}`

**Claim Too Long**
- Option 1: Truncate to 5000 characters with message: `{"error_message": "claim_text truncated to 5000 characters", "error_code": "TRUNCATION_WARNING"}`
- Option 2: Reject with: `{"error_message": "claim_text exceeds 5000 character limit", "error_code": "VALIDATION_ERROR"}`

### Processing Errors

**Non-English Language**
- Return: `{"error_message": "This agent currently supports English claims only. Please provide your claim in English.", "error_code": "LANGUAGE_ERROR"}`

**Unsupported Content**
- Return: `{"error_message": "Unable to process this claim. Please try a different claim.", "error_code": "PROCESSING_ERROR"}`

### Graceful Degradation

**Insufficient Information**
- Lower confidence_score
- Explain gaps in confidence_reasoning
- Include clarification questions
- Continue processing rather than failing

**Ambiguous Classification**
- Assign "other" for claim_type or claim_form
- Explain reasoning in confidence_reasoning
- Provide alternative tests

**Unsettleable Claims**
- Note in evidence_to_settle: "This claim cannot be settled with available evidence"
- Explain why (unfalsifiable, requires future events, etc.)
- Provide best available verification approaches

---

## Testing Strategy

### Dual Testing Approach

The system requires both unit tests and property-based tests for comprehensive coverage:

**Unit Tests** (specific examples and edge cases):
- Validate specific input/output pairs
- Test error conditions and edge cases
- Verify integration between components
- Examples: empty claim, health claim with dangerous implications, political claim

**Property-Based Tests** (universal properties):
- Verify properties hold across all inputs
- Generate random claims and verify correctness properties
- Ensure consistency across variations
- Minimum 100 iterations per property test

### Property-Based Testing Configuration

Each correctness property (1-52 above) SHALL have a corresponding property-based test:

- **Test Framework**: Hypothesis (Python) or equivalent
- **Iterations**: Minimum 100 per property test
- **Tag Format**: `Feature: fake-news-immunity-agent, Property {N}: {property_text}`
- **Example Tag**: `Feature: fake-news-immunity-agent, Property 1: Input Validation Completeness`

### Test Organization

Tests are organized by phase:

1. **Input Validation Tests** (Properties 1-3)
   - Test invalid inputs, boundary conditions
   - Verify error messages are specific

2. **Sense Phase Tests** (Properties 4-5)
   - Test claim summarization neutrality
   - Test missing details extraction

3. **Classify Phase Tests** (Properties 6-10)
   - Test type/form/risk assignment
   - Test consistency across similar claims

4. **Generate Tests Phase Tests** (Properties 11-14)
   - Test test count and completeness
   - Test time estimate realism

5. **Red Flag Tests** (Properties 15-18)
   - Test red flag identification
   - Test specific patterns (absolutes, sources, emotion)

6. **Scoring Tests** (Properties 19-23)
   - Test confidence score range
   - Test reasoning completeness
   - Test handling of insufficient information

7. **Evidence Tests** (Properties 24-27)
   - Test evidence specification
   - Test source prioritization

8. **Questions Tests** (Properties 28-29)
   - Test question count and quality
   - Test distinguishing questions

9. **Actions Tests** (Properties 30-32)
   - Test action ordering
   - Test high-value prioritization

10. **Output Tests** (Properties 33-40)
    - Test JSON validity
    - Test field presence
    - Test enum validity

11. **Tone Tests** (Properties 41-44)
    - Test neutral language
    - Test political neutrality
    - Test objective explanations

12. **Workflow Tests** (Properties 45-48)
    - Test phase order
    - Test phase dependencies

13. **Edge Case Tests** (Properties 49-52)
    - Test empty claims
    - Test language handling
    - Test satire detection
    - Test vague claims

---

## Implementation Notes

### Technology Stack

- **Framework**: Strands Agent SDK (Python)
- **LLM**: Claude 3.5 Sonnet (via Bedrock or Anthropic API)
- **Testing**: Hypothesis (property-based testing)
- **JSON Validation**: Pydantic or jsonschema
- **Frontend**: HTML/JavaScript (provided separately)

### Dependencies

```
strands-sdk>=1.0.0
anthropic>=0.7.0
pydantic>=2.0.0
hypothesis>=6.0.0
pytest>=7.0.0
```

### Configuration Requirements

- **API Keys**: Anthropic API key or AWS Bedrock credentials
- **Model Selection**: Claude 3.5 Sonnet recommended for nuanced analysis
- **Rate Limiting**: Consider rate limits for production deployment
- **Timeout**: Set reasonable timeout for agent processing (30-60 seconds)

### System Prompt

The agent's system prompt should establish:
- Non-judgmental, neutral tone
- Focus on teaching evaluation, not claiming verification
- Emphasis on actionable, specific output
- Reminder to follow workflow phases in order
- Instruction to use tools for each phase

Example:
```
You are a neutral claim evaluation assistant. Your role is to help users 
evaluate social media claims through systematic analysis, not to verify 
or judge claims as true or false.

Follow this workflow strictly:
1. Sense: Parse and extract claim elements
2. Classify: Categorize the claim
3. Generate tests: Create verification tests
4. Score: Assess reliability confidence
5. Actions: Prioritize next steps

Use tools for each phase. Maintain neutral, non-judgmental language.
Never claim to verify or judge truth. Frame everything as "here's how 
to evaluate this claim."
```

### Integration with Frontend

The agent returns JSON that the frontend displays as:
- Claim summary and missing details
- Classification (type, form, risk)
- Red flags with explanations
- Verification tests with time estimates
- Evidence requirements
- Clarifying questions
- Confidence score with reasoning
- Prioritized next actions
- Shareable summary

---

## Design Decisions and Rationale

### Why Five Phases?

The Strands workflow (Sense → Classify → Generate → Score → Actions) maps naturally to claim evaluation:
- **Sense**: Understand what's being claimed
- **Classify**: Categorize to determine evaluation approach
- **Generate**: Create specific tests based on classification
- **Score**: Assess reliability using all gathered information
- **Actions**: Prioritize what users should do

This order ensures each phase builds on previous outputs, avoiding circular dependencies.

### Why Tool-Based Architecture?

Using Strands tools (rather than monolithic processing) provides:
- **Modularity**: Each tool has single responsibility
- **Testability**: Each tool can be tested independently
- **Flexibility**: Tools can be updated without affecting others
- **LLM Reasoning**: LLM decides which tool to use and when
- **Transparency**: Clear tool names and docstrings explain the process

### Why JSON Output?

Structured JSON enables:
- **Frontend Integration**: Easy parsing and display
- **Programmatic Use**: Other systems can consume the output
- **Validation**: Schema validation ensures correctness
- **Consistency**: All outputs follow same structure

### Why Confidence Score, Not Truth Score?

The distinction is critical:
- **Confidence Score**: Reflects reliability based on available information and quality signals
- **Truth Score**: Would claim to verify the claim (which we don't do)

This maintains the agent's non-judgmental stance while providing useful information.

### Why Prioritize Ease and Value in Actions?

Users have limited time. Ordering by ease first ensures:
- Quick wins build momentum
- High-value checks come early
- First 2-3 actions provide maximum value
- Users can stop after early actions if needed


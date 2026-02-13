# Requirements Document: Fake News Immunity Agent

## Introduction

The Fake News Immunity Agent is a tool that helps users evaluate social media claims by producing a structured "verification kit." Rather than claiming to verify claims, the agent teaches critical evaluation by identifying key elements, potential red flags, and actionable verification tests. The agent follows the Strands workflow (Sense → Classify → Generate tests → Score reliability → Next actions) to guide users through systematic claim evaluation.

## Glossary

- **Claim**: A statement or assertion made by a user about a topic, typically from social media
- **Verification Kit**: A structured JSON output containing analysis, tests, and next steps for evaluating a claim
- **Claim Type**: The domain category of a claim (health, politics, finance, science, crime, product, celebrity, history, other)
- **Claim Form**: The structural pattern of a claim (statistic, causal, conspiracy, anecdote, quote, before_after, prediction, other)
- **Risk Level**: The potential harm if the claim is believed without verification (low, medium, high)
- **Confidence Score**: A 0-100 score representing confidence in the reliability of a claim based on available information and quality signals (NOT a truth score)
- **Red Flag**: A characteristic or pattern in a claim that suggests potential unreliability
- **Verification Test**: A specific action a user can take to evaluate a claim, including time estimate
- **Agent**: The Strands-based AI system that processes claims and generates verification kits
- **Platform**: The social media source where the claim originated (TikTok, Instagram, YouTube, X, Other)
- **User Confidence**: The user's initial confidence level in the claim (0-100 scale)

## Requirements

### Requirement 1: Accept and Parse User Input

**User Story:** As a user, I want to submit a claim from social media, so that I can get help evaluating its reliability.

#### Acceptance Criteria

1. WHEN a user submits a claim through the web form, THE Agent SHALL accept claim_text (string), platform (TikTok | Instagram | YouTube | X | Other), and user_confidence (0-100 number)
2. WHEN the user submits incomplete input, THE Agent SHALL return a validation error specifying which fields are required
3. WHEN a user submits a claim_text longer than 5000 characters, THE Agent SHALL truncate or reject it with a clear message
4. WHEN a user provides user_confidence outside the 0-100 range, THE Agent SHALL return a validation error

### Requirement 2: Sense Phase - Restate and Extract

**User Story:** As a user, I want the agent to restate my claim neutrally, so that I can see if my original claim was biased or unclear.

#### Acceptance Criteria

1. WHEN the Agent processes a claim, THE Agent SHALL produce a claim_summary that restates the claim in one neutral sentence without bias or editorializing
2. WHEN analyzing a claim, THE Agent SHALL extract and list missing_details including: who/what/when/where, numbers, absolutes (always/never/100%), and missing context
3. WHEN a claim contains multiple distinct assertions, THE Agent SHALL identify each as a separate element in missing_details
4. WHEN a claim lacks temporal information, THE Agent SHALL note "timing unclear" or "no date specified" in missing_details

### Requirement 3: Classify Phase - Categorize Claim Type and Form

**User Story:** As a user, I want the agent to categorize my claim, so that I understand what domain it belongs to and what pattern it follows.

#### Acceptance Criteria

1. WHEN the Agent analyzes a claim, THE Agent SHALL assign exactly one claim_type from: health | politics | finance | science | crime | product | celebrity | history | other
2. WHEN the Agent analyzes a claim, THE Agent SHALL assign exactly one claim_form from: statistic | causal | conspiracy | anecdote | quote | before_after | prediction | other
3. WHEN a claim does not clearly fit a category, THE Agent SHALL assign "other" and explain the reasoning in confidence_reasoning
4. WHEN the Agent assigns a claim_type, THE Agent SHALL use consistent categorization rules across all claims

### Requirement 4: Assign Risk Level

**User Story:** As a user, I want to understand the potential harm of the claim, so that I know how important it is to verify.

#### Acceptance Criteria

1. WHEN the Agent analyzes a claim, THE Agent SHALL assign exactly one risk_level from: low | medium | high
2. WHEN assigning risk_level, THE Agent SHALL base it on potential harm if the claim is believed without verification, not on whether the claim is true
3. WHEN a health claim could lead to dangerous medical decisions, THE Agent SHALL assign risk_level "high"
4. WHEN a claim is a minor factual dispute with no safety implications, THE Agent SHALL assign risk_level "low"

### Requirement 5: Generate Verification Tests

**User Story:** As a user, I want specific, actionable tests I can run, so that I can verify the claim myself.

#### Acceptance Criteria

1. WHEN the Agent generates verification tests, THE Agent SHALL provide 3–7 tests tailored to the claim_type and claim_form
2. WHEN the Agent provides a test, THE Agent SHALL include: test (what to do), how (how to do it), and time_minutes (estimated time)
3. WHEN generating tests, THE Agent SHALL include tests from this set: reverse image search, search exact quote, check primary sources, look for reputable outlet coverage, check for satire
4. WHEN a test is not applicable to the claim, THE Agent SHALL omit it and provide alternative tests instead
5. WHEN the Agent provides time estimates, THE Agent SHALL be realistic and conservative (err on the side of longer estimates)

### Requirement 6: Identify Red Flags

**User Story:** As a user, I want to know what warning signs suggest the claim might be unreliable, so that I can spot manipulation patterns.

#### Acceptance Criteria

1. WHEN the Agent analyzes a claim, THE Agent SHALL identify red_flags that suggest potential unreliability
2. WHEN identifying a red_flag, THE Agent SHALL provide: flag (the observation) and why_it_matters (explanation of significance)
3. WHEN a claim contains absolutes (always, never, 100%), THE Agent SHALL flag this as a red flag
4. WHEN a claim lacks sources or attribution, THE Agent SHALL flag this as a red flag
5. WHEN a claim uses emotional language or appeals to fear, THE Agent SHALL flag this as a red flag

### Requirement 7: Score Reliability

**User Story:** As a user, I want a confidence score that reflects reliability, so that I understand how much I should trust the claim.

#### Acceptance Criteria

1. WHEN the Agent scores a claim, THE Agent SHALL output confidence_score (0–100) representing confidence in reliability based on available information and quality signals
2. WHEN the Agent provides a confidence_score, THE Agent SHALL NOT claim this is a "truth score" or verification
3. WHEN the Agent provides a confidence_score, THE Agent SHALL provide 3–6 bullet reasons in confidence_reasoning explaining the score
4. WHEN the Agent scores a claim, THE Agent SHALL list what_would_change_my_mind with evidence that would increase or decrease the score
5. WHEN a claim lacks sufficient information to assess, THE Agent SHALL assign a lower confidence_score and explain the gaps

### Requirement 8: Identify Evidence Needed

**User Story:** As a user, I want to know what specific evidence would settle the claim, so that I know what to look for.

#### Acceptance Criteria

1. WHEN the Agent analyzes a claim, THE Agent SHALL identify evidence_to_settle with specific evidence types and best_sources where that evidence can be found
2. WHEN identifying evidence, THE Agent SHALL prioritize primary sources (original research, official statements, primary data)
3. WHEN identifying evidence, THE Agent SHALL suggest reputable outlets or authoritative sources appropriate to the claim_type
4. WHEN a claim cannot be settled with available evidence, THE Agent SHALL note this and explain why

### Requirement 9: Generate Clarifying Questions

**User Story:** As a user, I want to know what questions to ask about the claim, so that I can probe for missing information.

#### Acceptance Criteria

1. WHEN the Agent analyzes a claim, THE Agent SHALL generate questions_to_ask that help clarify ambiguities or test assumptions
2. WHEN generating questions, THE Agent SHALL provide 3–6 questions that are open-ended and non-leading
3. WHEN a question would help distinguish between similar claims, THE Agent SHALL include it

### Requirement 10: Create Ordered Next Actions

**User Story:** As a user, I want a prioritized action plan, so that I know what to do first.

#### Acceptance Criteria

1. WHEN the Agent generates next_actions, THE Agent SHALL order them: easiest first, highest-value checks early
2. WHEN the Agent provides next_actions, THE Agent SHALL include step number and action description
3. WHEN a user has limited time, THE Agent SHALL ensure the first 2–3 actions provide the most value

### Requirement 11: Generate Safe Share Summary

**User Story:** As a user, I want a summary I can share, so that I can discuss the claim with others without spreading misinformation.

#### Acceptance Criteria

1. WHEN the Agent generates a verification kit, THE Agent SHALL create share_safe_summary that users can copy/paste
2. WHEN creating share_safe_summary, THE Agent SHALL avoid claiming verification or truth
3. WHEN creating share_safe_summary, THE Agent SHALL frame it as "here's how to evaluate this claim" rather than "this claim is false"
4. WHEN a claim is health-related, THE Agent SHALL include a reminder to consult qualified professionals

### Requirement 12: Return Valid JSON Output

**User Story:** As a developer, I want the agent to return structured JSON, so that I can parse and display the verification kit.

#### Acceptance Criteria

1. WHEN the Agent completes analysis, THE Agent SHALL return ONLY valid JSON matching the specified schema
2. WHEN the Agent returns JSON, THE Agent SHALL include all required fields: claim_summary, missing_details, claim_type, claim_form, risk_level, red_flags, tests_to_run, evidence_to_settle, questions_to_ask, confidence_score, confidence_reasoning, what_would_change_my_mind, next_actions, share_safe_summary
3. WHEN the Agent returns JSON, THE Agent SHALL ensure all enum fields contain only valid values from the specification
4. WHEN the Agent encounters an error, THE Agent SHALL return a JSON error object with error_message and error_code

### Requirement 13: Maintain Neutral, Non-Judgmental Tone

**User Story:** As a user, I want the agent to be neutral, so that I feel the analysis is fair and not politically motivated.

#### Acceptance Criteria

1. WHEN the Agent generates analysis, THE Agent SHALL use neutral, non-judgmental language
2. WHEN the Agent analyzes political claims, THE Agent SHALL not show political bias or persuasion
3. WHEN the Agent analyzes health claims, THE Agent SHALL remind users to consult qualified professionals
4. WHEN the Agent identifies red flags, THE Agent SHALL explain them objectively without moral judgment

### Requirement 14: Follow Strands Workflow Order

**User Story:** As a developer, I want the agent to follow the Strands workflow, so that the analysis is systematic and reproducible.

#### Acceptance Criteria

1. WHEN the Agent processes a claim, THE Agent SHALL execute phases in this order: Sense → Classify → Generate tests → Score reliability → Next actions
2. WHEN the Agent completes each phase, THE Agent SHALL use outputs from previous phases to inform later phases
3. WHEN the Agent generates tests, THE Agent SHALL base test selection on claim_type and claim_form from the Classify phase
4. WHEN the Agent scores reliability, THE Agent SHALL consider red_flags and missing_details from earlier phases

### Requirement 15: Handle Edge Cases and Errors

**User Story:** As a user, I want the agent to handle edge cases gracefully, so that I get helpful feedback even with unusual inputs.

#### Acceptance Criteria

1. WHEN a user submits an empty claim, THE Agent SHALL return a validation error
2. WHEN a user submits a claim in a language other than English, THE Agent SHALL either process it or return a clear message that only English is supported
3. WHEN a user submits a claim that is clearly satire or a joke, THE Agent SHALL identify this and adjust confidence_score accordingly
4. WHEN a user submits a claim that is too vague to analyze, THE Agent SHALL note this and ask for clarification in questions_to_ask


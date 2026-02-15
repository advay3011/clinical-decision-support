# How assess_vitals() Works - Deep Dive

Let me show you exactly how the `assess_vitals()` tool evaluates blood pressure and heart rate.

## The Code

```python
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
    
    # Blood Pressure Assessment
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
    
    # Heart Rate Assessment
    if heart_rate < 60:
        assessment["hr_status"] = "low"
        assessment["flags"].append("Resting heart rate is low - may be normal for athletes")
    elif heart_rate <= 100:
        assessment["hr_status"] = "normal"
    else:
        assessment["hr_status"] = "elevated"
        assessment["flags"].append("Elevated heart rate - check if stressed or unwell")
    
    return assessment
```

## Step-by-Step Breakdown

### Step 1: Function Definition

```python
@tool
def assess_vitals(systolic: int, diastolic: int, heart_rate: int) -> dict:
```

**What this means:**
- `@tool` - Decorator that tells Strands this is a tool the agent can use
- `systolic: int` - Top BP number (e.g., 160)
- `diastolic: int` - Bottom BP number (e.g., 90)
- `heart_rate: int` - Beats per minute (e.g., 85)
- `-> dict` - Returns a dictionary with results

### Step 2: Create Assessment Dictionary

```python
assessment = {
    "timestamp": datetime.now().isoformat(),
    "systolic": systolic,
    "diastolic": diastolic,
    "heart_rate": heart_rate,
    "bp_status": "",
    "hr_status": "",
    "flags": []
}
```

**What this does:**
- Creates a dictionary to store results
- Saves the timestamp (when this was checked)
- Stores the input values
- Creates empty fields for status and flags

**Example:**
```python
{
    "timestamp": "2024-02-13T15:30:45.123456",
    "systolic": 160,
    "diastolic": 90,
    "heart_rate": 85,
    "bp_status": "",      # Will be filled in
    "hr_status": "",      # Will be filled in
    "flags": []           # Will be filled in
}
```

### Step 3: Blood Pressure Assessment

This is where the magic happens. The function compares the BP numbers to medical standards:

#### Check 1: Low Blood Pressure

```python
if systolic < 90 or diastolic < 60:
    assessment["bp_status"] = "low"
    assessment["flags"].append("Low blood pressure - may cause dizziness")
```

**What it checks:**
- Is systolic less than 90? OR
- Is diastolic less than 60?

**If YES:**
- Status = "low"
- Add warning flag

**Example:**
```
Input: systolic=85, diastolic=55
Check: 85 < 90? YES
Result: bp_status = "low"
Flag: "Low blood pressure - may cause dizziness"
```

#### Check 2: Normal Blood Pressure

```python
elif systolic < 120 and diastolic < 80:
    assessment["bp_status"] = "normal"
```

**What it checks:**
- Is systolic less than 120? AND
- Is diastolic less than 80?

**If YES:**
- Status = "normal"
- No flags added

**Example:**
```
Input: systolic=118, diastolic=78
Check: 118 < 120 AND 78 < 80? YES
Result: bp_status = "normal"
```

#### Check 3: Elevated Blood Pressure

```python
elif systolic < 130 and diastolic < 80:
    assessment["bp_status"] = "elevated"
    assessment["flags"].append("Slightly elevated - monitor and manage stress")
```

**What it checks:**
- Is systolic less than 130? AND
- Is diastolic less than 80?

**If YES:**
- Status = "elevated"
- Add warning flag

**Example:**
```
Input: systolic=125, diastolic=78
Check: 125 < 130 AND 78 < 80? YES
Result: bp_status = "elevated"
Flag: "Slightly elevated - monitor and manage stress"
```

#### Check 4: Stage 1 Hypertension

```python
elif systolic < 140 or diastolic < 90:
    assessment["bp_status"] = "stage1_hypertension"
    assessment["flags"].append("Stage 1 hypertension - lifestyle changes recommended")
```

**What it checks:**
- Is systolic less than 140? OR
- Is diastolic less than 90?

**If YES:**
- Status = "stage1_hypertension"
- Add warning flag

**Example:**
```
Input: systolic=135, diastolic=88
Check: 135 < 140 OR 88 < 90? YES
Result: bp_status = "stage1_hypertension"
Flag: "Stage 1 hypertension - lifestyle changes recommended"
```

#### Check 5: Stage 2 Hypertension

```python
else:
    assessment["bp_status"] = "stage2_hypertension"
    assessment["flags"].append("Stage 2 hypertension - medical attention recommended")
```

**What it checks:**
- If none of the above conditions are true

**If YES:**
- Status = "stage2_hypertension"
- Add warning flag

**Example:**
```
Input: systolic=160, diastolic=90
Check: All previous checks failed
Result: bp_status = "stage2_hypertension"
Flag: "Stage 2 hypertension - medical attention recommended"
```

### Step 4: Heart Rate Assessment

Similar logic for heart rate:

#### Check 1: Low Heart Rate

```python
if heart_rate < 60:
    assessment["hr_status"] = "low"
    assessment["flags"].append("Resting heart rate is low - may be normal for athletes")
```

**Example:**
```
Input: heart_rate=55
Check: 55 < 60? YES
Result: hr_status = "low"
```

#### Check 2: Normal Heart Rate

```python
elif heart_rate <= 100:
    assessment["hr_status"] = "normal"
```

**Example:**
```
Input: heart_rate=75
Check: 75 <= 100? YES
Result: hr_status = "normal"
```

#### Check 3: Elevated Heart Rate

```python
else:
    assessment["hr_status"] = "elevated"
    assessment["flags"].append("Elevated heart rate - check if stressed or unwell")
```

**Example:**
```
Input: heart_rate=110
Check: 110 <= 100? NO
Result: hr_status = "elevated"
```

### Step 5: Return Results

```python
return assessment
```

Returns the complete assessment dictionary with all results.

## Complete Example

### Input

```python
assess_vitals(systolic=160, diastolic=90, heart_rate=85)
```

### Processing

```
1. Create assessment dict
2. Check BP: 160 >= 140? YES → stage2_hypertension
3. Add flag: "Stage 2 hypertension - medical attention recommended"
4. Check HR: 85 <= 100? YES → normal
5. Return assessment
```

### Output

```python
{
    "timestamp": "2024-02-13T15:30:45.123456",
    "systolic": 160,
    "diastolic": 90,
    "heart_rate": 85,
    "bp_status": "stage2_hypertension",
    "hr_status": "normal",
    "flags": [
        "Stage 2 hypertension - medical attention recommended"
    ]
}
```

## Blood Pressure Categories (Medical Standards)

| Category | Systolic | Diastolic | Status |
|----------|----------|-----------|--------|
| Low | < 90 | < 60 | "low" |
| Normal | < 120 | < 80 | "normal" |
| Elevated | 120-129 | < 80 | "elevated" |
| Stage 1 | 130-139 | 80-89 | "stage1_hypertension" |
| Stage 2 | ≥ 140 | ≥ 90 | "stage2_hypertension" |

## Heart Rate Categories

| Category | BPM | Status |
|----------|-----|--------|
| Low | < 60 | "low" |
| Normal | 60-100 | "normal" |
| Elevated | > 100 | "elevated" |

## How the Agent Uses It

### User Says

```
"My blood pressure is 160 over 90 and my heart rate is 85"
```

### Agent Thinks

```
1. User is reporting vitals
2. I should use assess_vitals()
3. Extract: systolic=160, diastolic=90, heart_rate=85
4. Call the tool
```

### Tool Executes

```python
result = assess_vitals(160, 90, 85)
# Returns the assessment dictionary
```

### Agent Responds

```
"That's a little on the high side. Your blood pressure is in 
Stage 2 hypertension range, which needs attention. Your heart 
rate is normal though, which is good. Are you feeling anything 
like headaches or chest tightness?"
```

## Key Points

1. **It's just comparisons** - The tool compares numbers to medical standards
2. **If/elif/else logic** - Uses conditional statements to categorize
3. **Returns structured data** - Returns a dictionary with status and flags
4. **Agent uses the result** - The agent reads the result and generates a response
5. **No external API** - It's all local logic, no API calls needed

## The Flow

```
User Input
    ↓
Agent extracts numbers
    ↓
assess_vitals(160, 90, 85)
    ↓
Compare to standards
    ↓
Return assessment
    ↓
Agent reads result
    ↓
Agent generates response
    ↓
User sees friendly message
```

## Summary

`assess_vitals()` works by:
1. Taking three numbers (systolic, diastolic, heart_rate)
2. Comparing them to medical standards using if/elif/else
3. Assigning a status (low, normal, elevated, stage1, stage2)
4. Adding warning flags if needed
5. Returning a dictionary with all the results
6. The agent then uses this result to generate a response

**It's simple logic, but powerful!** 🏥

---

**Want to see how other tools work?** Check out the other tool explanations in the docs!

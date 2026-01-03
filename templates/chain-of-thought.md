# Chain of Thought Template

## Purpose

Guide the model through step-by-step reasoning for complex problems. Use when:
- Problem requires multiple reasoning steps
- Accuracy is more important than speed
- You need to understand the model's logic
- Intermediate steps help catch errors

## The Pattern

### Basic Structure

```
[Task description]

Think through this step-by-step:
1. First, [initial analysis step]
2. Then, [second step]
3. Next, [third step]
4. Finally, [conclusion step]

[Input data]

Show your reasoning for each step, then provide your final answer.
```

### Key Elements

1. **Explicit instruction to reason**: "Think step-by-step"
2. **Structured steps**: Guide the reasoning process
3. **Reasoning visibility**: Ask for shown work
4. **Clear conclusion**: Separate reasoning from answer

## Template Variants

### Variant 1: Open-Ended Chain of Thought

```
Analyze the following situation and provide a recommendation.

{{situation_description}}

Think through this carefully:
1. What are the key factors to consider?
2. What are the possible options?
3. What are the pros and cons of each option?
4. What risks should be considered?
5. Based on this analysis, what is your recommendation?

Show your reasoning for each step.
```

### Variant 2: Structured Problem Solving

```
Solve this problem step-by-step.

PROBLEM:
{{problem_statement}}

Follow these steps:

STEP 1 - UNDERSTAND THE PROBLEM
- What are we trying to find/solve?
- What information is given?
- What constraints exist?

STEP 2 - IDENTIFY THE APPROACH
- What method or framework applies?
- What similar problems does this resemble?

STEP 3 - WORK THROUGH THE SOLUTION
- Show each calculation or logical step
- Explain why each step follows from the previous

STEP 4 - VERIFY THE ANSWER
- Does the answer make sense?
- Does it satisfy the constraints?
- Can we check it another way?

FINAL ANSWER:
[Your answer here]
```

### Variant 3: Decision Analysis

```
Evaluate this decision using structured reasoning.

DECISION TO EVALUATE:
{{decision_description}}

CONTEXT:
{{context}}

Analyze using this framework:

1. SITUATION ASSESSMENT
   - What is the current state?
   - What are the objectives?
   - What are the constraints?

2. OPTIONS ANALYSIS
   For each option:
   - Describe the option
   - List benefits
   - List drawbacks
   - Assess feasibility
   - Estimate outcomes

3. RISK ASSESSMENT
   - What could go wrong?
   - How likely are negative outcomes?
   - How severe would they be?
   - Can risks be mitigated?

4. RECOMMENDATION
   - Which option do you recommend?
   - Why is this the best choice?
   - What are the key implementation considerations?
   - What should be monitored after deciding?

Provide your analysis:
```

### Variant 4: Diagnostic Reasoning

```
Diagnose the issue described below.

SYMPTOMS:
{{symptoms}}

CONTEXT:
{{context}}

Think through this systematically:

1. SYMPTOM ANALYSIS
   - What exactly is happening?
   - When did it start?
   - What are the patterns?

2. HYPOTHESIS GENERATION
   - What could cause these symptoms?
   - List at least 3 possible causes
   - Rank by likelihood

3. EVIDENCE EVALUATION
   For each hypothesis:
   - What evidence supports it?
   - What evidence contradicts it?
   - What additional information would confirm/refute it?

4. CONCLUSION
   - Most likely cause: [X]
   - Confidence: [high/medium/low]
   - Recommended next steps: [actions]
```

### Variant 5: Math/Logic Problems

```
Solve this problem, showing all work.

PROBLEM:
{{math_problem}}

Approach:
1. Identify what we need to find
2. List the relevant information
3. Determine the method to use
4. Execute step-by-step
5. Verify the answer

Solution:

Step 1: [First step with explanation]

Step 2: [Second step with explanation]

[Continue as needed]

Verification: [Check the answer]

FINAL ANSWER: [Boxed or clearly marked answer]
```

### Variant 6: Comparative Analysis

```
Compare these options and recommend one.

OPTION A:
{{option_a}}

OPTION B:
{{option_b}}

{{#if option_c}}
OPTION C:
{{option_c}}
{{/if}}

EVALUATION CRITERIA:
{{criteria}}

Analysis:

1. CRITERIA WEIGHTING
   - Rank criteria by importance
   - Explain the ranking rationale

2. OPTION EVALUATION
   For each option, score against each criterion:
   - [Criterion 1]: Score and reasoning
   - [Criterion 2]: Score and reasoning
   - [Continue for all criteria]

3. TRADE-OFF ANALYSIS
   - What are you giving up with each choice?
   - Which trade-offs are most acceptable?

4. RECOMMENDATION
   - Selected option: [X]
   - Key reasons: [primary factors]
   - Caveats: [when another option might be better]
```

## Best Practices

### 1. Step Granularity

**Too vague:**
```
1. Think about the problem
2. Solve it
3. Check your work
```

**Too granular:**
```
1. Read the first word
2. Read the second word
3. Understand word 1
4. Understand word 2
...
```

**Just right:**
```
1. Identify the key variables
2. Determine the relationship between them
3. Set up the equation
4. Solve for the unknown
5. Verify against constraints
```

### 2. Reasoning Markers

Use consistent markers to separate reasoning from output:

```
THINKING: [reasoning process]
ANALYSIS: [structured analysis]
REASONING: [step-by-step logic]
---
CONCLUSION: [final answer]
ANSWER: [result]
RECOMMENDATION: [action to take]
```

### 3. Encourage Self-Correction

```
After reaching a conclusion, ask yourself:
- Does this make sense?
- Did I miss anything?
- Would this hold up to scrutiny?

If you find an error, go back and correct it before providing the final answer.
```

### 4. Handle Uncertainty

```
Express your confidence at each step:
- "I'm confident that..." for strong conclusions
- "This suggests..." for reasonable inferences
- "It's possible that..." for uncertain elements
- "I need more information about..." for gaps
```

## Common Gotchas

### Problem: Model skips steps

**Solution:** Make steps mandatory:
```
You MUST complete each step below. Do not skip any steps.

Step 1: [Required step]
[Your response here - do not leave blank]

Step 2: [Required step]
[Your response here - do not leave blank]
```

### Problem: Reasoning too verbose

**Solution:** Set length expectations:
```
For each step, provide 1-2 sentences of reasoning. Be concise but complete.
```

### Problem: Model reaches wrong conclusion despite good reasoning

**Solution:** Add verification step:
```
VERIFICATION:
Before finalizing, check:
- Does your answer actually address the original question?
- Are there any mathematical errors in your calculations?
- Does your conclusion follow logically from your reasoning?
```

### Problem: Model provides reasoning but no clear answer

**Solution:** Require explicit final answer:
```
After your reasoning, you MUST provide a final answer in this format:

=== FINAL ANSWER ===
[Your clear, direct answer here]
=== END ===
```

## When to Use Chain of Thought

**Best for:**
- Multi-step reasoning problems
- Mathematical calculations
- Logical deduction
- Complex decisions
- Debugging/troubleshooting
- Evaluation with multiple criteria

**Consider alternatives:**
- Simple factual queries (direct answer faster)
- Creative tasks (structure may constrain)
- Very time-sensitive applications (adds latency)
- High-volume processing (increased token usage)

## Performance Considerations

| Aspect | Impact |
|--------|--------|
| Accuracy | Generally improves, especially for complex tasks |
| Latency | Increases (more tokens generated) |
| Cost | Higher (more output tokens) |
| Interpretability | Much better (can see reasoning) |
| Consistency | Often improves (structured process) |

## Model-Specific Notes

| Model | Notes |
|-------|-------|
| Claude Opus 4 | Excellent CoT, can handle complex multi-step reasoning |
| Claude Sonnet | Good CoT, provide clear step structure |
| GPT-4o | Strong CoT capabilities |
| GPT-4o-mini | Capable but may need more explicit steps |
| Smaller models | CoT often helps significantly but keep steps simple |

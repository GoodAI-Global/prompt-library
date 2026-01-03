# Few-Shot Learning Template

## Purpose

Demonstrate desired behavior through examples rather than instructions. Use when:
- Task requires nuanced judgment
- Instructions alone are ambiguous
- Consistent formatting is critical
- Classification has subtle distinctions

## The Pattern

### Basic Structure

```
[Brief task description]

Examples:

Input: [example input 1]
Output: [example output 1]

Input: [example input 2]
Output: [example output 2]

Input: [example input 3]
Output: [example output 3]

Now process:
Input: {{actual_input}}
Output:
```

### Key Elements

1. **Minimal instruction**: Let examples do the teaching
2. **Diverse examples**: Cover different cases
3. **Consistent format**: Same structure every time
4. **Clear delimiter**: Separate examples from actual task

## Template Variants

### Variant 1: Classification

```
Classify customer feedback sentiment.

Examples:

Feedback: "This product exceeded all my expectations! Best purchase ever."
Sentiment: positive
Reason: Strong positive language, superlatives

Feedback: "It works okay I guess. Nothing special."
Sentiment: neutral
Reason: Lukewarm language, no strong sentiment

Feedback: "Complete waste of money. Broke after one week."
Sentiment: negative
Reason: Negative outcome, strong negative language

Feedback: "Oh great, another update that breaks everything."
Sentiment: negative
Reason: Sarcasm indicating frustration

Feedback: "Received on Tuesday as expected."
Sentiment: neutral
Reason: Factual statement, no emotional content

Now classify:
Feedback: {{customer_feedback}}
Sentiment:
Reason:
```

### Variant 2: Extraction with Format

```
Extract structured data from transaction descriptions.

Examples:

Transaction: "AMAZON.COM*MK4TZ AMZN.COM/BILL WA"
{
  "merchant": "Amazon",
  "category": "online_shopping",
  "location": "WA",
  "type": "purchase"
}

Transaction: "UBER *EATS HELP.UBER.C CA"
{
  "merchant": "Uber Eats",
  "category": "food_delivery",
  "location": "CA",
  "type": "purchase"
}

Transaction: "PAYPAL *NETFLIX 866-716-0414 CA"
{
  "merchant": "Netflix",
  "category": "subscription",
  "location": "CA",
  "type": "recurring"
}

Transaction: "ATM WITHDRAWAL 1234 MAIN ST"
{
  "merchant": null,
  "category": "cash",
  "location": "unknown",
  "type": "withdrawal"
}

Now extract:
Transaction: {{transaction_description}}
```

### Variant 3: Transformation

```
Convert natural language to SQL queries.

Examples:

Request: "Show me all customers from New York"
SQL: SELECT * FROM customers WHERE state = 'NY';

Request: "How many orders were placed last month?"
SQL: SELECT COUNT(*) FROM orders WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH);

Request: "Get the top 5 products by revenue"
SQL: SELECT product_name, SUM(quantity * price) as revenue FROM order_items GROUP BY product_name ORDER BY revenue DESC LIMIT 5;

Request: "Find customers who haven't ordered in 90 days"
SQL: SELECT c.* FROM customers c LEFT JOIN orders o ON c.id = o.customer_id WHERE o.order_date < DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY) OR o.id IS NULL;

Now convert:
Request: {{natural_language_query}}
SQL:
```

### Variant 4: Edge Cases Emphasis

```
Extract phone numbers from text. Handle various formats.

Examples:

Text: "Call me at 555-123-4567"
Phone: +1-555-123-4567

Text: "My number is (555) 123-4567"
Phone: +1-555-123-4567

Text: "Reach me at 5551234567"
Phone: +1-555-123-4567

Text: "International: +44 20 7946 0958"
Phone: +44-20-7946-0958

Text: "No contact info provided"
Phone: null

Text: "Call 555-1234 or 555-5678"
Phone: ["+1-555-555-1234", "+1-555-555-5678"]

Now extract:
Text: {{input_text}}
Phone:
```

### Variant 5: Chain of Thought Few-Shot

```
Determine if the customer request requires escalation.

Examples:

Request: "I want to cancel my account immediately"
Thinking: Customer wants to cancel. This is a retention risk. Standard cancellation can be handled by tier 1, but we should try to retain.
Decision: no_escalate
Action: Transfer to retention team (not escalation, standard routing)

Request: "I've been charged incorrectly for 3 months and nobody will fix it"
Thinking: Billing issue persisting across multiple months. Customer has already tried to resolve. Frustration evident. This is a repeated failure to resolve.
Decision: escalate
Action: Escalate to billing supervisor with history

Request: "How do I update my address?"
Thinking: Simple account maintenance question. Standard procedure exists. No complexity.
Decision: no_escalate
Action: Provide self-service instructions or handle directly

Request: "I'm a lawyer and will be filing suit unless this is resolved today"
Thinking: Legal threat mentioned. Regardless of merit, legal threats require special handling per policy.
Decision: escalate
Action: Immediate escalation to legal/compliance team

Now process:
Request: {{customer_request}}
Thinking:
Decision:
Action:
```

## Best Practices

### 1. Example Selection

**Cover the spectrum:**
- Clear positive case
- Clear negative case
- Edge cases / boundary conditions
- Common errors or confusions
- At least one "tricky" case

**Diversity checklist:**
- Different lengths of input
- Different formats
- Different domains (if applicable)
- Different outcomes

### 2. Example Count

| Task Complexity | Recommended Examples |
|-----------------|---------------------|
| Simple binary | 2-3 |
| Multi-class (3-5 classes) | 4-6 |
| Complex judgment | 5-8 |
| With reasoning | 3-5 (reasoning adds length) |

### 3. Example Order

**Options:**
- Simple to complex (building understanding)
- By category (one of each type)
- Random (reduce order bias)
- Edge cases last (leave impression)

### 4. Formatting Consistency

All examples must use identical format:
```
# Consistent
Input: "example"
Output: result

Input: "example"
Output: result

# Inconsistent (BAD)
Input: "example"
Output: result

Text: "example"
Result: something
```

## Common Gotchas

### Problem: Model copies example instead of generalizing

**Solution:** Add variety to examples:
```
# Instead of similar examples
Input: "I love this product"
Output: positive

Input: "I love this service"
Output: positive

# Use diverse examples
Input: "I love this product"
Output: positive

Input: "Exceeded expectations"
Output: positive

Input: "Absolutely fantastic experience"
Output: positive
```

### Problem: Examples too similar to actual input

**Solution:** Keep examples clearly different:
```
# If classifying support tickets, use examples from different topics
# than what you expect to process
```

### Problem: Output format drift

**Solution:** Use explicit delimiters:
```
---
Example 1:
Input: xxx
Output: yyy
---
Example 2:
Input: xxx
Output: yyy
---

Now your turn:
Input: {{actual}}
Output:
```

### Problem: Model explaining instead of doing

**Solution:** Examples should show just output:
```
# Bad - includes explanation in output
Input: "The food was cold"
Output: This is negative sentiment because the customer is complaining about food temperature. negative

# Good - clean output
Input: "The food was cold"
Output: negative
```

## Example Library Patterns

### Reusable Example Sets

```python
SENTIMENT_EXAMPLES = """
Text: "Best purchase I've ever made!"
Sentiment: positive

Text: "Arrived damaged, very disappointed"
Sentiment: negative

Text: "It's okay, works as expected"
Sentiment: neutral

Text: "Oh sure, 'fast shipping' my foot"
Sentiment: negative
"""

def classify_sentiment(text: str) -> str:
    prompt = f"""Classify the sentiment.

{SENTIMENT_EXAMPLES}

Text: "{text}"
Sentiment:"""
    return call_llm(prompt)
```

### Dynamic Example Selection

```python
def get_relevant_examples(input_text: str, example_pool: list, n: int = 3) -> list:
    """Select most relevant examples using embedding similarity."""
    input_embedding = embed(input_text)
    scored = [
        (example, cosine_similarity(input_embedding, embed(example['input'])))
        for example in example_pool
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [ex for ex, score in scored[:n]]
```

## When to Use Few-Shot

**Best for:**
- Classification with nuance
- Format transformation
- Subjective judgments
- Domain-specific conventions
- When examples are clearer than rules

**Consider alternatives:**
- Very simple tasks (zero-shot may suffice)
- Highly variable output (examples may constrain)
- Limited context window (examples consume tokens)
- Rapidly changing requirements (updating examples is overhead)

## Model-Specific Notes

| Model | Notes |
|-------|-------|
| Claude Opus 4 | Excellent few-shot learning, can use fewer examples |
| Claude Sonnet | Good few-shot, use 3-5 examples |
| GPT-4o | Strong few-shot, similar to Claude |
| GPT-4o-mini | May need more examples for nuanced tasks |
| Smaller models | Need more examples, simpler patterns |

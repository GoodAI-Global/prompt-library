# Tool Use Patterns

## Use Case

Structure prompts for effective function calling and tool use:
- API integration with LLMs
- Multi-tool orchestration
- Parameter extraction and validation
- Error handling in tool calls
- Tool selection reasoning

Use when building systems where the LLM needs to call external functions or APIs.

## Input Format

**Required:**
- `user_request`: The user's request or query
- `available_tools`: List of tools with descriptions and parameters

**Optional:**
- `context`: Additional context for tool selection
- `constraints`: Limitations on tool usage
- `previous_calls`: History of previous tool calls in conversation

## Output Format

```json
{
  "reasoning": {
    "user_intent": "What the user is trying to accomplish",
    "required_information": ["Info needed to fulfill request"],
    "tool_selection_rationale": "Why these tools were chosen"
  },
  "tool_calls": [
    {
      "tool_name": "function_name",
      "parameters": {
        "param1": "value1",
        "param2": "value2"
      },
      "purpose": "Why this tool call is needed",
      "depends_on": null
    }
  ],
  "execution_plan": {
    "parallel": ["tool_calls that can run in parallel"],
    "sequential": ["tool_calls that must run in order"],
    "contingent": {
      "if_success": "next_action",
      "if_failure": "fallback_action"
    }
  },
  "expected_outcome": "What the combined tool calls should produce",
  "fallback_strategy": "What to do if tools fail"
}
```

## The Prompt

```
You are an AI assistant with access to tools. Analyze the user's request and determine which tools to use and how to use them.

USER REQUEST:
{{user_request}}

AVAILABLE TOOLS:
{{available_tools}}

{{#if context}}
ADDITIONAL CONTEXT:
{{context}}
{{/if}}

{{#if constraints}}
CONSTRAINTS:
{{constraints}}
{{/if}}

{{#if previous_calls}}
PREVIOUS TOOL CALLS:
{{previous_calls}}
{{/if}}

TOOL USE FRAMEWORK:

1. UNDERSTAND THE REQUEST
   - What is the user trying to accomplish?
   - What information is needed?
   - What actions need to be taken?

2. TOOL SELECTION
   For each required action:
   - Which tool(s) can accomplish this?
   - Are the required parameters available?
   - Are there dependencies between tools?

   Selection criteria:
   - Choose the most specific tool for the task
   - Prefer fewer tool calls when possible
   - Consider tool limitations and edge cases

3. PARAMETER EXTRACTION
   For each tool call:
   - Extract parameters from user request
   - Validate parameter types and formats
   - Use defaults where appropriate
   - Flag missing required parameters

4. EXECUTION PLANNING
   Determine execution order:
   - Parallel: Independent calls that can run simultaneously
   - Sequential: Calls that depend on previous results
   - Contingent: Calls that depend on success/failure

5. ERROR HANDLING
   Plan for failures:
   - What if a tool call fails?
   - Are there fallback options?
   - How to communicate failures to user?

TOOL CALLING RULES:
- Only call tools that exist in the available tools list
- Provide all required parameters
- Use correct parameter types
- Don't invent capabilities tools don't have
- If unsure, ask for clarification rather than guessing

PARAMETER FORMATTING:
- Dates: ISO 8601 format (YYYY-MM-DD)
- Times: 24-hour format (HH:MM:SS)
- Numbers: Unformatted (no commas or currency symbols)
- Lists: JSON arrays
- Booleans: true/false (lowercase)

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{user_request}}` | string | Yes | User's request or query |
| `{{available_tools}}` | string | Yes | Tool definitions |
| `{{context}}` | string | No | Additional context |
| `{{constraints}}` | string | No | Usage limitations |
| `{{previous_calls}}` | string | No | Previous tool call history |

## Examples

### Example 1: Multi-Tool Orchestration

**Input:**
```
user_request: |
  Book a flight from San Francisco to New York for next Friday,
  and find a hotel near Times Square for 2 nights. Budget is $500
  for the hotel.

available_tools: |
  1. search_flights
     Description: Search for available flights
     Parameters:
       - origin (string, required): Departure airport code
       - destination (string, required): Arrival airport code
       - date (string, required): Departure date (YYYY-MM-DD)
       - passengers (integer, optional): Number of passengers (default: 1)
       - class (string, optional): Economy, Business, First

  2. book_flight
     Description: Book a specific flight
     Parameters:
       - flight_id (string, required): Flight ID from search results
       - passenger_info (object, required): Passenger details

  3. search_hotels
     Description: Search for available hotels
     Parameters:
       - location (string, required): City or address
       - checkin (string, required): Check-in date (YYYY-MM-DD)
       - checkout (string, required): Check-out date (YYYY-MM-DD)
       - guests (integer, optional): Number of guests (default: 1)
       - max_price (number, optional): Maximum price per night

  4. book_hotel
     Description: Book a specific hotel
     Parameters:
       - hotel_id (string, required): Hotel ID from search results
       - guest_info (object, required): Guest details

context: |
  Today's date: 2024-01-15 (Monday)
  "Next Friday" = 2024-01-19
```

**Output:**
```json
{
  "reasoning": {
    "user_intent": "Book travel from San Francisco to New York including flight and hotel accommodations",
    "required_information": [
      "Available flights SFO to NYC on 2024-01-19",
      "Available hotels near Times Square for 2024-01-19 to 2024-01-21",
      "Passenger/guest information (not yet provided)"
    ],
    "tool_selection_rationale": "Need to search for options before booking. Flight and hotel searches are independent and can run in parallel. Booking requires user selection from search results."
  },
  "tool_calls": [
    {
      "tool_name": "search_flights",
      "parameters": {
        "origin": "SFO",
        "destination": "JFK",
        "date": "2024-01-19",
        "passengers": 1,
        "class": "Economy"
      },
      "purpose": "Find available flights from San Francisco to New York",
      "depends_on": null
    },
    {
      "tool_name": "search_hotels",
      "parameters": {
        "location": "Times Square, New York, NY",
        "checkin": "2024-01-19",
        "checkout": "2024-01-21",
        "guests": 1,
        "max_price": 250
      },
      "purpose": "Find hotels near Times Square within budget ($500 total / 2 nights = $250/night)",
      "depends_on": null
    }
  ],
  "execution_plan": {
    "parallel": ["search_flights", "search_hotels"],
    "sequential": [],
    "contingent": {
      "if_success": "Present options to user for selection, then proceed with booking",
      "if_failure": "If no flights available, suggest alternative dates. If no hotels in budget, suggest nearby areas or higher budget."
    }
  },
  "expected_outcome": "List of available flights and hotels matching user criteria for user to select from",
  "fallback_strategy": "If JFK has no availability, try LGA or EWR as alternate NYC airports",
  "user_action_required": [
    "Select preferred flight from search results",
    "Select preferred hotel from search results",
    "Provide passenger/guest information for booking"
  ]
}
```

### Example 2: Sequential Tool Calls with Dependencies

**Input:**
```
user_request: |
  Get the current stock price for Apple, then calculate what my 100 shares are worth,
  and add that to my portfolio tracker.

available_tools: |
  1. get_stock_price
     Description: Get current stock price
     Parameters:
       - symbol (string, required): Stock ticker symbol
     Returns: { price: number, currency: string, timestamp: string }

  2. calculate_value
     Description: Calculate total value of holdings
     Parameters:
       - price (number, required): Price per share
       - quantity (number, required): Number of shares
     Returns: { total_value: number }

  3. update_portfolio
     Description: Update portfolio with current holdings value
     Parameters:
       - symbol (string, required): Stock ticker symbol
       - quantity (number, required): Number of shares
       - current_value (number, required): Total current value
     Returns: { success: boolean, portfolio_id: string }
```

**Output:**
```json
{
  "reasoning": {
    "user_intent": "Calculate and record the current value of Apple stock holdings",
    "required_information": [
      "Current Apple stock price (from get_stock_price)",
      "Total value calculation (from calculate_value)",
      "Portfolio update confirmation (from update_portfolio)"
    ],
    "tool_selection_rationale": "Sequential dependency: need price before calculating value, need value before updating portfolio. All three tools required in order."
  },
  "tool_calls": [
    {
      "tool_name": "get_stock_price",
      "parameters": {
        "symbol": "AAPL"
      },
      "purpose": "Get current Apple stock price",
      "depends_on": null
    },
    {
      "tool_name": "calculate_value",
      "parameters": {
        "price": "{{get_stock_price.result.price}}",
        "quantity": 100
      },
      "purpose": "Calculate total value of 100 shares",
      "depends_on": "get_stock_price"
    },
    {
      "tool_name": "update_portfolio",
      "parameters": {
        "symbol": "AAPL",
        "quantity": 100,
        "current_value": "{{calculate_value.result.total_value}}"
      },
      "purpose": "Update portfolio tracker with current value",
      "depends_on": "calculate_value"
    }
  ],
  "execution_plan": {
    "parallel": [],
    "sequential": ["get_stock_price", "calculate_value", "update_portfolio"],
    "contingent": {
      "if_success": "Report final portfolio value to user",
      "if_failure": "If stock price unavailable, report market may be closed. If portfolio update fails, retry once then report error."
    }
  },
  "expected_outcome": "Portfolio updated with current value of 100 AAPL shares, confirmation returned to user",
  "fallback_strategy": "If any step fails, report partial results (e.g., 'Got price but couldn't update portfolio')"
}
```

## Gotchas

### Common Failure Modes
1. **Hallucinated tools**: Model invents tools that don't exist
2. **Wrong parameters**: Incorrect types or missing required params
3. **Ignoring dependencies**: Calling tools before dependencies complete
4. **Over-tooling**: Using multiple tools when one would suffice

### Edge Cases to Handle
- **Ambiguous requests**: Ask for clarification vs. guessing
- **Missing parameters**: Request needed info from user
- **Tool limitations**: Acknowledge when no tool can help
- **Rate limits**: Consider tool call frequency limits

### When NOT to Use This Prompt
- **Simple queries**: Direct answers don't need tools
- **Sensitive operations**: Dangerous actions need safeguards
- **Real-time systems**: May need different architecture
- **Stateful operations**: May need session management

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex multi-tool orchestration | Best reasoning about dependencies |
| **Acceptable:** Claude Sonnet 4 | Standard tool use | Good parameter extraction |
| **Acceptable:** GPT-4o | Function calling | Native function calling support |
| **Caution:** Smaller models | - | May hallucinate tools or parameters |

## Integration Notes

### With Claude Tool Use API

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_stock_price",
        "description": "Get current stock price",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Stock ticker symbol"}
            },
            "required": ["symbol"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's Apple's stock price?"}]
)
```

### Error Handling

```python
def handle_tool_result(tool_name: str, result: dict) -> dict:
    """Process tool result with error handling."""
    if result.get("error"):
        return {
            "tool_name": tool_name,
            "success": False,
            "error": result["error"],
            "fallback_action": determine_fallback(tool_name, result["error"])
        }
    return {
        "tool_name": tool_name,
        "success": True,
        "result": result
    }
```

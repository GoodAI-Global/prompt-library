# Human-in-the-Loop Patterns

## Use Case

Design prompts for workflows requiring human approval or input:
- Approval workflows before critical actions
- Confirmation of high-stakes decisions
- Human review of AI-generated content
- Escalation of uncertain cases
- Collaborative human-AI task completion

Use when building systems where human oversight is required for safety, compliance, or quality.

## Input Format

**Required:**
- `task`: The task being performed
- `current_state`: Current state of the workflow
- `decision_point`: What decision or action needs human input

**Optional:**
- `risk_level`: Severity of the decision
- `context`: Background information for the human reviewer
- `options`: Pre-defined options for the human to choose from
- `deadline`: Time constraint for the decision

## Output Format

```json
{
  "workflow_state": {
    "task_id": "TASK-001",
    "status": "awaiting_human_input",
    "current_step": "approval_required",
    "initiated_at": "2024-01-15T10:00:00Z"
  },
  "human_input_request": {
    "type": "approval|selection|input|review",
    "priority": "critical|high|medium|low",
    "assigned_to": "role_or_person",
    "deadline": "2024-01-15T12:00:00Z"
  },
  "decision_context": {
    "summary": "Brief summary of what needs to be decided",
    "background": "Relevant context for the decision",
    "what_ai_did": "Actions taken before this point",
    "what_happens_next": "Consequences of different decisions"
  },
  "options": [
    {
      "option_id": "approve",
      "label": "Approve",
      "description": "Accept the proposed action",
      "consequences": "What happens if selected",
      "recommended": true,
      "recommendation_reason": "Why AI suggests this"
    },
    {
      "option_id": "reject",
      "label": "Reject",
      "description": "Decline the proposed action",
      "consequences": "What happens if selected",
      "recommended": false
    },
    {
      "option_id": "modify",
      "label": "Modify",
      "description": "Request changes before proceeding",
      "requires_input": true,
      "input_prompt": "What changes would you like?"
    }
  ],
  "risk_assessment": {
    "level": "high",
    "factors": ["Factor 1", "Factor 2"],
    "reversibility": "reversible|partially_reversible|irreversible",
    "impact_scope": "Description of who/what is affected"
  },
  "supporting_information": {
    "data_summary": "Relevant data for decision",
    "similar_cases": ["How similar situations were handled"],
    "policies": ["Relevant policies or guidelines"]
  },
  "escalation": {
    "escalate_if": "Conditions for escalation",
    "escalate_to": "Who to escalate to",
    "auto_escalate_after": "2024-01-15T14:00:00Z"
  },
  "audit_trail": {
    "events": [
      {
        "timestamp": "2024-01-15T10:00:00Z",
        "action": "workflow_initiated",
        "actor": "system"
      }
    ]
  }
}
```

## The Prompt

```
You are an AI assistant in a human-in-the-loop workflow. Prepare decision points for human review with clear context and options.

TASK:
{{task}}

CURRENT STATE:
{{current_state}}

DECISION POINT:
{{decision_point}}

RISK LEVEL: {{risk_level | default: "medium"}}

{{#if context}}
ADDITIONAL CONTEXT:
{{context}}
{{/if}}

{{#if options}}
PREDEFINED OPTIONS:
{{options}}
{{/if}}

{{#if deadline}}
DEADLINE: {{deadline}}
{{/if}}

HUMAN-IN-THE-LOOP FRAMEWORK:

1. ASSESS THE DECISION POINT
   Determine:
   - What type of human input is needed (approval, selection, free input, review)
   - Priority level based on risk and time sensitivity
   - Who should make this decision
   - What information they need

2. PREPARE DECISION CONTEXT
   For the human reviewer, provide:
   - Clear summary of what needs to be decided
   - Background context (what led to this point)
   - What the AI has done/analyzed so far
   - What will happen based on their decision

3. STRUCTURE OPTIONS
   For each option:
   - Clear label and description
   - Consequences of choosing this option
   - AI recommendation if appropriate
   - Required follow-up input if any

4. ASSESS AND COMMUNICATE RISK
   Provide risk assessment:
   - Overall risk level
   - Contributing factors
   - Reversibility of the action
   - Scope of impact
   - Compliance considerations

5. PROVIDE SUPPORTING INFORMATION
   Include:
   - Relevant data summaries
   - Similar past cases if available
   - Applicable policies or guidelines
   - Confidence levels for AI analysis

6. DEFINE ESCALATION PATHS
   Specify:
   - When to escalate
   - Who to escalate to
   - Automatic escalation triggers (timeout, complexity)

7. MAINTAIN AUDIT TRAIL
   Track:
   - Workflow timeline
   - Actions taken
   - Decisions made
   - Who made them

PRINCIPLES FOR HUMAN HANDOFF:
- Be transparent about AI confidence and limitations
- Present information clearly and concisely
- Make the decision easy to understand
- Don't hide important information
- Respect human time - don't over-ask
- Provide enough context without overwhelming

WHEN TO REQUIRE HUMAN INPUT:
- High-stakes or irreversible actions
- Low AI confidence (below threshold)
- Policy or compliance requirements
- Novel situations outside training
- Ethical considerations
- Customer-facing communications

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{task}}` | string | Yes | Task being performed |
| `{{current_state}}` | string | Yes | Current workflow state |
| `{{decision_point}}` | string | Yes | Decision needing input |
| `{{risk_level}}` | string | No | Risk severity |
| `{{context}}` | string | No | Background information |
| `{{options}}` | string | No | Predefined options |
| `{{deadline}}` | string | No | Decision deadline |

## Examples

### Example 1: High-Value Refund Approval

**Input:**
```
task: |
  Process customer refund request for order #ORD-2024-15789

current_state: |
  - Customer requested full refund for $2,847.00 purchase
  - Order placed 45 days ago (outside 30-day policy)
  - Customer claims product defective, no photos provided
  - Customer lifetime value: $12,500 (VIP tier)
  - Previous refunds: 1 in past year ($150)
  - AI has verified order exists and matches customer account

decision_point: |
  Approve full refund that exceeds standard policy limits
  - Amount: $2,847.00 (above $500 auto-approve threshold)
  - Outside return window: 45 days vs 30-day policy
  - No defect documentation provided

risk_level: high

context: |
  - Company policy: Refunds >$500 require manager approval
  - VIP customers have extended 60-day return window
  - Competitor recently launched similar product
  - Q1 retention target: 95% (currently at 93%)
```

**Output:**
```json
{
  "workflow_state": {
    "task_id": "REFUND-2024-15789",
    "status": "awaiting_human_input",
    "current_step": "manager_approval_required",
    "initiated_at": "2024-01-15T10:30:00Z"
  },
  "human_input_request": {
    "type": "approval",
    "priority": "high",
    "assigned_to": "customer_service_manager",
    "deadline": "2024-01-15T17:00:00Z",
    "reason_for_human": "Refund amount ($2,847) exceeds auto-approve threshold ($500)"
  },
  "decision_context": {
    "summary": "VIP customer requesting $2,847 refund for order 45 days old, claiming defect but no documentation provided",
    "background": "Customer is VIP tier ($12,500 LTV) with minimal refund history (1 refund of $150 in past year). Order is outside standard 30-day window but within VIP 60-day window.",
    "what_ai_did": "Verified order exists, confirmed customer identity, checked refund history, identified VIP status, flagged policy exceptions",
    "what_happens_next": {
      "if_approved": "Full refund processed immediately, customer retains product (no return required for defects)",
      "if_rejected": "Customer offered alternative resolution, case escalated if customer insists",
      "if_partial": "Partial refund or store credit offered as compromise"
    }
  },
  "options": [
    {
      "option_id": "approve_full",
      "label": "Approve Full Refund",
      "description": "Process $2,847.00 refund to original payment method",
      "consequences": "Customer retains as satisfied, $2,847 cost to company, positive retention impact",
      "recommended": true,
      "recommendation_reason": "VIP customer within extended return window, low refund history, high retention risk given competitor activity"
    },
    {
      "option_id": "approve_conditional",
      "label": "Approve with Return Required",
      "description": "Approve refund contingent on product return for defect verification",
      "consequences": "Refund delayed until return received, may frustrate customer",
      "recommended": false
    },
    {
      "option_id": "partial_refund",
      "label": "Offer Partial Refund",
      "description": "Offer 50% refund ($1,423.50) as compromise",
      "consequences": "Lower cost, customer may accept or escalate",
      "recommended": false,
      "requires_input": true,
      "input_prompt": "What percentage refund to offer?"
    },
    {
      "option_id": "store_credit",
      "label": "Offer Store Credit",
      "description": "Full value as store credit instead of refund",
      "consequences": "Retains revenue, customer may accept given VIP status benefits",
      "recommended": false
    },
    {
      "option_id": "reject",
      "label": "Deny Refund",
      "description": "Decline refund request",
      "consequences": "High churn risk for VIP customer, potential negative review",
      "recommended": false,
      "requires_input": true,
      "input_prompt": "Please provide reason for denial to share with customer"
    }
  ],
  "risk_assessment": {
    "level": "high",
    "factors": [
      "VIP customer churn risk if denied",
      "Financial impact: $2,847",
      "No defect documentation to verify claim",
      "Competitor activity increases flight risk"
    ],
    "reversibility": "irreversible",
    "impact_scope": "Single customer, but VIP segment retention metrics affected",
    "compliance_notes": "VIP 60-day policy applies - customer is within extended window"
  },
  "supporting_information": {
    "data_summary": {
      "customer_ltv": "$12,500",
      "vip_tier": true,
      "refund_history": "1 refund ($150) in 12 months",
      "order_age_days": 45,
      "policy_window_days": 60,
      "refund_amount": "$2,847.00"
    },
    "similar_cases": [
      "Case #12456: Similar VIP refund approved, customer retained and spent $3K more",
      "Case #12102: VIP refund denied, customer churned, left negative review"
    ],
    "policies": [
      "Standard return window: 30 days",
      "VIP return window: 60 days",
      "Defect claims: Return required unless manager override",
      "Approval thresholds: <$500 auto, >$500 manager, >$5000 director"
    ]
  },
  "escalation": {
    "escalate_if": "Manager unavailable or requests director input",
    "escalate_to": "Director of Customer Service",
    "auto_escalate_after": "2024-01-15T17:00:00Z"
  },
  "audit_trail": {
    "events": [
      {
        "timestamp": "2024-01-15T10:15:00Z",
        "action": "refund_request_received",
        "actor": "customer"
      },
      {
        "timestamp": "2024-01-15T10:20:00Z",
        "action": "ai_verification_complete",
        "actor": "system",
        "details": "Order verified, VIP status confirmed, policy check complete"
      },
      {
        "timestamp": "2024-01-15T10:30:00Z",
        "action": "escalated_for_approval",
        "actor": "system",
        "details": "Amount exceeds auto-approve threshold"
      }
    ]
  }
}
```

## Gotchas

### Common Failure Modes
1. **Over-escalation**: Asking for approval on everything defeats the purpose
2. **Insufficient context**: Human can't decide without proper information
3. **Unclear options**: Ambiguous choices lead to confusion
4. **Missing urgency**: Not communicating time sensitivity

### Edge Cases to Handle
- **No response**: Auto-escalation or default action
- **Conflicting approvers**: Clear hierarchy needed
- **Partial approval**: Handle modified requests
- **Revoked approval**: Ability to undo if caught in time

### When NOT to Use This Prompt
- **Trivial decisions**: Don't waste human time on low-stakes items
- **Time-critical**: When delay is unacceptable
- **Fully automated flows**: Where human approval not required
- **No appropriate approver**: Need defined escalation path

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex approval workflows | Best context synthesis |
| **Acceptable:** Claude Sonnet 4 | Standard approvals | Good clarity |
| **Acceptable:** GPT-4o | Decision preparation | Strong formatting |
| **Caution:** Smaller models | - | May miss risk factors |

# Email Classification & Routing

## Use Case

Automatically classify incoming emails and route to appropriate teams/queues:
- Support ticket triage
- Sales lead qualification
- Inquiry categorization
- Priority assignment
- Auto-response selection

Use when handling high-volume email where consistent categorization and fast routing matter.

## Input Format

**Required:**
- `email_subject`: Email subject line
- `email_body`: Email body content (plain text)

**Optional:**
- `sender_email`: Sender's email address
- `sender_history`: Previous interactions with this sender
- `categories`: Custom category list (overrides defaults)
- `routing_rules`: Custom routing logic
- `attachments`: List of attachment filenames

## Output Format

```json
{
  "classification": {
    "primary_category": "support",
    "subcategory": "technical_issue",
    "confidence": 0.92
  },
  "priority": {
    "level": "high",
    "reasoning": "Production system affected",
    "sla_hours": 4
  },
  "routing": {
    "team": "technical_support",
    "queue": "tier2",
    "suggested_assignee": null
  },
  "sentiment": {
    "overall": "frustrated",
    "urgency_indicators": ["ASAP", "production down"],
    "escalation_risk": "medium"
  },
  "suggested_actions": [
    {
      "action": "auto_reply",
      "template": "support_acknowledgment",
      "delay_minutes": 0
    }
  ],
  "extracted_info": {
    "product_mentioned": "Enterprise Dashboard",
    "issue_type": "login_failure",
    "account_id": "ACC-12345"
  }
}
```

## The Prompt

```
You are an email classification system for a business. Analyze the incoming email and provide structured routing information.

EMAIL SUBJECT:
{{email_subject}}

EMAIL BODY:
{{email_body}}

{{#if sender_email}}
SENDER: {{sender_email}}
{{/if}}

{{#if sender_history}}
SENDER HISTORY:
{{sender_history}}
{{/if}}

{{#if attachments}}
ATTACHMENTS: {{attachments}}
{{/if}}

CLASSIFICATION CATEGORIES:
{{#if categories}}
{{categories}}
{{else}}
Primary categories:
- support: Customer needs help with product/service
- sales: Purchase inquiry, pricing, demos
- billing: Payment, invoices, account charges
- feedback: Product feedback, feature requests
- complaint: Dissatisfaction, escalation
- spam: Unsolicited, irrelevant
- internal: From internal employees
- partnership: Business development, integration requests
- legal: Legal notices, compliance
- other: Doesn't fit above categories

Subcategories (by primary):
support: technical_issue, how_to_question, account_access, bug_report, feature_help
sales: new_lead, existing_customer_upsell, pricing_inquiry, demo_request, rfp
billing: payment_issue, refund_request, invoice_question, subscription_change
{{/if}}

ROUTING RULES:
{{#if routing_rules}}
{{routing_rules}}
{{else}}
Default routing:
- support/technical_issue → technical_support/tier1
- support/bug_report → engineering/bugs
- sales/* → sales_team/inbound
- billing/* → finance/customer_billing
- complaint/* → customer_success/escalations
- legal/* → legal/inbox
{{/if}}

PRIORITY LEVELS:
- critical: Production down, security issue, legal deadline (SLA: 1 hour)
- high: Significant impact, paying customer, time-sensitive (SLA: 4 hours)
- medium: Standard request, normal urgency (SLA: 24 hours)
- low: General inquiry, no urgency (SLA: 48 hours)

ANALYSIS INSTRUCTIONS:

1. Read the full email to understand intent
2. Identify primary category and most specific subcategory
3. Assess priority based on:
   - Business impact mentioned
   - Customer tier (if known from history)
   - Urgency language used
   - Presence of deadlines
4. Determine sentiment and escalation risk
5. Extract key information for routing
6. Suggest immediate actions if applicable

CONFIDENCE GUIDELINES:
- 0.9+: Clear, unambiguous intent
- 0.7-0.9: High confidence with minor ambiguity
- 0.5-0.7: Moderate confidence, could fit multiple categories
- Below 0.5: Flag for manual review

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{email_subject}}` | string | Yes | The email subject line |
| `{{email_body}}` | string | Yes | The email body content |
| `{{sender_email}}` | string | No | Sender's email address |
| `{{sender_history}}` | string | No | Previous interactions summary |
| `{{categories}}` | string | No | Custom category definitions |
| `{{routing_rules}}` | string | No | Custom routing logic |
| `{{attachments}}` | array | No | List of attachment filenames |

## Examples

### Example 1: Clear Support Request

**Input:**
```
email_subject: Can't login to dashboard - URGENT
email_body: |
  Hi Support Team,

  Since this morning our entire team (15 people) cannot access the Enterprise Dashboard.
  We keep getting "Authentication Failed" errors even with correct passwords.

  We're in the middle of a critical project deadline and need this fixed ASAP.

  Account ID: ACC-12345
  Company: TechCorp Industries

  Please help!

  Sarah Chen
  IT Manager
  TechCorp Industries
sender_email: sarah.chen@techcorp.com
```

**Output:**
```json
{
  "classification": {
    "primary_category": "support",
    "subcategory": "account_access",
    "confidence": 0.96
  },
  "priority": {
    "level": "critical",
    "reasoning": "Multiple users affected (15), blocking critical project deadline, authentication system issue",
    "sla_hours": 1
  },
  "routing": {
    "team": "technical_support",
    "queue": "tier2",
    "suggested_assignee": null
  },
  "sentiment": {
    "overall": "urgent",
    "urgency_indicators": ["URGENT", "ASAP", "critical project deadline", "entire team"],
    "escalation_risk": "high"
  },
  "suggested_actions": [
    {
      "action": "auto_reply",
      "template": "critical_acknowledgment",
      "delay_minutes": 0
    },
    {
      "action": "alert",
      "template": "auth_system_check",
      "delay_minutes": 0
    }
  ],
  "extracted_info": {
    "product_mentioned": "Enterprise Dashboard",
    "issue_type": "authentication_failure",
    "account_id": "ACC-12345",
    "company_name": "TechCorp Industries",
    "users_affected": 15,
    "contact_role": "IT Manager"
  }
}
```

### Example 2: Ambiguous Sales/Support Mix

**Input:**
```
email_subject: Question about your product
email_body: |
  Hello,

  I came across your website and I'm interested in learning more. We currently
  use a competitor but having issues with reliability.

  A few questions:
  1. How does your uptime compare?
  2. What's the pricing for 50 users?
  3. Can you migrate our data from CompetitorX?

  Also, if we sign up, how quickly can we get started?

  Thanks,
  Mike
```

**Output:**
```json
{
  "classification": {
    "primary_category": "sales",
    "subcategory": "new_lead",
    "confidence": 0.82
  },
  "priority": {
    "level": "high",
    "reasoning": "Active buyer comparing solutions, competitor mentioned, specific user count indicates serious evaluation",
    "sla_hours": 4
  },
  "routing": {
    "team": "sales_team",
    "queue": "inbound",
    "suggested_assignee": null
  },
  "sentiment": {
    "overall": "curious",
    "urgency_indicators": ["how quickly can we get started"],
    "escalation_risk": "low"
  },
  "suggested_actions": [
    {
      "action": "auto_reply",
      "template": "sales_inquiry_response",
      "delay_minutes": 0
    },
    {
      "action": "crm_update",
      "template": "new_lead_50_users",
      "delay_minutes": 0
    }
  ],
  "extracted_info": {
    "product_mentioned": null,
    "issue_type": null,
    "account_id": null,
    "company_size": "50 users",
    "competitor_mentioned": "CompetitorX",
    "lead_temperature": "warm"
  }
}
```

### Example 3: Edge Case - Angry Customer Complaint

**Input:**
```
email_subject: THIS IS UNACCEPTABLE - CANCEL MY ACCOUNT
email_body: |
  I have been a customer for 3 YEARS and this is how you treat me???

  I was charged TWICE this month and nobody responds to my emails. I've sent
  THREE messages over the past week. Nothing.

  If I don't hear back TODAY with a full refund, I'm disputing with my bank
  AND leaving reviews everywhere.

  Account: premium-user-8821

  EXTREMELY DISAPPOINTED
sender_email: john.frustrated@email.com
sender_history: |
  - Customer since 2021
  - Premium tier ($299/mo)
  - Sent 3 unanswered tickets in past 7 days
  - LTV: $10,764
```

**Output:**
```json
{
  "classification": {
    "primary_category": "complaint",
    "subcategory": "billing_escalation",
    "confidence": 0.98,
    "secondary_category": "billing",
    "secondary_subcategory": "payment_issue"
  },
  "priority": {
    "level": "critical",
    "reasoning": "Long-term premium customer ($10k+ LTV), double-charged, multiple ignored tickets, threatening chargeback and public reviews, explicit deadline",
    "sla_hours": 1
  },
  "routing": {
    "team": "customer_success",
    "queue": "escalations",
    "suggested_assignee": "manager_on_duty"
  },
  "sentiment": {
    "overall": "angry",
    "urgency_indicators": ["THIS IS UNACCEPTABLE", "CANCEL", "TODAY", "disputing with my bank", "reviews everywhere"],
    "escalation_risk": "critical"
  },
  "suggested_actions": [
    {
      "action": "page_on_call",
      "template": "high_value_escalation",
      "delay_minutes": 0
    },
    {
      "action": "auto_reply",
      "template": "escalation_acknowledgment_personal",
      "delay_minutes": 0
    },
    {
      "action": "create_ticket",
      "template": "billing_investigation",
      "delay_minutes": 0
    }
  ],
  "extracted_info": {
    "product_mentioned": null,
    "issue_type": "double_charge",
    "account_id": "premium-user-8821",
    "customer_tenure": "3 years",
    "previous_tickets": 3,
    "churn_risk": "immediate",
    "ltv": 10764
  }
}
```

## Gotchas

### Common Failure Modes
1. **Multi-intent emails**: Customer asks sales AND support questions. Classify by primary intent, note secondary.
2. **Sarcasm/irony**: "Great job breaking the feature" reads positive out of context. Consider full email sentiment.
3. **Reply chains**: Email contains quoted replies. Focus on the new content, not quoted material.
4. **Signature pollution**: Contact info, legal disclaimers in signature. Don't over-weight this content.

### Edge Cases to Handle
- **Auto-generated emails**: OOO replies, delivery failures, system notifications
- **Encrypted/empty body**: Subject only, attachments only
- **Non-English**: Detect language, route to appropriate team
- **Internal vs external**: Same domain as company = internal

### When NOT to Use This Prompt
- **Transactional emails**: Order confirmations, shipping notifications (use rule-based)
- **Newsletter/marketing**: Bulk inbound (use spam filter first)
- **Encrypted content**: Cannot read body (route to security)
- **Very long threads**: Summarize first, then classify

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Sonnet 4 | High-volume production | Excellent speed/accuracy balance |
| **Best:** GPT-4o-mini | Very high volume | Cost-effective, good accuracy |
| **Acceptable:** Claude Haiku 3.5 | Massive scale | Fastest, for simpler routing |
| **Overkill:** Claude Opus 4.1 | - | Only for complex edge cases |

## Integration Notes

### Pre-filtering
```python
# Skip classification for obvious cases
def should_classify(email):
    # Skip auto-replies
    if email.headers.get('Auto-Submitted') == 'auto-replied':
        return False, 'auto_reply'

    # Skip delivery failures
    if email.sender.startswith('mailer-daemon@'):
        return False, 'delivery_failure'

    # Skip if already classified (forwarded)
    if '[CLASSIFIED:' in email.subject:
        return False, 'already_classified'

    return True, None
```

### Routing Integration
```python
# Apply routing decision
def route_email(classification_result):
    routing = classification_result['routing']
    priority = classification_result['priority']

    # Create ticket in helpdesk
    ticket = helpdesk.create(
        queue=routing['queue'],
        team=routing['team'],
        priority=priority['level'],
        sla_due=now() + timedelta(hours=priority['sla_hours'])
    )

    # Execute suggested actions
    for action in classification_result['suggested_actions']:
        if action['action'] == 'auto_reply':
            schedule_reply(
                template=action['template'],
                delay=action['delay_minutes']
            )
        elif action['action'] == 'page_on_call':
            pagerduty.trigger(action['template'])

    return ticket
```

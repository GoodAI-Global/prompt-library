# Report Generation

## Use Case

Generate structured business reports from raw data and context:
- Weekly/monthly status reports
- Executive summaries
- Progress reports
- Performance dashboards (narrative)
- Incident reports

Use when you need consistent, professional reporting that synthesizes data into narrative insights.

## Input Format

**Required:**
- `report_type`: status, executive_summary, progress, performance, incident
- `data`: Structured data to include in report (JSON, tables, or text)

**Optional:**
- `audience`: executive, technical, stakeholder, public
- `previous_report`: Content from last report for comparison
- `time_period`: Reporting period (e.g., "Week of Jan 15, 2024")
- `key_metrics`: Specific metrics to highlight
- `template`: Custom template or section requirements

## Output Format

```json
{
  "report": {
    "title": "Generated report title",
    "subtitle": "Time period or context",
    "generated_at": "2024-01-15T10:00:00Z",
    "report_type": "status",
    "audience": "executive"
  },
  "sections": [
    {
      "heading": "Section Title",
      "content": "Narrative content with insights",
      "highlights": ["Key point 1", "Key point 2"],
      "data_tables": [
        {
          "caption": "Table title",
          "headers": ["Col1", "Col2"],
          "rows": [["data", "data"]]
        }
      ]
    }
  ],
  "executive_summary": "2-3 sentence overview for quick scanning",
  "key_metrics": {
    "metric_name": {
      "value": 95,
      "unit": "%",
      "trend": "up",
      "vs_previous": "+5%"
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "recommendation": "Action to take",
      "rationale": "Why this matters"
    }
  ],
  "next_steps": ["Planned action 1", "Planned action 2"],
  "appendix": {
    "raw_data_summary": "Reference to source data",
    "methodology_notes": "How metrics were calculated"
  }
}
```

## The Prompt

```
You are a business report writer. Generate a professional report from the provided data.

REPORT TYPE: {{report_type}}
AUDIENCE: {{audience | default: "stakeholder"}}
TIME PERIOD: {{time_period}}

DATA:
{{data}}

{{#if previous_report}}
PREVIOUS REPORT FOR COMPARISON:
{{previous_report}}
{{/if}}

{{#if key_metrics}}
METRICS TO HIGHLIGHT:
{{key_metrics}}
{{/if}}

{{#if template}}
TEMPLATE/SECTIONS REQUIRED:
{{template}}
{{/if}}

REPORT WRITING GUIDELINES:

1. EXECUTIVE SUMMARY (always include)
   - 2-3 sentences maximum
   - Lead with the most important finding
   - Include one key metric and one key action
   - Audience should understand report value without reading further

2. SECTION STRUCTURE
   - Clear, descriptive headings
   - Lead each section with the key insight
   - Support with data (tables, metrics)
   - End with implications or actions

3. TONE BY AUDIENCE:
   {{#if audience == "executive"}}
   - Focus on outcomes, not process
   - Lead with business impact
   - Minimize technical jargon
   - Emphasize decisions needed
   {{/if}}
   {{#if audience == "technical"}}
   - Include technical details
   - Reference specific systems/components
   - Include methodology notes
   - Provide granular metrics
   {{/if}}
   {{#if audience == "stakeholder"}}
   - Balance detail with accessibility
   - Connect to project goals
   - Clear status indicators
   - Highlight risks and mitigations
   {{/if}}

4. DATA PRESENTATION
   - Use tables for comparative data
   - Highlight trends (↑ ↓ →)
   - Compare to previous period when available
   - Note any data limitations

5. REPORT TYPE SPECIFIC:
   {{#if report_type == "status"}}
   - Current state summary
   - Progress against milestones
   - Blockers and risks
   - Next period focus
   {{/if}}
   {{#if report_type == "executive_summary"}}
   - Strategic implications
   - Key decisions needed
   - Resource requirements
   - Competitive context if relevant
   {{/if}}
   {{#if report_type == "incident"}}
   - Incident timeline
   - Impact assessment
   - Root cause (if known)
   - Remediation steps
   - Prevention measures
   {{/if}}

6. METRICS FORMATTING
   - Include trend vs previous period
   - Use consistent units
   - Highlight against targets
   - RAG status where applicable (Red/Amber/Green)

7. RECOMMENDATIONS
   - Prioritize (high/medium/low)
   - Actionable and specific
   - Include rationale
   - Assign owner if appropriate

QUALITY STANDARDS:
- Professional, neutral tone
- Data-driven assertions
- Clear attribution of sources
- No speculation beyond data
- Acknowledge uncertainties

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{report_type}}` | string | Yes | Type: status, executive_summary, progress, performance, incident |
| `{{data}}` | string/JSON | Yes | Data to include in the report |
| `{{audience}}` | string | No | Target audience (default: stakeholder) |
| `{{previous_report}}` | string | No | Previous report for comparison |
| `{{time_period}}` | string | No | Reporting period |
| `{{key_metrics}}` | array | No | Specific metrics to highlight |
| `{{template}}` | string | No | Custom template requirements |

## Examples

### Example 1: Weekly Status Report

**Input:**
```
report_type: status
audience: stakeholder
time_period: "Week of January 15-19, 2024"
data: |
  Project: Platform Modernization
  Sprint: 8 of 12

  Completed this week:
  - User authentication migration (100%)
  - API gateway configuration (100%)
  - Performance testing round 1 (100%)

  In progress:
  - Database migration scripts (75%)
  - UI component library v2 (60%)

  Metrics:
  - Velocity: 34 points (target: 32)
  - Bug count: 12 open (down from 18)
  - Test coverage: 78% (target: 80%)
  - Uptime (staging): 99.2%

  Blockers:
  - Waiting on security review for API gateway (ETA: Jan 22)

  Risks:
  - Database migration complexity higher than estimated
  - Key developer (Sam) on PTO next week

previous_report: |
  Last week velocity: 28 points
  Bug count: 18 open
  Test coverage: 72%
```

**Output:**
```json
{
  "report": {
    "title": "Platform Modernization - Weekly Status",
    "subtitle": "Week of January 15-19, 2024 | Sprint 8 of 12",
    "generated_at": "2024-01-19T17:00:00Z",
    "report_type": "status",
    "audience": "stakeholder"
  },
  "executive_summary": "Strong sprint with velocity exceeding target (34 vs 32 points) and bug count reduced by 33%. Authentication and API gateway milestones completed. Primary concern: database migration complexity may impact Sprint 9 timeline.",
  "sections": [
    {
      "heading": "Sprint Progress",
      "content": "Sprint 8 closed with above-target velocity and three major milestones achieved. The team is now 67% through the overall project timeline with key infrastructure components in place.",
      "highlights": [
        "User authentication migration completed - enables SSO rollout",
        "API gateway fully configured - removes blockers for mobile team",
        "Performance testing validates <200ms response times"
      ],
      "data_tables": [
        {
          "caption": "Milestone Status",
          "headers": ["Milestone", "Status", "Notes"],
          "rows": [
            ["Authentication Migration", "✓ Complete", "Ahead of schedule"],
            ["API Gateway", "✓ Complete", "Pending security review"],
            ["Database Migration", "◐ 75%", "Complexity increased"],
            ["UI Component Library", "◐ 60%", "On track"]
          ]
        }
      ]
    },
    {
      "heading": "Key Metrics",
      "content": "All velocity and quality metrics showing positive trends. Test coverage approaching target with gap expected to close in Sprint 9.",
      "highlights": [
        "Velocity improved 21% week-over-week (28 → 34)",
        "Bug count reduced 33% (18 → 12)",
        "Test coverage up 6 percentage points"
      ],
      "data_tables": [
        {
          "caption": "Metrics Summary",
          "headers": ["Metric", "Current", "Target", "Trend", "Status"],
          "rows": [
            ["Velocity", "34 pts", "32 pts", "↑ +21%", "🟢"],
            ["Open Bugs", "12", "<15", "↓ -33%", "🟢"],
            ["Test Coverage", "78%", "80%", "↑ +6%", "🟡"],
            ["Staging Uptime", "99.2%", "99.5%", "→", "🟡"]
          ]
        }
      ]
    },
    {
      "heading": "Blockers & Risks",
      "content": "One active blocker pending external dependency. Two risks identified requiring mitigation planning.",
      "highlights": [
        "Security review for API gateway expected Jan 22",
        "Database migration scripts more complex than scoped",
        "Key developer unavailable next week"
      ],
      "data_tables": [
        {
          "caption": "Risk Register",
          "headers": ["Risk", "Impact", "Probability", "Mitigation"],
          "rows": [
            ["DB migration complexity", "Medium", "High", "Pair programming, scope review"],
            ["Sam PTO coverage", "Low", "Certain", "Knowledge transfer completed"]
          ]
        }
      ]
    }
  ],
  "key_metrics": {
    "velocity": {
      "value": 34,
      "unit": "points",
      "trend": "up",
      "vs_previous": "+21%",
      "vs_target": "+6%"
    },
    "bugs_open": {
      "value": 12,
      "unit": "count",
      "trend": "down",
      "vs_previous": "-33%"
    },
    "test_coverage": {
      "value": 78,
      "unit": "%",
      "trend": "up",
      "vs_previous": "+6%",
      "vs_target": "-2%"
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "recommendation": "Schedule database migration scope review before Sprint 9 planning",
      "rationale": "Complexity increase may require re-estimation and potential scope adjustment"
    },
    {
      "priority": "medium",
      "recommendation": "Follow up with Security team on API gateway review status",
      "rationale": "Blocking production deployment if delayed beyond Jan 22"
    }
  ],
  "next_steps": [
    "Complete database migration scripts (target: 100%)",
    "Continue UI component library development",
    "Begin security review remediation (if findings)",
    "Sprint 9 planning session (Jan 22)"
  ],
  "appendix": {
    "raw_data_summary": "Source: Jira Sprint 8 board, DataDog metrics dashboard",
    "methodology_notes": "Velocity calculated as story points completed. Test coverage from Jest/Istanbul reports."
  }
}
```

### Example 2: Executive Performance Summary

**Input:**
```
report_type: executive_summary
audience: executive
time_period: "Q4 2024"
key_metrics: ["revenue", "customer_satisfaction", "churn_rate", "nps"]
data: |
  Revenue:
  - Q4 actual: $4.2M
  - Q4 target: $4.0M
  - Q3 actual: $3.8M
  - YoY growth: 18%

  Customer Metrics:
  - NPS: 72 (up from 65 in Q3)
  - CSAT: 4.3/5.0
  - Churn rate: 2.1% monthly (down from 2.8% in Q3)
  - Support ticket volume: -15% QoQ

  Product:
  - New features shipped: 8
  - Customer-requested features: 5 of 8
  - Platform uptime: 99.95%

  Team:
  - Headcount: 45 (added 5 in Q4)
  - Employee satisfaction: 4.1/5.0
  - Attrition: 2 voluntary departures
```

**Output:**
```json
{
  "report": {
    "title": "Q4 2024 Executive Performance Summary",
    "subtitle": "Quarterly Business Review",
    "generated_at": "2025-01-05T10:00:00Z",
    "report_type": "executive_summary",
    "audience": "executive"
  },
  "executive_summary": "Q4 exceeded revenue target by 5% ($4.2M vs $4.0M) with 18% YoY growth. Customer health metrics significantly improved: NPS up 7 points, churn down 25%. Platform delivered 8 features with 99.95% uptime. Team scaled to 45 with controlled attrition.",
  "sections": [
    {
      "heading": "Financial Performance",
      "content": "Q4 represents the strongest quarter of the year, exceeding target and demonstrating accelerating growth trajectory. Revenue growth rate increased from 15% YoY in Q3 to 18% in Q4.",
      "highlights": [
        "$4.2M revenue vs $4.0M target (+5%)",
        "18% year-over-year growth",
        "10.5% quarter-over-quarter growth"
      ],
      "data_tables": [
        {
          "caption": "Revenue Performance",
          "headers": ["Period", "Actual", "Target", "Variance"],
          "rows": [
            ["Q4 2024", "$4.2M", "$4.0M", "+5%"],
            ["Q3 2024", "$3.8M", "$3.7M", "+3%"],
            ["Q4 2023", "$3.6M", "$3.5M", "+3%"]
          ]
        }
      ]
    },
    {
      "heading": "Customer Health",
      "content": "Significant improvement across all customer health indicators. NPS increase of 7 points indicates strengthening product-market fit. Churn reduction suggests improved retention from product investments.",
      "highlights": [
        "NPS improved from 65 to 72 (+7 points)",
        "Churn reduced from 2.8% to 2.1% monthly (-25%)",
        "Support volume down 15% despite customer growth"
      ],
      "data_tables": [
        {
          "caption": "Customer Metrics Trend",
          "headers": ["Metric", "Q4", "Q3", "Change"],
          "rows": [
            ["NPS", "72", "65", "↑ +7"],
            ["CSAT", "4.3/5.0", "4.1/5.0", "↑ +0.2"],
            ["Monthly Churn", "2.1%", "2.8%", "↓ -25%"],
            ["Support Tickets", "-15%", "baseline", "↓ improved"]
          ]
        }
      ]
    },
    {
      "heading": "Product Delivery",
      "content": "Strong product velocity with customer-centric prioritization. Majority of shipped features (5 of 8) directly from customer requests, indicating responsive roadmap execution.",
      "highlights": [
        "8 features shipped (5 customer-requested)",
        "99.95% platform uptime exceeded SLA",
        "Zero critical incidents in Q4"
      ]
    },
    {
      "heading": "Team & Operations",
      "content": "Successfully scaled team by 12% while maintaining engagement and limiting attrition. Employee satisfaction stable at 4.1 despite rapid growth.",
      "highlights": [
        "Grew from 40 to 45 headcount",
        "4.4% attrition rate (industry avg: 13%)",
        "Employee satisfaction at 4.1/5.0"
      ]
    }
  ],
  "key_metrics": {
    "revenue": {
      "value": 4.2,
      "unit": "M USD",
      "trend": "up",
      "vs_previous": "+10.5%",
      "vs_target": "+5%"
    },
    "nps": {
      "value": 72,
      "unit": "score",
      "trend": "up",
      "vs_previous": "+7 points"
    },
    "churn_rate": {
      "value": 2.1,
      "unit": "% monthly",
      "trend": "down",
      "vs_previous": "-25%"
    },
    "customer_satisfaction": {
      "value": 4.3,
      "unit": "/5.0",
      "trend": "up",
      "vs_previous": "+0.2"
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "recommendation": "Invest in customer success to capitalize on NPS momentum",
      "rationale": "NPS trajectory suggests opportunity to accelerate referral revenue"
    },
    {
      "priority": "medium",
      "recommendation": "Analyze churn reduction drivers for Q1 retention playbook",
      "rationale": "25% churn improvement is significant; codify learnings"
    }
  ],
  "next_steps": [
    "Q1 2025 planning with 20% revenue growth target",
    "Customer advisory board launch (February)",
    "Headcount plan for 55 by Q2"
  ],
  "appendix": {
    "raw_data_summary": "Sources: Salesforce (revenue), Delighted (NPS), Stripe (churn), Zendesk (support)",
    "methodology_notes": "Churn calculated as logo churn. NPS from transactional surveys post-support."
  }
}
```

### Example 3: Incident Report

**Input:**
```
report_type: incident
audience: technical
time_period: "January 15, 2024"
data: |
  Incident ID: INC-2024-0115
  Severity: P1
  Duration: 47 minutes (14:23 - 15:10 UTC)

  Timeline:
  - 14:23: Monitoring alerts for API latency spike
  - 14:25: On-call engineer paged
  - 14:28: Confirmed customer-facing impact
  - 14:32: Identified database connection pool exhaustion
  - 14:35: Escalated to database team
  - 14:42: Root cause identified - runaway query from batch job
  - 14:48: Batch job killed, connections recovering
  - 14:55: Latency returning to normal
  - 15:10: Full recovery confirmed, incident closed

  Impact:
  - 12,000 API requests failed (HTTP 503)
  - 450 unique customers affected
  - Payment processing delayed for 89 transactions
  - $0 revenue loss (all payments processed after recovery)

  Root Cause:
  - Batch reporting job deployed at 14:15
  - Query lacked pagination, attempted to scan 2M rows
  - Connection pool (100 connections) exhausted in 8 minutes
  - Cascading failure to all API endpoints

  Contributing Factors:
  - No connection pool monitoring alerts
  - Batch jobs not isolated from production pool
  - Query review not required for batch job deployments
```

**Output:**
```json
{
  "report": {
    "title": "Incident Report: Database Connection Pool Exhaustion",
    "subtitle": "INC-2024-0115 | P1 | January 15, 2024",
    "generated_at": "2024-01-15T16:00:00Z",
    "report_type": "incident",
    "audience": "technical"
  },
  "executive_summary": "47-minute P1 outage caused by unoptimized batch job exhausting database connection pool. 450 customers impacted with 12,000 failed requests. No revenue loss. Root cause: unpaginated query scanning 2M rows. Immediate fix applied; systemic improvements identified.",
  "sections": [
    {
      "heading": "Incident Timeline",
      "content": "Total duration from first alert to full recovery: 47 minutes. Time to identification: 19 minutes. Time to mitigation: 25 minutes.",
      "highlights": [
        "Alert-to-acknowledgment: 2 minutes",
        "Alert-to-root-cause: 19 minutes",
        "Alert-to-mitigation: 25 minutes"
      ],
      "data_tables": [
        {
          "caption": "Timeline of Events",
          "headers": ["Time (UTC)", "Event", "Actor"],
          "rows": [
            ["14:23", "Monitoring alerts - API latency spike", "System"],
            ["14:25", "On-call engineer paged", "PagerDuty"],
            ["14:28", "Customer impact confirmed", "On-call"],
            ["14:32", "Identified DB connection pool exhaustion", "On-call"],
            ["14:35", "Escalated to database team", "On-call"],
            ["14:42", "Root cause identified - runaway batch query", "DB Team"],
            ["14:48", "Batch job terminated", "DB Team"],
            ["14:55", "Latency returning to normal", "System"],
            ["15:10", "Full recovery confirmed, incident closed", "On-call"]
          ]
        }
      ]
    },
    {
      "heading": "Impact Assessment",
      "content": "Customer-facing impact was significant but contained. No permanent data loss or revenue impact due to idempotent payment processing.",
      "highlights": [
        "12,000 API requests returned 503 errors",
        "450 unique customers experienced failures",
        "89 payment transactions delayed (all recovered)"
      ],
      "data_tables": [
        {
          "caption": "Impact Summary",
          "headers": ["Metric", "Value", "Severity"],
          "rows": [
            ["Failed Requests", "12,000", "High"],
            ["Customers Affected", "450", "Medium"],
            ["Delayed Payments", "89", "Medium"],
            ["Revenue Loss", "$0", "None"],
            ["Data Loss", "None", "None"]
          ]
        }
      ]
    },
    {
      "heading": "Root Cause Analysis",
      "content": "A batch reporting job deployed at 14:15 contained a query without pagination that attempted to scan 2 million rows. This query held connections open, exhausting the 100-connection pool within 8 minutes. With no available connections, all API endpoints began returning 503 errors.",
      "highlights": [
        "Trigger: Batch job deployed at 14:15 with unoptimized query",
        "Mechanism: Unpaginated query scanning 2M rows",
        "Failure: 100-connection pool exhausted in 8 minutes",
        "Cascade: All API endpoints failed due to shared pool"
      ],
      "data_tables": [
        {
          "caption": "Contributing Factors",
          "headers": ["Factor", "Gap Identified", "Classification"],
          "rows": [
            ["Monitoring", "No connection pool utilization alerts", "Detection"],
            ["Architecture", "Batch and API share connection pool", "Design"],
            ["Process", "No query review for batch deployments", "Process"]
          ]
        }
      ]
    },
    {
      "heading": "Remediation",
      "content": "Immediate fix applied by terminating the batch job. Short-term and long-term improvements identified to prevent recurrence.",
      "highlights": [
        "Immediate: Batch job terminated, connections recovered",
        "Short-term: Add connection pool monitoring",
        "Long-term: Isolate batch job database connections"
      ],
      "data_tables": [
        {
          "caption": "Action Items",
          "headers": ["Action", "Owner", "Priority", "ETA"],
          "rows": [
            ["Add connection pool alerts (<80% threshold)", "SRE Team", "P1", "Jan 16"],
            ["Fix batch query with pagination", "Data Team", "P1", "Jan 16"],
            ["Implement separate connection pool for batch", "Platform", "P2", "Jan 31"],
            ["Add query review to batch deployment checklist", "Data Team", "P2", "Jan 22"]
          ]
        }
      ]
    }
  ],
  "key_metrics": {
    "duration": {
      "value": 47,
      "unit": "minutes"
    },
    "time_to_detect": {
      "value": 0,
      "unit": "minutes",
      "note": "Automated detection"
    },
    "time_to_mitigate": {
      "value": 25,
      "unit": "minutes"
    },
    "customers_affected": {
      "value": 450,
      "unit": "customers"
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "recommendation": "Implement connection pool monitoring with <80% utilization alert",
      "rationale": "Would have provided 2-3 minute earlier warning before exhaustion"
    },
    {
      "priority": "high",
      "recommendation": "Isolate batch job database connections from production API pool",
      "rationale": "Prevents batch workloads from impacting customer-facing traffic"
    },
    {
      "priority": "medium",
      "recommendation": "Require query review and explain plan for batch jobs touching >10k rows",
      "rationale": "Process gate to catch problematic queries before deployment"
    }
  ],
  "next_steps": [
    "Complete P1 remediation items by Jan 16",
    "Schedule incident retrospective for Jan 17",
    "Update runbook with connection pool troubleshooting",
    "Review all batch jobs for similar query patterns"
  ],
  "appendix": {
    "raw_data_summary": "Sources: DataDog metrics, PostgreSQL logs, deployment pipeline",
    "methodology_notes": "Customer impact calculated from unique API keys in 503 responses"
  }
}
```

## Gotchas

### Common Failure Modes
1. **Data gaps assumed**: Don't invent data. If metric not provided, exclude or note "data not available."
2. **Causal overclaiming**: "Revenue increased because..." requires evidence. Use "correlated with" if unsure.
3. **Trend extrapolation**: Two points don't make a trend. Be careful with directional claims.
4. **Jargon mismatch**: Executive audience gets business terms; technical audience gets system terms.

### Edge Cases to Handle
- **Incomplete data**: Generate what's possible, clearly note gaps
- **Conflicting data**: Flag discrepancies, don't silently choose one
- **Negative trends**: Report honestly, frame constructively
- **Sensitive information**: Follow data classification guidelines

### When NOT to Use This Prompt
- **Real-time dashboards**: Reports are point-in-time; dashboards need different approach
- **Regulatory filings**: Legal/compliance reports need specialized review
- **Financial statements**: Auditable financials need structured templates
- **Performance reviews**: HR documents need different format and tone

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Executive summaries | Best synthesis and insight |
| **Best:** GPT-4o | Complex data narratives | Strong analytical framing |
| **Acceptable:** Claude Sonnet 4 | Standard reports | Good balance |
| **Acceptable:** GPT-4o-mini | High volume, simple reports | Cost-effective |
| **Not Recommended:** Smaller models | - | Miss nuanced analysis |

## Integration Notes

### Output Formatting
```python
def to_markdown(report_json):
    """Convert JSON report to Markdown"""
    md = f"# {report_json['report']['title']}\n"
    md += f"*{report_json['report']['subtitle']}*\n\n"

    md += f"## Executive Summary\n{report_json['executive_summary']}\n\n"

    for section in report_json['sections']:
        md += f"## {section['heading']}\n"
        md += f"{section['content']}\n\n"

        if section.get('highlights'):
            for h in section['highlights']:
                md += f"- {h}\n"
            md += "\n"

        if section.get('data_tables'):
            for table in section['data_tables']:
                md += f"**{table['caption']}**\n\n"
                md += "| " + " | ".join(table['headers']) + " |\n"
                md += "| " + " | ".join(["---"] * len(table['headers'])) + " |\n"
                for row in table['rows']:
                    md += "| " + " | ".join(row) + " |\n"
                md += "\n"

    return md

def to_slides(report_json):
    """Generate slide-friendly format (Markdown sections)"""
    slides = []

    # Title slide
    slides.append({
        "title": report_json['report']['title'],
        "subtitle": report_json['report']['subtitle'],
        "type": "title"
    })

    # Executive summary slide
    slides.append({
        "title": "Executive Summary",
        "bullets": [report_json['executive_summary']],
        "type": "content"
    })

    # Key metrics slide
    if report_json.get('key_metrics'):
        metrics_bullets = []
        for name, data in report_json['key_metrics'].items():
            trend = data.get('trend', '')
            vs_prev = data.get('vs_previous', '')
            metrics_bullets.append(f"{name}: {data['value']}{data.get('unit', '')} ({vs_prev})")
        slides.append({
            "title": "Key Metrics",
            "bullets": metrics_bullets,
            "type": "metrics"
        })

    return slides
```

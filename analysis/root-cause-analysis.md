# Root Cause Analysis

## Use Case

Structure and facilitate root cause analysis for problems and incidents:
- Incident post-mortems
- Quality issue investigation
- Performance problem diagnosis
- Process failure analysis

Use when you need systematic problem-solving to identify underlying causes and prevent recurrence.

## Input Format

**Required:**
- `problem_statement`: Clear description of the problem
- `evidence`: Available data, observations, and findings

**Optional:**
- `timeline`: Chronological sequence of events
- `system_context`: System architecture or process description
- `previous_analysis`: Any prior investigation findings
- `constraints`: Known constraints on solutions

## Output Format

```json
{
  "analysis_summary": {
    "problem_id": "RCA-2024-001",
    "analysis_date": "2024-01-15",
    "problem_statement": "Concise problem description",
    "severity": "high",
    "status": "root_cause_identified"
  },
  "problem_definition": {
    "what": "What happened",
    "where": "Where it occurred",
    "when": "When it occurred",
    "extent": "How widespread"
  },
  "causal_chain": [
    {
      "level": "direct_cause",
      "cause": "What directly caused the problem",
      "evidence": ["Supporting evidence"]
    },
    {
      "level": "contributing_cause",
      "cause": "What enabled the direct cause",
      "evidence": ["Supporting evidence"]
    },
    {
      "level": "root_cause",
      "cause": "The fundamental cause",
      "evidence": ["Supporting evidence"],
      "category": "process|people|technology|external"
    }
  ],
  "five_whys": {
    "why_1": {"question": "Why?", "answer": "Because..."},
    "why_2": {"question": "Why?", "answer": "Because..."},
    "...": "..."
  },
  "verification": {
    "test": "How to verify this is the root cause",
    "result": "pass|fail|pending"
  },
  "recommendations": {
    "immediate": [...],
    "short_term": [...],
    "long_term": [...]
  },
  "prevention": {
    "controls": ["Preventive controls"],
    "detection": ["Early warning mechanisms"]
  }
}
```

## The Prompt

```
You are a root cause analysis specialist. Guide systematic problem analysis to identify true underlying causes.

PROBLEM STATEMENT:
{{problem_statement}}

EVIDENCE:
{{evidence}}

{{#if timeline}}
TIMELINE:
{{timeline}}
{{/if}}

{{#if system_context}}
SYSTEM CONTEXT:
{{system_context}}
{{/if}}

{{#if previous_analysis}}
PREVIOUS ANALYSIS:
{{previous_analysis}}
{{/if}}

{{#if constraints}}
CONSTRAINTS:
{{constraints}}
{{/if}}

ROOT CAUSE ANALYSIS FRAMEWORK:

1. PROBLEM DEFINITION (5W1H)
   - What: Precisely what happened
   - Where: Location, system, component
   - When: Timeline, duration
   - Who: People/systems involved
   - How: Mechanism of failure
   - Extent: Scope and impact

2. EVIDENCE GATHERING
   Categorize evidence:
   - Direct observations
   - Data/metrics
   - Logs/records
   - Interviews/statements
   - Physical evidence

   Note gaps:
   - What evidence is missing?
   - What would help confirm/refute hypotheses?

3. CAUSAL ANALYSIS

   Five Whys technique:
   - Start with the problem
   - Ask "Why?" repeatedly
   - Stop when you reach actionable root cause
   - Each "Why" should be supported by evidence

   Causal chain levels:
   - Symptom: What was observed
   - Direct cause: Immediate trigger
   - Contributing causes: Enabling factors
   - Root cause: Fundamental issue that, if fixed, prevents recurrence

   Root cause categories:
   - Process: Missing/inadequate procedures
   - People: Training, awareness, behavior
   - Technology: System design, capacity, reliability
   - External: Vendor, environment, force majeure

4. HYPOTHESIS TESTING
   For each hypothesis:
   - State the proposed cause
   - List supporting evidence
   - List contradicting evidence
   - Identify verification method
   - Assess confidence

5. ROOT CAUSE VERIFICATION
   The root cause should:
   - Explain all symptoms
   - Be supported by evidence
   - Be actionable (can be addressed)
   - If fixed, prevent recurrence

   Verification tests:
   - Does removing this cause prevent the problem?
   - Does introducing this cause reproduce the problem?
   - Does it explain why it happened now vs. before?

6. RECOMMENDATIONS

   Immediate (containment):
   - Stop the bleeding
   - Protect from further damage
   - Communicate appropriately

   Short-term (correction):
   - Fix the specific issue
   - Address direct cause
   - Restore normal operation

   Long-term (prevention):
   - Address root cause
   - Implement systemic changes
   - Update processes/controls

7. PREVENTION FRAMEWORK

   Controls:
   - Eliminate: Remove the hazard entirely
   - Prevent: Make failure impossible
   - Detect: Catch problems early
   - Mitigate: Reduce impact if failure occurs

   Defense layers:
   - Technical controls
   - Process controls
   - Human controls
   - Monitoring/alerting

OUTPUT REQUIREMENTS:
- Clear problem definition
- Evidence-based causal chain
- Verified root cause with supporting evidence
- Actionable recommendations
- Prevention measures

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{problem_statement}}` | string | Yes | Clear description of the problem |
| `{{evidence}}` | string | Yes | Data, observations, findings |
| `{{timeline}}` | string | No | Chronological sequence |
| `{{system_context}}` | string | No | System or process description |
| `{{previous_analysis}}` | string | No | Prior investigation findings |
| `{{constraints}}` | string | No | Known constraints |

## Examples

### Example 1: System Outage RCA

**Input:**
```
problem_statement: |
  Production database became unavailable for 47 minutes on January 15, 2024,
  causing complete service outage affecting all customers.

evidence: |
  OBSERVATIONS:
  - Database server stopped responding at 14:23 UTC
  - Failover to secondary did not occur
  - Application servers returned 500 errors to all requests
  - Manual database restart required
  - Service restored at 15:10 UTC

  METRICS:
  - CPU usage spiked to 100% at 14:20
  - Memory usage was stable at 75%
  - Disk I/O maxed out from 14:18-14:23
  - Connection pool exhausted at 14:22

  LOGS:
  - Database slow query log shows query ID #77821 running for 180 seconds
  - Query was a report generation query with no timeout
  - Query lacked index on date_range field
  - 5,000 users were active when issue started

  CONFIGURATION:
  - Automatic failover was enabled but health check interval was 120 seconds
  - Query timeout was not configured (default: unlimited)
  - Connection pool max was 100

timeline: |
  14:15 - Report generation triggered by scheduled job
  14:18 - Query #77821 starts, begins full table scan
  14:20 - CPU spikes as query consumes resources
  14:22 - Connection pool exhausted, new requests fail
  14:23 - Database stops responding
  14:25 - Monitoring alert fires (health check failed)
  14:27 - On-call engineer paged
  14:35 - Engineer begins investigation
  14:50 - Root cause identified, decision to restart
  14:55 - Database restart initiated
  15:05 - Database online, connections recovering
  15:10 - Service fully restored

system_context: |
  - PostgreSQL 14 on AWS RDS
  - Primary-replica configuration with automatic failover
  - Connected to 3 application servers
  - Health checks via TCP connection (not query-based)
```

**Output:**
```json
{
  "analysis_summary": {
    "problem_id": "RCA-2024-0115",
    "analysis_date": "2024-01-15",
    "problem_statement": "47-minute production database outage caused by unoptimized report query exhausting database resources",
    "severity": "critical",
    "status": "root_cause_identified",
    "total_impact": "47 minutes downtime, all customers affected"
  },
  "problem_definition": {
    "what": "Production database became unresponsive, causing complete service outage",
    "where": "Primary PostgreSQL database on AWS RDS",
    "when": {
      "started": "2024-01-15T14:23:00Z",
      "ended": "2024-01-15T15:10:00Z",
      "duration": "47 minutes"
    },
    "who": {
      "triggered_by": "Scheduled report generation job",
      "affected": "All customers (approximately 5,000 active users)"
    },
    "how": "Resource-intensive query consumed all database capacity, preventing other queries from executing",
    "extent": "Complete service unavailability, 100% of requests failed"
  },
  "causal_chain": [
    {
      "level": "symptom",
      "description": "Application returning 500 errors to all requests",
      "timestamp": "14:23"
    },
    {
      "level": "direct_cause",
      "cause": "Database connection pool exhausted and database stopped responding",
      "evidence": [
        "Connection pool (100 max) fully consumed at 14:22",
        "Database health check failed at 14:23"
      ]
    },
    {
      "level": "contributing_cause_1",
      "cause": "Single query consumed all database resources for 5+ minutes",
      "evidence": [
        "Query #77821 ran for 180+ seconds",
        "CPU at 100%, I/O maxed during query execution",
        "Query used full table scan (no index on date_range)"
      ]
    },
    {
      "level": "contributing_cause_2",
      "cause": "No query timeout configured to kill runaway queries",
      "evidence": [
        "Database query timeout set to default (unlimited)",
        "Query allowed to run indefinitely"
      ]
    },
    {
      "level": "contributing_cause_3",
      "cause": "Automatic failover did not trigger in time",
      "evidence": [
        "Health check interval was 120 seconds",
        "Primary was degraded but TCP connection still open",
        "TCP health check insufficient to detect query-level issues"
      ]
    },
    {
      "level": "root_cause",
      "cause": "Report generation query executed without performance safeguards",
      "evidence": [
        "Query lacked necessary index (date_range field)",
        "No query timeout to limit execution time",
        "Report job had full database access without resource limits"
      ],
      "category": "process_and_technology",
      "explanation": "The system allowed a poorly-optimized query to run without any guardrails. The combination of missing index, no timeout, and unlimited resource access allowed a single query to consume all database capacity."
    }
  ],
  "five_whys": {
    "why_1": {
      "question": "Why did the service go down?",
      "answer": "Because the database stopped responding to queries"
    },
    "why_2": {
      "question": "Why did the database stop responding?",
      "answer": "Because one query consumed all CPU and I/O resources"
    },
    "why_3": {
      "question": "Why did one query consume all resources?",
      "answer": "Because it performed a full table scan without an index and had no timeout"
    },
    "why_4": {
      "question": "Why was there no index and no timeout?",
      "answer": "Because the query was not reviewed for performance, and system defaults don't include protective limits"
    },
    "why_5": {
      "question": "Why wasn't the query reviewed and why are there no system limits?",
      "answer": "Because we lack mandatory query review process and haven't implemented database-level resource governance"
    },
    "root_cause_reached": "Lack of query performance review process and database resource governance allowed unoptimized query to impact production"
  },
  "verification": {
    "test": "Add index to date_range field and set query timeout - verify similar query completes in <1 second",
    "result": "pending",
    "additional_verification": [
      "Reproduce issue in staging with the same query (passed - confirmed table scan)",
      "Test with index added (pending)",
      "Verify timeout kills long-running queries (pending)"
    ]
  },
  "contributing_factors": [
    {
      "factor": "Health check configuration",
      "detail": "120-second interval with TCP-only check missed degradation",
      "impact": "Delayed automatic failover that could have reduced outage duration"
    },
    {
      "factor": "Shared connection pool",
      "detail": "Report job used same connection pool as production traffic",
      "impact": "Allowed report to starve production queries of connections"
    },
    {
      "factor": "Monitoring gap",
      "detail": "Alert didn't fire until database was completely unresponsive",
      "impact": "5-minute window between degradation and alert"
    }
  ],
  "recommendations": {
    "immediate": [
      {
        "action": "Add index on date_range field",
        "owner": "DBA",
        "deadline": "Today",
        "status": "in_progress"
      },
      {
        "action": "Set statement_timeout to 30 seconds on production database",
        "owner": "DBA",
        "deadline": "Today",
        "status": "pending"
      },
      {
        "action": "Pause scheduled report job until fix verified",
        "owner": "Engineering",
        "deadline": "Immediate",
        "status": "complete"
      }
    ],
    "short_term": [
      {
        "action": "Implement query-based health checks (not just TCP)",
        "owner": "SRE",
        "deadline": "This week",
        "rationale": "Enable faster failover detection"
      },
      {
        "action": "Configure separate connection pool for batch/report jobs",
        "owner": "Engineering",
        "deadline": "This week",
        "rationale": "Isolate report workload from production traffic"
      },
      {
        "action": "Add query duration monitoring and alerting",
        "owner": "SRE",
        "deadline": "This week",
        "rationale": "Alert before queries cause outage"
      }
    ],
    "long_term": [
      {
        "action": "Implement mandatory query review for batch jobs",
        "owner": "Engineering Manager",
        "deadline": "30 days",
        "rationale": "Prevent unoptimized queries from reaching production"
      },
      {
        "action": "Implement database resource governance (pg_stat_statements, resource quotas)",
        "owner": "DBA",
        "deadline": "30 days",
        "rationale": "System-level protection against resource abuse"
      },
      {
        "action": "Move heavy reports to read replica",
        "owner": "Engineering",
        "deadline": "60 days",
        "rationale": "Completely isolate report workload from primary"
      }
    ]
  },
  "prevention": {
    "controls": [
      {
        "type": "prevent",
        "control": "Query timeout on all database connections (30s max)",
        "effectiveness": "high",
        "implementation": "Database configuration change"
      },
      {
        "type": "prevent",
        "control": "Mandatory query plan review for new batch jobs",
        "effectiveness": "medium",
        "implementation": "Code review checklist"
      },
      {
        "type": "detect",
        "control": "Query duration monitoring with alert at 10 seconds",
        "effectiveness": "high",
        "implementation": "Monitoring enhancement"
      },
      {
        "type": "mitigate",
        "control": "Faster failover (30-second health check, query-based)",
        "effectiveness": "medium",
        "implementation": "RDS configuration change"
      }
    ],
    "defense_in_depth": [
      "Layer 1: Query review prevents bad queries from deploying",
      "Layer 2: Query timeout kills runaway queries",
      "Layer 3: Monitoring alerts before impact",
      "Layer 4: Separate connection pool limits blast radius",
      "Layer 5: Faster failover reduces outage duration"
    ]
  },
  "lessons_learned": [
    "Default database configurations are not production-safe",
    "Batch jobs need resource isolation from production workloads",
    "Health checks need to reflect actual service health, not just connectivity",
    "Query review should be required for jobs touching production data"
  ],
  "follow_up": {
    "verification_deadline": "2024-01-16",
    "review_meeting": "2024-01-17",
    "action_tracking": "JIRA ticket RCA-2024-0115"
  }
}
```

## Gotchas

### Common Failure Modes
1. **Stopping at symptoms**: "Database crashed" is not a root cause.
2. **Blame-focused**: "Operator error" doesn't prevent recurrence.
3. **Single cause bias**: Often multiple factors contribute.
4. **Action without verification**: Ensure proposed fix addresses actual root cause.

### Edge Cases to Handle
- **Multiple root causes**: Some problems have several independent causes
- **Unknown causes**: Sometimes root cause can't be determined
- **Recurring issues**: May indicate prior RCA was incomplete
- **External causes**: Limited control over external factors

### When NOT to Use This Prompt
- **Active incidents**: Focus on resolution first
- **Legal/compliance investigations**: Need formal methodology
- **Simple problems**: Don't over-engineer obvious fixes
- **Human error focus**: Use "Just Culture" approaches instead

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex multi-factor | Best causal reasoning |
| **Acceptable:** Claude Sonnet 4 | Standard RCA | Good structured analysis |
| **Acceptable:** GPT-4o | Technical incidents | Strong technical detail |
| **Caution:** Smaller models | - | May miss deeper causes |

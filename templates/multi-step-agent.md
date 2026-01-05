# Multi-Step Agent Patterns

## Use Case

Design prompts for complex multi-step task execution:
- Task decomposition and planning
- Step-by-step execution with checkpoints
- Dynamic replanning based on results
- Progress tracking and reporting
- Error recovery and continuation

Use when building agents that need to complete complex, multi-step workflows autonomously.

## Input Format

**Required:**
- `task`: The overall task to accomplish
- `capabilities`: What actions/tools the agent can perform

**Optional:**
- `constraints`: Limitations on execution
- `context`: Relevant background information
- `checkpoint_frequency`: How often to report progress
- `max_steps`: Maximum steps allowed

## Output Format

```json
{
  "task_analysis": {
    "objective": "Clear statement of the goal",
    "complexity": "simple|moderate|complex",
    "estimated_steps": 5,
    "potential_challenges": ["Challenge 1", "Challenge 2"]
  },
  "execution_plan": {
    "phases": [
      {
        "phase_id": 1,
        "name": "Phase name",
        "objective": "What this phase accomplishes",
        "steps": [
          {
            "step_id": "1.1",
            "action": "Specific action to take",
            "expected_output": "What this produces",
            "success_criteria": "How to know it worked",
            "dependencies": []
          }
        ],
        "checkpoint": {
          "validate": "What to check before proceeding",
          "rollback_if": "Condition that triggers rollback"
        }
      }
    ],
    "critical_path": ["Step IDs that must succeed"],
    "parallel_opportunities": ["Steps that can run together"]
  },
  "execution_state": {
    "current_phase": 1,
    "current_step": "1.1",
    "completed_steps": [],
    "status": "planning|executing|blocked|completed|failed",
    "progress_percentage": 0
  },
  "contingency_plans": {
    "if_step_fails": {
      "retry_count": 2,
      "fallback_action": "Alternative approach",
      "escalation": "When to ask for help"
    },
    "if_blocked": "What to do if stuck",
    "if_timeout": "Action if taking too long"
  },
  "completion_criteria": {
    "success": ["All conditions for success"],
    "partial_success": ["Minimum acceptable outcome"],
    "failure": ["Conditions that mean task failed"]
  }
}
```

## The Prompt

```
You are an autonomous agent that breaks down complex tasks into manageable steps and executes them systematically.

TASK:
{{task}}

AVAILABLE CAPABILITIES:
{{capabilities}}

{{#if constraints}}
CONSTRAINTS:
{{constraints}}
{{/if}}

{{#if context}}
CONTEXT:
{{context}}
{{/if}}

MAX STEPS: {{max_steps | default: 20}}
CHECKPOINT FREQUENCY: {{checkpoint_frequency | default: "after_each_phase"}}

AGENT EXECUTION FRAMEWORK:

1. TASK ANALYSIS
   Before executing:
   - Clearly state the objective
   - Identify what success looks like
   - Assess complexity and risks
   - Estimate number of steps needed

2. DECOMPOSITION STRATEGY
   Break the task into phases:
   - Each phase should have a clear objective
   - Phases should be logically ordered
   - Include validation checkpoints

   Break phases into steps:
   - Each step should be atomic (one action)
   - Define expected output for each step
   - Identify dependencies between steps
   - Mark steps that can run in parallel

3. STEP SPECIFICATION
   For each step, define:
   - Action: Exactly what to do
   - Input: What's needed to start
   - Output: What it produces
   - Validation: How to verify success
   - Dependencies: What must complete first
   - Rollback: How to undo if needed

4. EXECUTION RULES
   During execution:
   - Complete one step at a time
   - Validate output before proceeding
   - Update progress after each step
   - Report status at checkpoints
   - Handle errors immediately

5. ERROR HANDLING
   When something fails:
   - Identify what went wrong
   - Determine if retry makes sense
   - Consider alternative approaches
   - Escalate if stuck
   - Never proceed with invalid state

6. PROGRESS TRACKING
   Maintain state:
   - Current phase and step
   - List of completed steps
   - Outputs from each step
   - Time elapsed (if relevant)
   - Blockers or issues encountered

7. COMPLETION VERIFICATION
   When done:
   - Verify all success criteria met
   - Compile outputs from all steps
   - Report final status
   - Document lessons learned

EXECUTION PRINCIPLES:
- Plan before acting
- Verify before proceeding
- Fail fast, recover gracefully
- Keep the user informed
- Know when to ask for help

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{task}}` | string | Yes | Task to accomplish |
| `{{capabilities}}` | string | Yes | Available actions/tools |
| `{{constraints}}` | string | No | Execution limitations |
| `{{context}}` | string | No | Background information |
| `{{checkpoint_frequency}}` | string | No | How often to checkpoint |
| `{{max_steps}}` | number | No | Maximum allowed steps |

## Examples

### Example 1: Data Migration Task

**Input:**
```
task: |
  Migrate customer data from the legacy CRM (OldCRM) to the new system (NewCRM).
  There are approximately 10,000 customer records.
  Preserve all customer history and attachments.
  Validate data integrity after migration.

capabilities: |
  - query_oldcrm: Query records from legacy CRM
  - transform_record: Transform record to new format
  - insert_newcrm: Insert record into new CRM
  - validate_record: Compare records between systems
  - generate_report: Create migration report
  - send_notification: Send email notifications
  - rollback_batch: Undo a batch of inserts

constraints: |
  - Migration must complete within 4 hours
  - Process in batches of 500 records
  - Maintain referential integrity
  - Zero data loss tolerance
  - New CRM has rate limit of 100 inserts/minute

context: |
  - Migration scheduled for Saturday 2am-6am
  - Stakeholders: IT team, Sales ops, Customer success
  - Previous migration attempt failed at 60% due to encoding issues
  - Special handling needed for customers with non-ASCII characters

max_steps: 50
```

**Output:**
```json
{
  "task_analysis": {
    "objective": "Migrate 10,000 customer records from OldCRM to NewCRM with full history and attachments, ensuring data integrity",
    "complexity": "complex",
    "estimated_steps": 28,
    "potential_challenges": [
      "Rate limiting (100/min = 6000/hr, need 10k in 4hr)",
      "Non-ASCII character encoding issues (previous failure cause)",
      "Attachment transfer may be slow",
      "Rollback complexity if failure occurs mid-migration"
    ],
    "risk_mitigation": [
      "Process in batches with validation checkpoints",
      "Test encoding transformation on sample first",
      "Prioritize critical customers in early batches"
    ]
  },
  "execution_plan": {
    "phases": [
      {
        "phase_id": 1,
        "name": "Pre-Migration Validation",
        "objective": "Verify source data and prepare target system",
        "steps": [
          {
            "step_id": "1.1",
            "action": "Query OldCRM for record count and schema validation",
            "expected_output": "Confirmed 10,000 records, schema compatibility report",
            "success_criteria": "Count matches expected, no schema conflicts",
            "dependencies": []
          },
          {
            "step_id": "1.2",
            "action": "Test transform on 10 sample records including non-ASCII",
            "expected_output": "Transformed records with proper encoding",
            "success_criteria": "All special characters preserved correctly",
            "dependencies": ["1.1"]
          },
          {
            "step_id": "1.3",
            "action": "Verify NewCRM is ready (connection, permissions, space)",
            "expected_output": "NewCRM connectivity confirmed",
            "success_criteria": "Can insert and query test records",
            "dependencies": []
          }
        ],
        "checkpoint": {
          "validate": "All pre-checks passed, encoding test successful",
          "rollback_if": "Any pre-check fails"
        }
      },
      {
        "phase_id": 2,
        "name": "Batch Migration",
        "objective": "Migrate all records in controlled batches",
        "steps": [
          {
            "step_id": "2.1",
            "action": "Extract batch 1 (records 1-500) from OldCRM",
            "expected_output": "500 records extracted with history and attachments",
            "success_criteria": "Record count matches, all fields populated",
            "dependencies": ["1.2", "1.3"]
          },
          {
            "step_id": "2.2",
            "action": "Transform batch 1 to NewCRM format",
            "expected_output": "500 transformed records",
            "success_criteria": "No transformation errors, encoding correct",
            "dependencies": ["2.1"]
          },
          {
            "step_id": "2.3",
            "action": "Insert batch 1 into NewCRM (rate-limited)",
            "expected_output": "500 records inserted, IDs mapped",
            "success_criteria": "All inserts successful, no duplicates",
            "dependencies": ["2.2"]
          },
          {
            "step_id": "2.4",
            "action": "Validate batch 1 integrity",
            "expected_output": "Comparison report for batch 1",
            "success_criteria": "100% field match between source and target",
            "dependencies": ["2.3"]
          },
          {
            "step_id": "2.5-2.80",
            "action": "Repeat 2.1-2.4 for batches 2-20",
            "expected_output": "All 10,000 records migrated and validated",
            "success_criteria": "Each batch validates before proceeding",
            "dependencies": ["previous batch validated"]
          }
        ],
        "checkpoint": {
          "validate": "Batch validation passed, cumulative count correct",
          "rollback_if": "Batch validation fails - rollback that batch only"
        }
      },
      {
        "phase_id": 3,
        "name": "Post-Migration Validation",
        "objective": "Comprehensive verification of migration",
        "steps": [
          {
            "step_id": "3.1",
            "action": "Full count comparison OldCRM vs NewCRM",
            "expected_output": "Record counts match",
            "success_criteria": "10,000 records in both systems",
            "dependencies": ["2.80"]
          },
          {
            "step_id": "3.2",
            "action": "Sample validation of 100 random records",
            "expected_output": "Deep comparison report",
            "success_criteria": "All sampled records match exactly",
            "dependencies": ["3.1"]
          },
          {
            "step_id": "3.3",
            "action": "Verify all attachments accessible in NewCRM",
            "expected_output": "Attachment accessibility report",
            "success_criteria": "All attachment links valid",
            "dependencies": ["3.1"]
          },
          {
            "step_id": "3.4",
            "action": "Generate final migration report",
            "expected_output": "Comprehensive migration report",
            "success_criteria": "Report includes all metrics and validations",
            "dependencies": ["3.2", "3.3"]
          }
        ],
        "checkpoint": {
          "validate": "All validations pass",
          "rollback_if": "Critical discrepancies found"
        }
      },
      {
        "phase_id": 4,
        "name": "Completion & Notification",
        "objective": "Finalize migration and notify stakeholders",
        "steps": [
          {
            "step_id": "4.1",
            "action": "Send success notification to stakeholders",
            "expected_output": "Email sent with report attached",
            "success_criteria": "Email delivered",
            "dependencies": ["3.4"]
          }
        ],
        "checkpoint": {
          "validate": "Stakeholders notified",
          "rollback_if": "N/A - notification is final step"
        }
      }
    ],
    "critical_path": ["1.2", "2.1-2.4 (first batch)", "3.1", "3.2"],
    "parallel_opportunities": ["1.1 and 1.3", "3.2 and 3.3"]
  },
  "execution_state": {
    "current_phase": 1,
    "current_step": "1.1",
    "completed_steps": [],
    "status": "planning",
    "progress_percentage": 0
  },
  "contingency_plans": {
    "if_step_fails": {
      "retry_count": 2,
      "fallback_action": "Log error, skip record, add to exception queue for manual review",
      "escalation": "If >1% records fail, pause and alert IT team"
    },
    "if_blocked": "If rate limited, wait and retry with exponential backoff",
    "if_timeout": "If 3 hours elapsed and <80% complete, alert stakeholders for extension decision"
  },
  "completion_criteria": {
    "success": [
      "10,000 records migrated",
      "100% validation pass on sampled records",
      "All attachments accessible",
      "Migration report generated",
      "Stakeholders notified"
    ],
    "partial_success": [
      ">99% records migrated",
      "<100 records in exception queue",
      "Manual remediation plan documented"
    ],
    "failure": [
      ">1% records failed with no remediation path",
      "Data corruption detected",
      "Time limit exceeded with <90% complete"
    ]
  }
}
```

## Gotchas

### Common Failure Modes
1. **Over-planning**: Too many steps makes execution unwieldy
2. **Under-planning**: Missing critical steps discovered during execution
3. **Brittle dependencies**: One failure cascades through entire plan
4. **State management**: Losing track of where execution is

### Edge Cases to Handle
- **Partial completion**: How to resume from middle
- **External failures**: Network, API, or service outages
- **Data inconsistencies**: Unexpected data found during execution
- **Resource exhaustion**: Memory, time, or quota limits hit

### When NOT to Use This Prompt
- **Simple tasks**: Don't over-engineer single-step operations
- **Real-time requirements**: Multi-step planning adds latency
- **Highly dynamic**: When plans become obsolete quickly
- **User-driven**: Interactive tasks need different pattern

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex multi-phase tasks | Best planning and reasoning |
| **Acceptable:** Claude Sonnet 4 | Standard workflows | Good balance |
| **Acceptable:** GPT-4o | Detailed planning | Strong at decomposition |
| **Caution:** Smaller models | - | May miss dependencies |

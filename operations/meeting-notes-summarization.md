# Meeting Notes Summarization

## Use Case

Transform raw meeting transcripts or notes into actionable summaries:
- Executive summaries for stakeholders
- Action item extraction with owners and deadlines
- Decision documentation
- Follow-up tracking
- Meeting minutes generation

Use when you need consistent, scannable meeting documentation that drives action.

## Input Format

**Required:**
- `transcript`: Meeting transcript, notes, or recording transcription

**Optional:**
- `meeting_type`: standup, planning, review, brainstorm, decision, client, all_hands
- `attendees`: List of meeting participants
- `meeting_context`: Relevant background (project name, previous meeting link)
- `output_format`: summary, minutes, action_items_only, executive_brief

## Output Format

```json
{
  "meeting_summary": {
    "title": "Generated title based on content",
    "date": "2024-01-15",
    "duration_minutes": 45,
    "meeting_type": "planning",
    "attendees": ["Alice", "Bob", "Carol"]
  },
  "executive_summary": "2-3 sentence overview",
  "key_topics": [
    {
      "topic": "Topic name",
      "summary": "What was discussed",
      "outcome": "decision/discussion/deferred"
    }
  ],
  "decisions_made": [
    {
      "decision": "What was decided",
      "rationale": "Why",
      "decided_by": "Who made the call"
    }
  ],
  "action_items": [
    {
      "action": "What needs to be done",
      "owner": "Who is responsible",
      "deadline": "When it's due",
      "priority": "high/medium/low",
      "dependencies": ["Any blockers"]
    }
  ],
  "open_questions": [
    {
      "question": "Unresolved question",
      "assigned_to": "Who should answer",
      "due_date": "When answer needed"
    }
  ],
  "follow_up": {
    "next_meeting": "Date/time if scheduled",
    "items_for_next_meeting": ["Topics to revisit"]
  }
}
```

## The Prompt

```
You are a meeting documentation specialist. Transform the meeting transcript into a structured, actionable summary.

MEETING TRANSCRIPT:
{{transcript}}

{{#if meeting_type}}
MEETING TYPE: {{meeting_type}}
{{/if}}

{{#if attendees}}
ATTENDEES: {{attendees}}
{{/if}}

{{#if meeting_context}}
CONTEXT: {{meeting_context}}
{{/if}}

OUTPUT FORMAT: {{output_format | default: "summary"}}

SUMMARIZATION GUIDELINES:

1. EXECUTIVE SUMMARY (2-3 sentences max)
   - What was the meeting about?
   - What was the main outcome?
   - What's the most important next step?

2. KEY TOPICS
   - Group discussion into distinct topics
   - For each: what was discussed, what was the outcome
   - Outcomes: "decision" (concluded), "discussion" (explored, no conclusion), "deferred" (postponed)

3. DECISIONS MADE
   - Explicit decisions only (not suggestions or ideas)
   - Include who made/approved the decision
   - Note any dissent or conditions

4. ACTION ITEMS (be specific and actionable)
   - Start with verb: "Create...", "Review...", "Schedule..."
   - Must have clear owner (individual, not "the team")
   - Extract deadline if mentioned, otherwise mark "TBD"
   - Priority: high (blocking others), medium (this week), low (when possible)

5. OPEN QUESTIONS
   - Unresolved questions raised in meeting
   - Assign to most relevant person
   - Set due date if time-sensitive

6. FOLLOW-UP
   - Next meeting date if mentioned
   - Topics explicitly marked for follow-up

MEETING TYPE SPECIFIC GUIDANCE:

{{#if meeting_type == "standup"}}
Focus on: blockers, completed items, commitments for today
Skip: detailed discussion summaries
{{/if}}

{{#if meeting_type == "planning"}}
Focus on: sprint/cycle goals, capacity, commitments
Emphasize: action items with estimates
{{/if}}

{{#if meeting_type == "review"}}
Focus on: what was accomplished, demos given, feedback received
Emphasize: decisions on next steps
{{/if}}

{{#if meeting_type == "decision"}}
Focus on: options considered, decision rationale, dissent
Emphasize: final decision, implementation plan
{{/if}}

QUALITY STANDARDS:
- Use exact names mentioned (don't infer or guess)
- Preserve technical terms and project names exactly
- If deadline unclear, use "TBD" not a guess
- If owner unclear, use "Unassigned"
- Capture the substance, not filler conversation

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{transcript}}` | string | Yes | The meeting transcript or notes |
| `{{meeting_type}}` | string | No | Type of meeting for context-specific processing |
| `{{attendees}}` | array | No | List of meeting participants |
| `{{meeting_context}}` | string | No | Background context for the meeting |
| `{{output_format}}` | string | No | Desired output format (default: summary) |

## Examples

### Example 1: Sprint Planning Meeting

**Input:**
```
meeting_type: planning
transcript: |
  [Meeting started at 2:00 PM]

  Sarah: Alright everyone, let's kick off sprint 24 planning. We have two weeks.
  Alice, Bob, and I are fully available. Carol is out Thursday and Friday.

  Bob: Before we start - the API migration from last sprint is about 80% done.
  I need two more days to finish the authentication piece.

  Sarah: Okay, so that carries over. What's the priority this sprint?

  Alice: Product wants us to focus on the new dashboard. I broke it down into
  three parts: the widget framework, the data connectors, and the layout system.

  Sarah: How long for each?

  Alice: Widget framework is probably 5 days. Data connectors maybe 3. Layout
  system is smaller, 2 days, but it depends on the widget framework.

  Bob: I can help with data connectors once I'm done with the API migration.
  That's probably Wednesday.

  Carol: I can take the layout system, just need to coordinate with Alice on
  the framework interface. Can we define that by Tuesday?

  Alice: Yes, I'll have a draft interface by end of day Monday. Let's review
  Tuesday morning.

  Sarah: Perfect. So the plan is:
  - Bob finishes API migration by Wednesday
  - Alice does widget framework, interface draft by Monday
  - Bob picks up data connectors Thursday
  - Carol starts layout system after Tuesday's interface review

  What about the customer-reported bug with export?

  Bob: That's a quick fix. I can do it tomorrow morning, should take an hour.

  Sarah: Great, let's make that P1 since customers are waiting.

  Alice: One question - do we need design review for the dashboard?

  Sarah: Good point. I'll check with Design team and let you know by tomorrow.

  Sarah: Okay, I think we're set. Same time next week for mid-sprint check-in?

  All: Yes, works for us.

  [Meeting ended at 2:25 PM]
```

**Output:**
```json
{
  "meeting_summary": {
    "title": "Sprint 24 Planning - Dashboard Feature",
    "date": "2024-01-15",
    "duration_minutes": 25,
    "meeting_type": "planning",
    "attendees": ["Sarah", "Alice", "Bob", "Carol"]
  },
  "executive_summary": "Sprint 24 will focus on building the new dashboard (widget framework, data connectors, layout system) while completing the API migration carryover. Team committed to delivering all components with P1 bug fix for customer export issue.",
  "key_topics": [
    {
      "topic": "API Migration Carryover",
      "summary": "Migration is 80% complete, authentication piece needs 2 more days",
      "outcome": "decision"
    },
    {
      "topic": "New Dashboard Implementation",
      "summary": "Broken into three components: widget framework (5 days), data connectors (3 days), layout system (2 days). Dependencies mapped between Alice and Carol.",
      "outcome": "decision"
    },
    {
      "topic": "Export Bug Fix",
      "summary": "Customer-reported bug prioritized as P1",
      "outcome": "decision"
    },
    {
      "topic": "Design Review Requirement",
      "summary": "Need to confirm if design review required for dashboard",
      "outcome": "deferred"
    }
  ],
  "decisions_made": [
    {
      "decision": "Sprint 24 primary focus is new dashboard feature",
      "rationale": "Product priority",
      "decided_by": "Sarah (team consensus)"
    },
    {
      "decision": "Export bug is P1 priority",
      "rationale": "Customers are waiting",
      "decided_by": "Sarah"
    },
    {
      "decision": "Widget framework interface draft due Monday for Tuesday review",
      "rationale": "Enables Carol to start layout system",
      "decided_by": "Alice and Carol"
    }
  ],
  "action_items": [
    {
      "action": "Complete API migration authentication piece",
      "owner": "Bob",
      "deadline": "Wednesday",
      "priority": "high",
      "dependencies": []
    },
    {
      "action": "Fix customer export bug",
      "owner": "Bob",
      "deadline": "Tomorrow morning",
      "priority": "high",
      "dependencies": []
    },
    {
      "action": "Create widget framework interface draft",
      "owner": "Alice",
      "deadline": "Monday EOD",
      "priority": "high",
      "dependencies": []
    },
    {
      "action": "Build widget framework",
      "owner": "Alice",
      "deadline": "End of sprint",
      "priority": "medium",
      "dependencies": []
    },
    {
      "action": "Build data connectors",
      "owner": "Bob",
      "deadline": "End of sprint",
      "priority": "medium",
      "dependencies": ["API migration complete"]
    },
    {
      "action": "Build layout system",
      "owner": "Carol",
      "deadline": "End of sprint",
      "priority": "medium",
      "dependencies": ["Widget framework interface review"]
    },
    {
      "action": "Check with Design team about dashboard review requirement",
      "owner": "Sarah",
      "deadline": "Tomorrow",
      "priority": "medium",
      "dependencies": []
    }
  ],
  "open_questions": [
    {
      "question": "Is design review required for the dashboard?",
      "assigned_to": "Sarah",
      "due_date": "Tomorrow"
    }
  ],
  "follow_up": {
    "next_meeting": "Same time next week (mid-sprint check-in)",
    "items_for_next_meeting": ["Dashboard progress review", "Widget framework interface review (Tuesday)"]
  }
}
```

### Example 2: Client Meeting with Decisions

**Input:**
```
meeting_type: client
attendees: ["John (us)", "Maria (us)", "Tom Chen (Acme Corp)", "Lisa Park (Acme Corp)"]
transcript: |
  John: Thanks for joining, Tom and Lisa. Let's review the proposal and address
  your questions.

  Tom: We've reviewed the proposal. The scope looks good but we need to discuss
  timeline and pricing.

  Lisa: Specifically, you quoted 12 weeks but we have a board presentation in 10.
  Can you accelerate?

  John: We could potentially compress to 10 weeks but we'd need to start by
  February 1st and reduce the scope of Phase 2 testing.

  Tom: What would we lose with reduced testing?

  Maria: Instead of full regression testing, we'd do critical path only. About
  60% coverage versus 90%. We could do the remaining testing in a follow-on phase.

  Lisa: That's acceptable if we can schedule the follow-on before go-live.

  Tom: What's the cost impact?

  John: No change to the proposal price. We're absorbing the acceleration cost
  as a goodwill gesture given your long-term potential.

  Tom: That works for us. Let's proceed with the 10-week timeline.

  Lisa: What do you need from us to start February 1st?

  Maria: We need signed SOW by January 25th and access to your staging environment.

  Tom: I can get SOW signed by January 23rd. Lisa, can you handle environment
  access?

  Lisa: Yes, I'll create credentials and send by January 26th.

  John: Perfect. We'll send revised SOW with 10-week timeline by end of day
  tomorrow.

  Tom: One more thing - we'd like weekly status calls. Can you commit to that?

  John: Absolutely. We'll set up a recurring Thursday call.

  Lisa: 2 PM Eastern works best for our team.

  John: Done. Anything else before we wrap up?

  Tom: No, I think we're good. Looking forward to kicking off.

  John: Great, talk soon.
```

**Output:**
```json
{
  "meeting_summary": {
    "title": "Acme Corp Proposal Review - Timeline Acceleration",
    "date": "2024-01-15",
    "duration_minutes": null,
    "meeting_type": "client",
    "attendees": ["John (us)", "Maria (us)", "Tom Chen (Acme Corp)", "Lisa Park (Acme Corp)"]
  },
  "executive_summary": "Acme Corp approved the project with an accelerated 10-week timeline (vs 12 weeks) to meet their board presentation. Scope adjusted to critical path testing only with follow-on phase for full regression. Project kicks off February 1st.",
  "key_topics": [
    {
      "topic": "Timeline Acceleration",
      "summary": "Client requested 10-week timeline instead of 12 weeks due to board presentation deadline",
      "outcome": "decision"
    },
    {
      "topic": "Scope Adjustment",
      "summary": "Reduced Phase 2 testing from 90% to 60% coverage to accommodate timeline. Remaining testing moves to follow-on phase.",
      "outcome": "decision"
    },
    {
      "topic": "Pricing",
      "summary": "No price change for acceleration - absorbed as goodwill gesture",
      "outcome": "decision"
    },
    {
      "topic": "Project Kickoff Requirements",
      "summary": "Need signed SOW and staging environment access before Feb 1 start",
      "outcome": "decision"
    },
    {
      "topic": "Weekly Status Calls",
      "summary": "Recurring Thursday calls at 2 PM Eastern agreed",
      "outcome": "decision"
    }
  ],
  "decisions_made": [
    {
      "decision": "Project timeline compressed to 10 weeks",
      "rationale": "Client board presentation deadline",
      "decided_by": "Tom Chen (approved by all)"
    },
    {
      "decision": "Phase 2 testing reduced to 60% critical path coverage",
      "rationale": "Required to meet 10-week timeline, full testing in follow-on phase",
      "decided_by": "Tom Chen and Lisa Park"
    },
    {
      "decision": "No price change for acceleration",
      "rationale": "Goodwill gesture given long-term potential",
      "decided_by": "John"
    },
    {
      "decision": "Project start date: February 1st",
      "rationale": "Required for 10-week timeline completion before board presentation",
      "decided_by": "All parties"
    },
    {
      "decision": "Weekly status calls Thursdays at 2 PM Eastern",
      "rationale": "Client requested regular updates",
      "decided_by": "John (accepted Lisa's time preference)"
    }
  ],
  "action_items": [
    {
      "action": "Send revised SOW with 10-week timeline",
      "owner": "John",
      "deadline": "Tomorrow EOD",
      "priority": "high",
      "dependencies": []
    },
    {
      "action": "Sign and return SOW",
      "owner": "Tom Chen (Acme Corp)",
      "deadline": "January 23rd",
      "priority": "high",
      "dependencies": ["Receive revised SOW"]
    },
    {
      "action": "Create and send staging environment credentials",
      "owner": "Lisa Park (Acme Corp)",
      "deadline": "January 26th",
      "priority": "high",
      "dependencies": []
    },
    {
      "action": "Set up recurring Thursday status call (2 PM Eastern)",
      "owner": "John",
      "deadline": "Before February 1st",
      "priority": "medium",
      "dependencies": []
    },
    {
      "action": "Schedule follow-on phase for remaining testing before go-live",
      "owner": "Unassigned",
      "deadline": "TBD",
      "priority": "medium",
      "dependencies": ["Project kickoff"]
    }
  ],
  "open_questions": [],
  "follow_up": {
    "next_meeting": "First weekly status call after February 1st (Thursday, 2 PM Eastern)",
    "items_for_next_meeting": ["Project kickoff status", "Initial progress update"]
  }
}
```

### Example 3: Edge Case - Informal/Messy Transcript

**Input:**
```
transcript: |
  meeting started late, everyone was having coffee

  oh wait dave isn't here yet... ok he just joined

  Dave: sorry internet issues

  [cross-talk about weather]

  PM: ok lets get started. Last week we said we'd finish the feature but

  Dave: yeah I got blocked by the API issue

  PM: which api issue

  Dave: the one from that ticket... the auth one. mark said he'd fix it but

  Mark: i pushed a fix yesterday, did you try pulling?

  Dave: oh no let me check... [typing sounds]

  Dave: ok yeah the fix is there. I can finish today then

  PM: great. sarah how's the frontend

  Sarah: mostly done. waiting on dave's endpoint

  PM: ok so we should be done by wednesday?

  Sarah: ya probably thursday accounting for testing

  PM: fine. let's regroup thursday afternoon to verify. 3pm?

  [everyone agrees]

  PM: anything else? no? ok bye everyone
```

**Output:**
```json
{
  "meeting_summary": {
    "title": "Feature Progress Check-in",
    "date": null,
    "duration_minutes": null,
    "meeting_type": "standup",
    "attendees": ["PM", "Dave", "Mark", "Sarah"]
  },
  "executive_summary": "Feature blocked by API auth issue is now unblocked after Mark's fix. Dave will complete backend today, Sarah will finish frontend by Wednesday/Thursday. Team to verify completion Thursday 3 PM.",
  "key_topics": [
    {
      "topic": "API Auth Blocker Resolution",
      "summary": "Dave was blocked by auth API issue. Mark pushed fix yesterday. Dave confirmed fix works and can now proceed.",
      "outcome": "decision"
    },
    {
      "topic": "Feature Completion Timeline",
      "summary": "Backend completion expected today. Frontend mostly done, waiting on Dave's endpoint. Full feature expected Thursday with testing.",
      "outcome": "decision"
    }
  ],
  "decisions_made": [
    {
      "decision": "Target feature completion by Thursday",
      "rationale": "Wednesday for development, Thursday accounting for testing",
      "decided_by": "PM (with Sarah's input)"
    },
    {
      "decision": "Verification meeting Thursday 3 PM",
      "rationale": "Confirm feature completion",
      "decided_by": "PM"
    }
  ],
  "action_items": [
    {
      "action": "Pull Mark's API fix and complete endpoint",
      "owner": "Dave",
      "deadline": "Today",
      "priority": "high",
      "dependencies": []
    },
    {
      "action": "Complete frontend after Dave's endpoint is ready",
      "owner": "Sarah",
      "deadline": "Wednesday",
      "priority": "high",
      "dependencies": ["Dave's endpoint"]
    }
  ],
  "open_questions": [],
  "follow_up": {
    "next_meeting": "Thursday 3 PM - verification meeting",
    "items_for_next_meeting": ["Feature completion verification"]
  }
}
```

## Gotchas

### Common Failure Modes
1. **Implicit action items**: "Yeah I'll handle that" without clear task. Extract as action but flag uncertainty.
2. **Name confusion**: Nicknames, partial names, similar names. Use names exactly as spoken.
3. **Tentative vs committed**: "We could maybe..." vs "We will..." Only decisions are commitments.
4. **Context assumptions**: Technical terms, project names need preservation, not explanation.

### Edge Cases to Handle
- **No clear action items**: Some meetings are purely informational. Return empty array, not fabricated items.
- **Conflicting statements**: Person says X, later says not-X. Note the final position.
- **Side conversations**: Off-topic chat should be excluded from summary.
- **Incomplete transcript**: [inaudible] sections. Note gaps, don't guess content.

### When NOT to Use This Prompt
- **Sensitive/confidential meetings**: HR, legal, personnel matters (use specialized prompts with appropriate handling)
- **Large town halls**: More than 15 speakers (use hierarchical summarization)
- **Training sessions**: Different structure needed (focus on Q&A, not decisions)
- **Interviews**: Different output format required

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Sonnet 4 | Standard meetings | Excellent action item extraction |
| **Best:** GPT-4o | Long transcripts | Strong at maintaining context |
| **Acceptable:** Claude Haiku 3.5 | Quick summaries | Good for short standups |
| **Acceptable:** GPT-4o-mini | High volume | Cost-effective for simpler meetings |
| **Not Recommended:** Smaller models | - | Miss nuanced commitments |

## Integration Notes

### Transcript Preprocessing
```python
def preprocess_transcript(raw_transcript):
    # Remove timestamps if not needed
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', raw_transcript)

    # Normalize speaker labels
    text = re.sub(r'([A-Z][a-z]+):', r'\n\1:', text)

    # Remove filler content markers
    text = re.sub(r'\[(cross-talk|inaudible|laughter)\]', '', text, flags=re.I)

    return text.strip()
```

### Output Formatting
```python
def format_for_confluence(summary):
    """Convert JSON summary to Confluence wiki markup"""
    md = f"h1. {summary['meeting_summary']['title']}\n\n"
    md += f"*Date:* {summary['meeting_summary']['date']}\n"
    md += f"*Attendees:* {', '.join(summary['meeting_summary']['attendees'])}\n\n"

    md += "h2. Summary\n"
    md += f"{summary['executive_summary']}\n\n"

    md += "h2. Action Items\n"
    md += "|| Owner || Action || Deadline || Priority ||\n"
    for item in summary['action_items']:
        md += f"| {item['owner']} | {item['action']} | {item['deadline']} | {item['priority']} |\n"

    return md
```

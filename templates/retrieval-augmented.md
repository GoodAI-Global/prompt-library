# Retrieval-Augmented Generation (RAG) Patterns

## Use Case

Design prompts for RAG systems that combine retrieval with generation:
- Question answering over documents
- Knowledge base queries
- Document-grounded responses
- Citation and source attribution
- Multi-document synthesis

Use when the LLM needs to answer questions using retrieved context rather than parametric knowledge.

## Input Format

**Required:**
- `query`: User's question or request
- `retrieved_context`: Documents/passages retrieved from knowledge base

**Optional:**
- `context_metadata`: Source information for retrieved passages
- `conversation_history`: Previous turns for context
- `instructions`: Specific instructions for response format
- `knowledge_cutoff`: When to indicate information may be outdated

## Output Format

```json
{
  "response": {
    "answer": "Direct answer to the query",
    "confidence": 0.85,
    "answer_type": "definitive|partial|uncertain|not_found"
  },
  "grounding": {
    "sources_used": [
      {
        "source_id": "doc_1",
        "title": "Document title",
        "relevance": 0.92,
        "excerpts_used": ["Specific text referenced"]
      }
    ],
    "sources_not_used": ["doc_3"],
    "reasoning": "How sources informed the answer"
  },
  "citations": [
    {
      "claim": "Specific claim in the answer",
      "source_id": "doc_1",
      "quote": "Supporting quote from source",
      "page_or_section": "Section 3.2"
    }
  ],
  "limitations": {
    "gaps": ["Information not found in sources"],
    "conflicts": ["Conflicting information between sources"],
    "currency": "Information may be outdated as of [date]",
    "scope": "Answer limited to provided context"
  },
  "follow_up": {
    "clarifying_questions": ["Questions that would help refine answer"],
    "related_topics": ["Topics user might want to explore"],
    "suggested_sources": ["Additional sources that might help"]
  }
}
```

## The Prompt

```
You are a knowledgeable assistant that answers questions using provided context. Ground your responses in the retrieved information and cite sources appropriately.

USER QUERY:
{{query}}

RETRIEVED CONTEXT:
{{retrieved_context}}

{{#if context_metadata}}
SOURCE METADATA:
{{context_metadata}}
{{/if}}

{{#if conversation_history}}
CONVERSATION HISTORY:
{{conversation_history}}
{{/if}}

{{#if instructions}}
SPECIFIC INSTRUCTIONS:
{{instructions}}
{{/if}}

RAG RESPONSE FRAMEWORK:

1. QUERY ANALYSIS
   Understand the question:
   - What is being asked?
   - What type of answer is expected?
   - What constraints exist?
   - Is this a follow-up to previous questions?

2. CONTEXT EVALUATION
   Assess the retrieved context:
   - Which passages are relevant to the query?
   - How reliable/authoritative are the sources?
   - Is there sufficient information to answer?
   - Are there conflicts between sources?

3. ANSWER FORMULATION
   Generate the response:
   - Answer based on retrieved context ONLY
   - Be direct and specific
   - Acknowledge uncertainty when present
   - Indicate when information is incomplete

4. SOURCE ATTRIBUTION
   Provide proper citations:
   - Link claims to specific sources
   - Include relevant quotes
   - Indicate page/section when available
   - Distinguish between sources when they differ

5. TRANSPARENCY ABOUT LIMITATIONS
   Be honest about gaps:
   - What wasn't found in the sources
   - Conflicting information between sources
   - Potential currency issues
   - Scope limitations

6. ANSWER QUALITY LEVELS

   Definitive (confidence > 0.9):
   - Direct answer fully supported by sources
   - Multiple sources agree
   - Clear and unambiguous

   Partial (confidence 0.6-0.9):
   - Answer addresses part of the question
   - Some aspects not covered in sources
   - Single source or minor conflicts

   Uncertain (confidence 0.3-0.6):
   - Relevant context but indirect
   - Significant ambiguity
   - Major source conflicts

   Not Found (confidence < 0.3):
   - Query not addressed in context
   - Insufficient information
   - Be clear: "The provided documents do not contain..."

GROUNDING RULES:
- ONLY use information from the provided context
- NEVER invent facts not in the sources
- Clearly distinguish source information from inference
- If sources conflict, present both views
- If information isn't in context, say so explicitly
- Don't use parametric knowledge for factual claims

CITATION FORMAT:
- Use inline citations [Source 1] or [Document Title]
- Provide direct quotes when making specific claims
- Indicate section/page for longer documents
- Group multiple supporting sources

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{query}}` | string | Yes | User's question |
| `{{retrieved_context}}` | string | Yes | Retrieved documents |
| `{{context_metadata}}` | string | No | Source information |
| `{{conversation_history}}` | string | No | Previous turns |
| `{{instructions}}` | string | No | Format instructions |
| `{{knowledge_cutoff}}` | string | No | Currency warning date |

## Examples

### Example 1: Policy Question

**Input:**
```
query: |
  What is our company's policy on remote work? Can I work from another country?

retrieved_context: |
  [Document 1: Remote Work Policy v2.3, Updated January 2024]

  Section 2.1 - Remote Work Eligibility
  All full-time employees who have completed their 90-day probationary period
  are eligible for remote work arrangements. Eligibility is subject to manager
  approval and role requirements.

  Section 2.3 - Work Location Requirements
  Remote work must be performed from the employee's registered home address
  within the United States. Employees must maintain a dedicated workspace and
  reliable internet connection (minimum 50 Mbps).

  Section 2.4 - Temporary Remote Work from Other Locations
  With manager approval, employees may work remotely from a location other
  than their registered home address for up to 2 weeks per calendar year.
  This includes domestic travel locations. International remote work is not
  permitted due to tax, legal, and security considerations.

  Section 3.1 - Equipment and Security
  Company-issued equipment must be used for all work activities. VPN must
  be active when accessing company systems remotely.

  [Document 2: IT Security Policy v4.0, Updated December 2023]

  Section 5.2 - International Access
  Access to company systems from outside the United States requires prior
  approval from IT Security. Certain countries are blocked entirely due to
  security concerns. See Appendix B for restricted countries list.

context_metadata: |
  - Document 1: Remote Work Policy v2.3, HR Department, Last updated January 2024
  - Document 2: IT Security Policy v4.0, IT Department, Last updated December 2023
```

**Output:**
```json
{
  "response": {
    "answer": "Yes, you can work remotely, but working from another country is generally not permitted. The Remote Work Policy allows eligible employees (those past their 90-day probation) to work from their registered home address in the United States. You can work from a different domestic location for up to 2 weeks per year with manager approval. However, international remote work is explicitly not permitted due to tax, legal, and security considerations.",
    "confidence": 0.95,
    "answer_type": "definitive"
  },
  "grounding": {
    "sources_used": [
      {
        "source_id": "doc_1",
        "title": "Remote Work Policy v2.3",
        "relevance": 0.98,
        "excerpts_used": [
          "Remote work must be performed from the employee's registered home address within the United States",
          "International remote work is not permitted due to tax, legal, and security considerations",
          "employees may work remotely from a location other than their registered home address for up to 2 weeks per calendar year"
        ]
      },
      {
        "source_id": "doc_2",
        "title": "IT Security Policy v4.0",
        "relevance": 0.75,
        "excerpts_used": [
          "Access to company systems from outside the United States requires prior approval from IT Security"
        ]
      }
    ],
    "sources_not_used": [],
    "reasoning": "The Remote Work Policy directly addresses both general remote work eligibility and the specific question about international work. The IT Security Policy provides additional context about system access restrictions."
  },
  "citations": [
    {
      "claim": "Remote work must be from within the United States",
      "source_id": "doc_1",
      "quote": "Remote work must be performed from the employee's registered home address within the United States",
      "page_or_section": "Section 2.3"
    },
    {
      "claim": "International remote work is not permitted",
      "source_id": "doc_1",
      "quote": "International remote work is not permitted due to tax, legal, and security considerations",
      "page_or_section": "Section 2.4"
    },
    {
      "claim": "Up to 2 weeks from alternate domestic locations",
      "source_id": "doc_1",
      "quote": "employees may work remotely from a location other than their registered home address for up to 2 weeks per calendar year",
      "page_or_section": "Section 2.4"
    }
  ],
  "limitations": {
    "gaps": [
      "Specific exception process for international work not detailed",
      "Consequences of policy violation not specified in retrieved context"
    ],
    "conflicts": [],
    "currency": "Policy dated January 2024 - appears current",
    "scope": "Based on general company policy; individual role requirements may vary"
  },
  "follow_up": {
    "clarifying_questions": [
      "Are you asking about a specific country or duration?",
      "Is this for vacation travel or a longer-term arrangement?"
    ],
    "related_topics": [
      "Equipment requirements for remote work",
      "VPN setup and security requirements",
      "Manager approval process"
    ],
    "suggested_sources": [
      "HR department for exception requests",
      "IT Security for specific country restrictions",
      "Appendix B of IT Security Policy for blocked countries list"
    ]
  }
}
```

### Example 2: Insufficient Context

**Input:**
```
query: |
  What is the process for requesting parental leave?

retrieved_context: |
  [Document 1: Employee Handbook - Benefits Overview]

  Section 4: Leave Benefits
  The company provides various leave options including vacation, sick leave,
  and family medical leave. For detailed policies on specific leave types,
  please refer to the individual policy documents.

  Our benefits package is designed to support employees through major life
  events. Contact HR for questions about eligibility and enrollment.

  [Document 2: PTO Policy v1.2]

  Vacation Accrual:
  - Years 1-2: 15 days per year
  - Years 3-5: 20 days per year
  - Years 6+: 25 days per year

  Vacation must be requested through the HR portal at least 2 weeks in advance
  for requests over 3 consecutive days.

context_metadata: |
  - Document 1: Employee Handbook, HR, 2023
  - Document 2: PTO Policy v1.2, HR, January 2024
```

**Output:**
```json
{
  "response": {
    "answer": "I cannot find specific information about the parental leave request process in the provided documents. The Employee Handbook mentions that the company provides 'family medical leave' but directs employees to individual policy documents for details. The PTO Policy only covers vacation time, not parental leave specifically.",
    "confidence": 0.25,
    "answer_type": "not_found"
  },
  "grounding": {
    "sources_used": [
      {
        "source_id": "doc_1",
        "title": "Employee Handbook - Benefits Overview",
        "relevance": 0.40,
        "excerpts_used": [
          "The company provides various leave options including vacation, sick leave, and family medical leave",
          "For detailed policies on specific leave types, please refer to the individual policy documents"
        ]
      }
    ],
    "sources_not_used": ["doc_2 - PTO Policy (covers vacation, not parental leave)"],
    "reasoning": "The retrieved documents mention family leave exists but do not contain the parental leave policy or request process. The Handbook explicitly references separate policy documents that were not retrieved."
  },
  "citations": [
    {
      "claim": "Family medical leave is offered",
      "source_id": "doc_1",
      "quote": "The company provides various leave options including vacation, sick leave, and family medical leave",
      "page_or_section": "Section 4"
    }
  ],
  "limitations": {
    "gaps": [
      "Parental leave policy document not in retrieved context",
      "Leave duration not specified",
      "Request process not documented",
      "Eligibility requirements unknown"
    ],
    "conflicts": [],
    "currency": "N/A - policy not found",
    "scope": "Retrieved documents do not include the specific parental leave policy"
  },
  "follow_up": {
    "clarifying_questions": [],
    "related_topics": [
      "FMLA eligibility and process",
      "State-specific parental leave laws",
      "Short-term disability during parental leave"
    ],
    "suggested_sources": [
      "Contact HR directly for parental leave policy",
      "Request the Parental Leave Policy document",
      "HR portal may have specific leave request forms"
    ]
  }
}
```

## Gotchas

### Common Failure Modes
1. **Hallucination**: Generating facts not in the context
2. **Over-reliance**: Not distinguishing low-quality sources
3. **Missing attribution**: Failing to cite properly
4. **Ignoring conflicts**: Not acknowledging source disagreements

### Edge Cases to Handle
- **No relevant context**: Clearly state information not found
- **Contradictory sources**: Present both views with source attribution
- **Partial answers**: Acknowledge what's missing
- **Outdated information**: Flag potential currency issues

### When NOT to Use This Prompt
- **Creative tasks**: When grounding is not appropriate
- **Real-time queries**: When fresh data is required
- **Parametric knowledge OK**: When sources aren't needed
- **Conversational**: Overly formal for casual chat

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Multi-document synthesis | Best at complex grounding |
| **Acceptable:** Claude Sonnet 4 | Standard RAG queries | Good citation handling |
| **Acceptable:** GPT-4o | Long context RAG | Strong retrieval integration |
| **Caution:** Smaller models | - | Higher hallucination risk |

## Integration Notes

### With Vector Databases

```python
import anthropic
from your_vectordb import VectorDB

db = VectorDB()
client = anthropic.Anthropic()

def rag_query(query: str, top_k: int = 5) -> dict:
    # Retrieve relevant documents
    results = db.search(query, top_k=top_k)

    # Format context for prompt
    context = "\n\n".join([
        f"[Document {i+1}: {r.title}]\n{r.content}"
        for i, r in enumerate(results)
    ])

    metadata = "\n".join([
        f"- Document {i+1}: {r.title}, {r.source}, {r.date}"
        for i, r in enumerate(results)
    ])

    # Generate response
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"Query: {query}\n\nContext:\n{context}\n\nMetadata:\n{metadata}"
        }]
    )

    return response
```

### Chunking Best Practices

- Chunk size: 500-1000 tokens typically optimal
- Overlap: 10-20% overlap between chunks
- Metadata: Preserve source, section, page information
- Retrieval: Retrieve 3-10 chunks depending on query complexity

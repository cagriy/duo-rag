from __future__ import annotations

from dataclasses import dataclass

DEFAULT_QUERY_SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions about a document collection. "
    "Use the available tools to find information. "
    "For quantitative questions (counts, averages, comparisons), prefer run_sql. "
    "For qualitative questions (descriptions, explanations), prefer semantic_search. "
    "When writing SQL for text fields, use LIKE with wildcards for partial matching "
    "(e.g. WHERE birthplace LIKE '%England%') rather than exact equality, "
    "since stored values are full location or description strings.\n\n"
    "The available metadata columns are: {available_columns}. "
    "IMPORTANT: Only reference these exact columns in SQL. "
    "If the information needed to answer the question is not available as a column, "
    "do NOT approximate with an unrelated column — use semantic_search instead."
)

DEFAULT_METADATA_EXTRACTION_PROMPT = (
    "You are a metadata extraction assistant. "
    "Extract the following fields from the given text. "
    "Return valid JSON. Use null for fields not found.\n\n"
    "{extraction_fields}"
)

DEFAULT_SCHEMA_DISCOVERY_PROMPT = (
    "You are a metadata schema discovery assistant. "
    "Analyze the following document samples and propose structured metadata "
    "fields that can be extracted. Return a JSON object with a 'fields' array, "
    "where each field has 'name' (snake_case), 'type' ('text' or 'integer'), "
    "and 'description'."
)

DEFAULT_SCHEMA_GAP_DETECTION_PROMPT = (
    "You are a schema analyst for a structured metadata database. "
    "Given a user question and the current schema, decide if the question requires "
    "a SHORT, STRUCTURED metadata field that is missing.\n\n"
    "A valid gap is a field that is:\n"
    "  - atomic and short (e.g. a name, a year, a category, a country)\n"
    "  - useful for filtering or aggregation (GROUP BY, COUNT, WHERE)\n"
    "  - not already answerable by searching the document text\n\n"
    "Do NOT flag a gap for:\n"
    "  - open-ended or descriptive questions (e.g. 'tell me about', 'explain', 'describe')\n"
    "  - fields that would store long text or summaries (e.g. biography, summary, description)\n"
    "  - questions that ask about specific facts, events, or details described in the "
    "documents — these are answered by reading the document text via semantic search, "
    "NOT by adding a metadata column. Examples: 'Who discovered electromagnetic "
    "induction?', 'What did Curie research?', 'How did Turing contribute to computing?'\n"
    "  - Only flag a gap when the question REQUIRES filtering, sorting, or aggregating "
    "across documents by a structured value (e.g. 'how many scientists died after 1900' "
    "needs year_of_death; 'list people by nationality' needs nationality)\n"
    "  - counting or aggregation questions that are fully answerable with existing fields "
    "(e.g. 'how many people total' needs no new field; but 'how many died after 1800' "
    "DOES need year_of_death if it doesn't exist)\n"
    "  - identifier or system fields (e.g. person_id, record_id, id, key, index)\n"
    "  - fields that already exist in the schema\n"
    "  - fields that are SEMANTICALLY EQUIVALENT to an existing field, even if named "
    "differently (e.g. 'field_of_expertise', 'profession', 'role', 'specialization' "
    "are all covered by 'occupation')\n\n"
    "Return JSON with:\n"
    "- gap_detected (bool)\n"
    "- reasoning (string): brief explanation\n"
    "- proposed_field (object or null): if gap_detected, "
    "{{name (snake_case), type ('text' or 'integer'), description}}\n\n"
    "Current schema fields:\n{fields_text}"
)


@dataclass
class PromptConfig:
    """Customizable prompts for all LLM calls in meta-rag."""

    query_system_prompt: str = DEFAULT_QUERY_SYSTEM_PROMPT
    metadata_extraction_prompt: str = DEFAULT_METADATA_EXTRACTION_PROMPT
    schema_discovery_prompt: str = DEFAULT_SCHEMA_DISCOVERY_PROMPT
    schema_gap_detection_prompt: str = DEFAULT_SCHEMA_GAP_DETECTION_PROMPT

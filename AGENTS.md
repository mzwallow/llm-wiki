# LLM Wiki Schema

## Structure
- `raw/assets/`: Immutable source documents and images.
- `wiki/`: LLM-generated markdown files.
- `index.md`: Catalog of all wiki pages.
- `log.md`: Append-only chronological record of changes.

## Workflows

### Ingest
1. Read the new source document from `raw/`.
2. Extract key information and discuss takeaways.
3. Write/update summary pages in `wiki/`.
4. Update relevant entity/concept pages.
5. Update `index.md`.
6. Append an entry to `log.md` (e.g., `## [YYYY-MM-DD] ingest | Article Title`).
7. Run `bunx @tobilu/qmd embed` to update search index.

### Query
1. Read `index.md` to find relevant pages.
2. Read the specific pages.
3. Synthesize an answer with citations.
4. If the answer is valuable, file it back into `wiki/` as a new page and update `index.md` and `log.md`.

### Tokenize
1. Check if virtual environment is active (e.g., `[[ "$VIRTUAL_ENV" == "" ]]`).
2. If not active, source it: `source .venv/bin/activate`.
3. Run tokenization: `python3 scripts/tokenize.py <file_path>`.

### Lint
1. Check for contradictions, stale claims, orphan pages, missing cross-references, and data gaps.
2. Suggest new questions to investigate or sources to find.
3. Apply updates to the wiki as needed.

## Wiki Maintenance Principles

These principles guide how the LLM should act as a disciplined maintainer of the knowledge base. Bias toward caution and preservation over speed.

### 1. Think Before Writing
**Don't assume. Surface tradeoffs.**
- Before ingesting a complex source or answering a vague query, state your assumptions.
- If multiple interpretations of a source exist, present them rather than picking one silently.
- If an existing page structure is unclear, stop and ask before modifying it.

### 2. Simplicity First
**Minimum markdown that captures the knowledge. Nothing speculative.**
- Don't add structural features (complex tables, nested folders) unless asked or necessary.
- Don't create overly granular concept pages for single mentions.
- If you write 5 paragraphs of summary and it could be 1, rewrite it.
- Ask: "Would an experienced editor find this page over-complicated?"

### 3. Surgical Changes
**Touch only what you must. Clean up your own mess.**
- When updating existing pages, don't "improve" adjacent paragraphs or formatting unless requested.
- Don't rewrite historical summaries just because your style changed.
- Match existing formatting styles.
- If your updates create orphan pages (concepts no longer linked), mention them or remove them if appropriate.

### 4. Goal-Driven Workflows
**Define success criteria for large updates.**
- When batch-ingesting or executing a large lint pass, state a brief plan:
  1. [Task] → verify: [check]
- Strong success criteria (e.g., "All 5 new concepts have inbound links from index.md") let you loop independently until correct.

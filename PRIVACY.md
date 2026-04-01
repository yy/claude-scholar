# Privacy Policy

claude-scholar is a set of skills (plugins) for Claude Code. All skills run inside an AI coding agent, which means any content the agent reads during execution (LaTeX source, bibliography files, figure images, etc.) is sent to the underlying model provider (e.g., Anthropic's Claude API) as part of the conversation. This is inherent to how AI coding agents work and applies to all skills.

Beyond the model provider, skills vary in whether they send data to additional external services:

## Data exposure categories

### 1. Public API lookups only

These skills send only short identifiers or search terms to public academic APIs. No manuscript content is transmitted by these skills themselves:

- **arxiv-metadata** — sends an arXiv ID to the arXiv API (export.arxiv.org)
- **doi-bibtex** — sends a DOI to the CrossRef API (doi.org)
- **openalex** — sends search terms to the OpenAlex API (api.openalex.org); optionally sends your email as a `mailto` parameter for the higher-rate "polite pool" per the [OpenAlex API documentation](https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication)

### 2. AI model provider only

These skills send manuscript content or figures to the model provider but make no additional external requests:

- **latex-cleanup** — the agent reads your `.tex` files
- **verify-math** — the agent reads your math expressions; SymPy runs locally
- **critique-manuscript** — the agent reads your full manuscript (by default; optionally invokes `openalex`, see below)
- **critique-figures** — the agent receives your figure images for vision analysis; programmatic checks (file format, bitmap-in-PDF) run locally
- **arxiv-prep** — the agent reads your `.tex` files to identify the main document; packaging runs locally via [arxiv-latex-cleaner](https://github.com/google-research/arxiv-latex-cleaner)

### 3. AI model provider + external services

These skills send manuscript content to the model provider and additionally query external services:

- **check-refs** — uses [bibsleuth](https://github.com/yy/bibsleuth), which queries academic databases (Semantic Scholar, CrossRef) to verify citations. When bibsleuth's LLM analysis mode is enabled, citation context may also be sent to LLM APIs (Anthropic or OpenAI) via your API keys. This mode requires explicit configuration and is not enabled by default.

### 4. Composite skills

These skills orchestrate other skills and inherit their data exposure:

- **presubmit-checks** — invokes `latex-cleanup`, `check-refs`, and build verification. Data exposure depends on which sub-checks run (see above).
- **critique-manuscript** — model-provider-only by default. If the user opts in to literature search, it additionally invokes `openalex`.

## Per-skill summary

| Skill | Agent reads | External requests |
|-------|------------|-------------------|
| `arxiv-metadata` | arXiv ID | arXiv API |
| `doi-bibtex` | DOI | CrossRef API |
| `openalex` | Search terms | OpenAlex API |
| `arxiv-prep` | `.tex` files | None |
| `check-refs` | `.bib` files | Semantic Scholar, CrossRef; optionally LLM APIs |
| `critique-figures` | Figure images | None |
| `critique-manuscript` | Full manuscript | None (optionally OpenAlex) |
| `latex-cleanup` | `.tex` files | None |
| `presubmit-checks` | `.tex` and `.bib` files | Via `check-refs` |
| `verify-math` | Math expressions | None |

Please refer to each external service's own privacy policy for how they handle incoming requests.

## Contact

If you have questions about this policy, please open an issue at https://github.com/yy/claude-scholar/issues.

# Privacy Policy

claude-scholar is a set of skills (plugins) for Claude Code that run on your local machine. claude-scholar itself does not collect, store, or transmit any personal data or usage information. However, some skills make outbound requests to external services:

## External API requests

Several skills query public APIs to fetch metadata. These requests contain only the query parameters you provide (e.g., a DOI, arXiv ID, or search term):

- **arXiv API** (export.arxiv.org) — paper metadata lookups
- **CrossRef API** (doi.org) — DOI resolution and BibTeX retrieval
- **Semantic Scholar API** (api.semanticscholar.org) — reference verification

## OpenAlex API

The **openalex** skill queries the OpenAlex API (api.openalex.org) for literature searches. It optionally sends your email address as a `mailto` parameter to access the higher-rate "polite pool" — this is standard practice per the [OpenAlex API documentation](https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication).

## Reference checking (bibsleuth)

The **check-refs** skill uses [bibsleuth](https://github.com/yy/bibsleuth), which queries academic databases to verify citations. When bibsleuth's LLM analysis mode is enabled, citation context and paper content may be sent to LLM APIs (Anthropic or OpenAI) using API keys from your environment. This mode requires explicit configuration and is not enabled by default.

## Local-only skills

The following skills perform all operations locally and make no network requests: **latex-cleanup**, **verify-math**, **arxiv-prep**, and **presubmit-checks** (though presubmit-checks invokes check-refs, which may make external requests as described above).

Please refer to each external service's own privacy policy for how they handle incoming requests.

## Contact

If you have questions about this policy, please open an issue at https://github.com/yy/claude-scholar/issues.

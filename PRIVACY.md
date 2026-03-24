# Privacy Policy

claude-scholar is a set of skills (plugins) for Claude Code that run entirely on your local machine. claude-scholar does not collect, store, or transmit any personal data or usage information.

Some skills make outbound requests to public APIs to fetch metadata:

- **OpenAlex API** (api.openalex.org) — for literature searches
- **arXiv API** (export.arxiv.org) — for paper metadata
- **CrossRef API** (api.crossref.org) — for DOI lookups and BibTeX entries
- **Semantic Scholar API** (api.semanticscholar.org) — for reference verification

These requests contain only the query parameters you provide (e.g., a DOI or search term). No authentication tokens, personal identifiers, or tracking data are sent. Please refer to each service's own privacy policy for how they handle incoming requests.

## Contact

If you have questions about this policy, please open an issue at https://github.com/yy/claude-scholar/issues.

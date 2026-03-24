# Privacy Policy

claude-scholar is a set of skills (plugins) for Claude Code that run entirely on your local machine. claude-scholar does not collect, store, or transmit any personal data or usage information.

Some skills make outbound requests to public APIs to fetch metadata:

- **OpenAlex API** (api.openalex.org) — for literature searches
- **arXiv API** (export.arxiv.org) — for paper metadata
- **CrossRef API** (api.crossref.org) — for DOI lookups and BibTeX entries
- **Semantic Scholar API** (api.semanticscholar.org) — for reference verification

These requests contain the query parameters you provide (e.g., a DOI or search term). The OpenAlex skill optionally sends your email address as a `mailto` parameter to access their higher-rate "polite pool" — this is standard practice per the [OpenAlex API documentation](https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication). No other personal identifiers or tracking data are sent by claude-scholar. Please refer to each service's own privacy policy for how they handle incoming requests.

## Contact

If you have questions about this policy, please open an issue at https://github.com/yy/claude-scholar/issues.

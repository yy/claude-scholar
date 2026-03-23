# claude-scholar

Academic research tools for [Claude Code](https://claude.ai/code). Literature search, citation management, LaTeX checks, math verification, and submission preparation. These tools assist with formatting and verification—they do not generate original research content. Please check your venue's AI use policy for guidance on whether and how to use these tools.

## Skills

| Skill | Description |
|-------|-------------|
| `arxiv-metadata` | Fetch structured metadata for arXiv papers (title, authors, date, categories, DOI) |
| `arxiv-prep` | Prepare an arXiv submission package — clean source, compile, extract metadata, create tarball |
| `check-refs` | Verify citation references in LaTeX papers against academic databases using [bibsleuth](https://github.com/yy/bibsleuth) |
| `doi-bibtex` | Fetch BibTeX entries from DOIs and add to `.bib` files |
| `latex-cleanup` | Review LaTeX documents for common issues, style consistency, typography, cross-references, and draft artifacts |
| `math` | Verify mathematical derivations step-by-step using SymPy |
| `openalex` | Query and analyze 240M+ scholarly works via the [OpenAlex](https://openalex.org) API |
| `presubmit-checks` | Pre-submission checklist — references, LaTeX cleanup, build, and front matter |

## Installation

```
/plugin marketplace add yy/claude-scholar
/plugin install claude-scholar@yy-claude-scholar
/reload-plugins
```

Skills are invoked as slash commands with the `claude-scholar:` prefix:

```
/claude-scholar:arxiv-metadata 2301.10140
/claude-scholar:doi-bibtex
/claude-scholar:check-refs
/claude-scholar:latex-cleanup
/claude-scholar:presubmit-checks
/claude-scholar:math
/claude-scholar:openalex
/claude-scholar:arxiv-prep
```

## Dependencies

Some skills require external tools:

- **check-refs**: [bibsleuth](https://github.com/yy/bibsleuth) (`uvx bibsleuth`)
- **math**: [SymPy](https://www.sympy.org) (`uv run` with sympy available)
- **arxiv-prep**: [arxiv-latex-cleaner](https://github.com/google-research/arxiv-latex-cleaner) (`uvx arxiv-latex-cleaner`)
- **openalex**: Python with `requests` (included in the plugin's helper scripts)
- **arxiv-metadata**: Python with `requests` (`uv run` with inline script dependencies)

## Acknowledgements

- [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) — inspiration and starting point for the OpenAlex skill
- [Sadamori Kojaku](https://github.com/skojaku) — inspiration for the math verification skill

## License

MIT

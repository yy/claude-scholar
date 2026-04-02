# claude-scholar

Academic research tools for [Claude Code](https://claude.ai/code). Literature search, citation management, LaTeX checks, math verification, manuscript critique, and submission preparation. These tools assist with formatting and verification—they do not generate original research content. Please check your venue's AI use policy for guidance on whether and how to use these tools.

> **Note**: These skills are early-stage and not comprehensively tested. Proceed with caution!

## Basic principle for skill development and inclusion 

Don't overbuild. Foundation models and agent harnesses are getting better fast, and overbuilt structure becomes a maintenance burden that constrains the base model rather than helping it. These skills exist only where they add something Claude can't quickly or easily do on its own: calling external APIs, running programmatic verification, or encoding multi-step checklists that are easy to forget. No skill for something Claude already handles well out of the box or will likely handle with minimal guidance or conversation.

## Skills

### Lookup

Single-purpose data retrieval from external sources.

| Skill | Description |
|-------|-------------|
| `arxiv-metadata` | Fetch structured metadata for arXiv papers (title, authors, date, categories, DOI) |
| `doi-bibtex` | Fetch BibTeX entries from DOIs and add to `.bib` files |
| `openalex` | Query and analyze 240M+ scholarly works via the [OpenAlex](https://openalex.org) API |

### Analysis

Inspect, verify, or critique artifacts — from programmatic checks to structured review.

| Skill | Description |
|-------|-------------|
| `check-refs` | Verify citation references in LaTeX papers against academic databases using [bibsleuth](https://github.com/yy/bibsleuth) |
| `latex-cleanup` | Review LaTeX documents for common issues, style consistency, typography, cross-references, and draft artifacts |
| `verify-math` | Verify mathematical derivations step-by-step using SymPy |
| `critique-figures` | Critique figures for format, colorblind safety, legibility, overplotting, and chart choice |
| `critique-manuscript` | Structured self-review of your manuscript |

### Orchestration

Multi-step workflows that coordinate other skills or external tools.

| Skill | Description |
|-------|-------------|
| `presubmit-checks` | Pre-submission checklist — references, LaTeX cleanup, build, figure format, and front matter |
| `arxiv-prep` | Prepare an arXiv submission package — clean source, compile, extract metadata, create tarball |

## Skill details

### Lookup

#### `arxiv-metadata`

Fetches structured metadata from arXiv given an arXiv ID or URL — title, authors, date, categories, DOI. Handles multiple ID formats (new and old-style). Mainly used by other skills and agents rather than invoked directly.

#### `doi-bibtex`

Given a DOI (bare or full URL), fetches the BibTeX entry and appends it to the project's `.bib` file, checking for duplicates. Simple utility — mainly invoked by Claude when adding references.

#### `openalex`

Queries the [OpenAlex](https://openalex.org) API (240M+ scholarly works) for literature searches, citation analysis, and bibliometric queries. The helper script handles rate limiting, retries, and pagination. No API key required.

### Analysis

#### `check-refs`

Verifies that every citation in a LaTeX paper exists in academic databases, flags suspicious entries, and suggests missing DOIs/URLs. Uses [bibsleuth](https://github.com/yy/bibsleuth). Can run standalone or as part of `presubmit-checks`.

#### `latex-cleanup`

Systematic review of LaTeX documents for common issues: style consistency, typography, cross-references, draft artifacts, debugging code. Identifies all `.tex` files in the project (including `\input`/`\include` targets) and flags problems.

#### `verify-math`

Step-by-step verification of mathematical derivations using SymPy. Each derivation step is validated programmatically — useful for catching algebra and calculus errors in proofs and equations.

#### `critique-figures`

Critiques academic figures using a mix of programmatic checks and vision analysis. Checks file format and resolution (flags raster exports of plots/charts, detects bitmap-in-PDF wrappers), colorblind risk (red-green reliance), excessive categories, font legibility, overplotted scatterplots, and dynamite plots. Handles multi-panel figures by evaluating each panel individually. Resolves figures from `\includegraphics` references in the TeX tree. Report-only — does not modify figures.

#### `critique-manuscript`

Structured self-review of your own manuscript before submission. Evaluates the paper across seven review criteria — literature and novelty, methodological rigor, causal claims, data quality, generalizability, mechanism, and clarity — and produces a report with top risks, what to preserve, anticipated reviewer questions, and detailed criterion-by-criterion comments anchored to specific sections of the paper. Optionally searches OpenAlex for missing literature. Designed strictly for self-review; declines to review others' unpublished work and explains why.

### Orchestration

#### `presubmit-checks`

Pre-submission checklist that orchestrates multiple checks in parallel: references (`check-refs`), LaTeX cleanup (`latex-cleanup`), build verification, figure format checks (flags bitmap figures that should be vector), and front matter review (affiliations, acknowledgements, data availability). Presents a unified report organized by severity.

#### `arxiv-prep`

Automates arXiv submission packaging: cleans source files, removes cruft, verifies compilation, extracts metadata for the submission form, and produces a ready-to-upload tarball. Uses Google's [arxiv-latex-cleaner](https://github.com/google-research/arxiv-latex-cleaner) under the hood. Complements `presubmit-checks` (content quality) by handling the packaging side.

## Installation

```
/plugin marketplace add yy/claude-scholar
/plugin install claude-scholar@yy-claude-scholar
/reload-plugins
```

Skills are invoked as slash commands:

```
/arxiv-metadata 2301.10140
/doi-bibtex 10.1038/nature12373
/check-refs
/latex-cleanup
/presubmit-checks
/verify-math
/openalex
/arxiv-prep
/critique-manuscript
/critique-figures
```

## Dependencies

Some skills require external tools:

- **check-refs**: [bibsleuth](https://github.com/yy/bibsleuth) (`uvx bibsleuth`)
- **verify-math**: [SymPy](https://www.sympy.org) (`uv run` with sympy available)
- **arxiv-prep**: [arxiv-latex-cleaner](https://github.com/google-research/arxiv-latex-cleaner) (`uvx arxiv-latex-cleaner`)
- **openalex**: Python with `requests` (included in the plugin's helper scripts)
- **arxiv-metadata**: Python with `requests` (`uv run` with inline script dependencies)

## Acknowledgements

- [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) — inspiration and starting point for the OpenAlex skill
- [Sadamori Kojaku](https://github.com/skojaku) — inspiration for the math verification skill
- [Trevor Campbell's arXiv checklist](https://trevorcampbell.me/html/arxiv.html) — inspiration for the arXiv prep skill

## License

MIT

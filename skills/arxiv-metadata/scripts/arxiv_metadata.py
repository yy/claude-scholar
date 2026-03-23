#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""Fetch structured metadata from the arXiv API for a given arXiv ID."""

import json
import re
import sys
import xml.etree.ElementTree as ET

import requests

ARXIV_API = "http://export.arxiv.org/api/query"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def extract_arxiv_id(raw: str) -> str:
    """Extract bare arXiv ID from a URL or bare ID string."""
    # Handle URLs like https://arxiv.org/abs/2301.10140 or /pdf/2301.10140v2
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([^\s?#]+)", raw)
    if m:
        return re.sub(r"v\d+$", "", m.group(1))
    # Bare ID (new-style 2301.10140 or old-style hep-ph/9901234)
    m = re.match(r"([\w.-]+/\d{7}|\d{4}\.\d{4,5})(v\d+)?$", raw.strip())
    if m:
        return m.group(1)
    print(f"Error: could not parse arXiv ID from '{raw}'", file=sys.stderr)
    sys.exit(1)


def fetch_metadata(arxiv_id: str) -> dict:
    resp = requests.get(ARXIV_API, params={"id_list": arxiv_id}, timeout=15)
    resp.raise_for_status()

    root = ET.fromstring(resp.text)
    entry = root.find("atom:entry", NS)
    if entry is None:
        print(f"Error: no entry found for arXiv ID '{arxiv_id}'", file=sys.stderr)
        sys.exit(1)

    # Check for API error
    id_elem = entry.find("atom:id", NS)
    if id_elem is not None and id_elem.text and "api/errors" in id_elem.text:
        summary = entry.findtext("atom:summary", default="", namespaces=NS).strip()
        print(f"Error: arXiv API error — {summary}", file=sys.stderr)
        sys.exit(1)

    title = entry.findtext("atom:title", default="", namespaces=NS)
    title = " ".join(title.split())  # collapse whitespace

    authors = [
        name.text for name in entry.findall("atom:author/atom:name", NS) if name.text
    ]

    published = entry.findtext("atom:published", default="", namespaces=NS)[:10]

    primary_cat = None
    pc_elem = entry.find("arxiv:primary_category", NS)
    if pc_elem is not None:
        primary_cat = pc_elem.get("term")

    categories = [
        c.get("term") for c in entry.findall("atom:category", NS) if c.get("term")
    ]

    doi = None
    doi_elem = entry.find("arxiv:doi", NS)
    if doi_elem is not None and doi_elem.text:
        doi = doi_elem.text.strip()

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors,
        "published": published,
        "primary_category": primary_cat,
        "categories": categories,
        "doi": doi,
        "url": f"https://doi.org/{doi}" if doi else f"https://arxiv.org/abs/{arxiv_id}",
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: arxiv_metadata.py <arXiv-ID-or-URL>", file=sys.stderr)
        sys.exit(1)

    aid = extract_arxiv_id(sys.argv[1])
    meta = fetch_metadata(aid)
    print(json.dumps(meta, indent=2))

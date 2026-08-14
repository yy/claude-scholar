#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""Command-line interface for the bundled OpenAlex client."""

from __future__ import annotations

import argparse
import json
from openalex_client import OpenAlexClient


def parse_filter(value: str) -> tuple[str, str]:
    key, separator, filter_value = value.partition("=")
    if not separator or not key or not filter_value:
        raise argparse.ArgumentTypeError(
            f"invalid filter {value!r}; expected KEY=VALUE"
        )
    return key, filter_value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query the OpenAlex API")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search-works", help="Search scholarly works")
    search.add_argument("query")
    search.add_argument(
        "--filter", action="append", default=[], type=parse_filter, metavar="KEY=VALUE"
    )
    search.add_argument("--sort")
    search.add_argument("--select", action="append", default=[])
    search.add_argument("--per-page", type=int, default=25)

    entity = subparsers.add_parser("get-entity", help="Resolve an entity by ID")
    entity.add_argument(
        "entity_type", choices=("works", "authors", "institutions", "sources")
    )
    entity.add_argument("entity_id")

    batch = subparsers.add_parser("batch-lookup", help="Resolve up to 100 IDs")
    batch.add_argument("entity_type")
    batch.add_argument("ids", nargs="+")
    batch.add_argument("--id-field", default="openalex_id")

    group = subparsers.add_parser("group-by", help="Aggregate entities by a field")
    group.add_argument("entity_type")
    group.add_argument("group_field")
    group.add_argument(
        "--filter", action="append", default=[], type=parse_filter, metavar="KEY=VALUE"
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = OpenAlexClient()

    if args.command == "search-works":
        result = client.search_works(
            search=args.query,
            filter_params=dict(args.filter),
            per_page=args.per_page,
            sort=args.sort,
            select=args.select or None,
        )
    elif args.command == "get-entity":
        result = client.get_entity(args.entity_type, args.entity_id)
    elif args.command == "batch-lookup":
        result = client.batch_lookup(args.entity_type, args.ids, args.id_field)
    else:
        result = client.group_by(
            args.entity_type,
            args.group_field,
            filter_params=dict(args.filter),
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

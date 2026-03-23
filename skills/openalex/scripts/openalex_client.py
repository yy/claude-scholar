#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""OpenAlex API client with rate limiting, retries, and cursor pagination."""

import time

import requests


class OpenAlexClient:
    """Client for the OpenAlex API (https://api.openalex.org)."""

    BASE_URL = "https://api.openalex.org"

    def __init__(self, email=None, requests_per_second=10):
        self.email = email
        self.min_delay = 1.0 / requests_per_second
        self.last_request_time = 0

    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()

    def get(self, endpoint, params=None, max_retries=5):
        """Make a GET request with rate limiting and exponential backoff."""
        params = dict(params or {})
        if self.email:
            params["mailto"] = self.email

        url = f"{self.BASE_URL}{endpoint}"
        for attempt in range(max_retries):
            try:
                self._rate_limit()
                resp = requests.get(url, params=params, timeout=30)
                if resp.status_code == 200:
                    return resp.json()
                if resp.status_code in (403, 429) or resp.status_code >= 500:
                    time.sleep(2**attempt)
                    continue
                resp.raise_for_status()
            except requests.exceptions.Timeout:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2**attempt)
        raise RuntimeError(f"Failed after {max_retries} retries: {endpoint}")

    def search_works(
        self, search=None, filter_params=None, per_page=200, sort=None, select=None
    ):
        """Search works with optional filters, sorting, and field selection."""
        params = {"per-page": min(per_page, 200)}
        if search:
            params["search"] = search
        if filter_params:
            params["filter"] = ",".join(f"{k}:{v}" for k, v in filter_params.items())
        if sort:
            params["sort"] = sort
        if select:
            params["select"] = ",".join(select)
        return self.get("/works", params)

    def get_entity(self, entity_type, entity_id):
        """Get a single entity by OpenAlex ID or external ID (DOI, ORCID, etc.)."""
        return self.get(f"/{entity_type}/{entity_id}")

    def batch_lookup(self, entity_type, ids, id_field="openalex_id"):
        """Look up multiple entities by ID (up to 50 per batch)."""
        results = []
        for i in range(0, len(ids), 50):
            batch = "|".join(ids[i : i + 50])
            resp = self.get(
                f"/{entity_type}", {"filter": f"{id_field}:{batch}", "per-page": 50}
            )
            results.extend(resp.get("results", []))
        return results

    def paginate_all(self, endpoint, params=None, max_results=None):
        """Paginate through all results using cursor-based pagination."""
        params = dict(params or {})
        params["per-page"] = 200
        params["cursor"] = "*"
        params.pop("page", None)

        results = []
        while True:
            resp = self.get(endpoint, params)
            page = resp.get("results", [])
            results.extend(page)
            if max_results and len(results) >= max_results:
                return results[:max_results]
            next_cursor = resp.get("meta", {}).get("next_cursor")
            if not next_cursor or not page:
                break
            params["cursor"] = next_cursor
        return results

    def group_by(self, entity_type, group_field, filter_params=None):
        """Aggregate results by a field (e.g., publication_year, topics.id)."""
        params = {"group_by": group_field}
        if filter_params:
            params["filter"] = ",".join(f"{k}:{v}" for k, v in filter_params.items())
        return self.get(f"/{entity_type}", params).get("group_by", [])

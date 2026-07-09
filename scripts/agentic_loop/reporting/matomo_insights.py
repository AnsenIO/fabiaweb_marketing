"""Matomo Reporting API client.

Fetches visits, actions, events and conversions from a self-hosted Matomo
instance. Requires a read-only token_auth.
"""

import os
from typing import Any, Optional
from urllib.parse import urlencode, urljoin

import requests


class MatomoInsights:
    def __init__(
        self,
        base_url: str,
        site_id: str | int,
        token_auth: Optional[str] = None,
    ):
        self.base_url = base_url.rstrip("/") + "/"
        self.site_id = str(site_id)
        self.token_auth = token_auth or os.environ.get("MATOMO_TOKEN_AUTH", "")

    def _api_url(self) -> str:
        return urljoin(self.base_url, "index.php")

    def _request(
        self,
        method: str,
        period: str = "day",
        date: str = "today",
        extra_params: Optional[dict[str, Any]] = None,
    ) -> Any:
        params: dict[str, Any] = {
            "module": "API",
            "format": "json",
            "idSite": self.site_id,
            "period": period,
            "date": date,
            "method": method,
        }
        if extra_params:
            params.update(extra_params)

        # Matomo requires token_auth as a POST parameter on this instance.
        data = {"token_auth": self.token_auth}
        resp = requests.post(self._api_url(), params=params, data=data, timeout=60)
        data = resp.json()
        if isinstance(data, dict) and data.get("result") == "error":
            raise RuntimeError(f"Matomo API error: {data.get('message', data)}")
        return data

    def visits_summary(self, period: str = "day", date: str = "today") -> dict:
        """Visits summary (nb_visits, nb_uniq_visitors, nb_actions, etc.)."""
        return self._request("VisitsSummary.get", period=period, date=date)

    def page_urls(
        self,
        period: str = "day",
        date: str = "today",
        flat: bool = True,
        filter_limit: int = 25,
    ) -> list[dict]:
        """Top page URLs for the period."""
        return self._request(
            "Actions.getPageUrls",
            period=period,
            date=date,
            extra_params={"flat": "1" if flat else "0", "filter_limit": filter_limit},
        )

    def events(
        self,
        period: str = "day",
        date: str = "today",
        filter_limit: int = 25,
    ) -> list[dict]:
        """Event categories/actions/names."""
        return self._request(
            "Events.getCategory",
            period=period,
            date=date,
            extra_params={"flat": "1", "filter_limit": filter_limit},
        )

    def conversions(self, period: str = "day", date: str = "today") -> dict:
        """Goal conversions summary (requires at least one goal)."""
        return self._request("Goals.get", period=period, date=date)

    def live_visits(self, limit: int = 10) -> list[dict]:
        """Last visits details (real-time)."""
        return self._request(
            "Live.getLastVisitsDetails",
            period="day",
            date="today",
            extra_params={"filter_limit": limit},
        )

    def print_summary(self, period: str = "day", date: str = "today") -> None:
        summary = self.visits_summary(period=period, date=date)
        if isinstance(summary, list):
            # Multi-date response
            print(f"Visits summary ({period} / {date}): multiple dates returned")
            for item in summary:
                print(item)
            return

        print(f"Matomo site {self.site_id} | {period} / {date}")
        print(
            f"  Visits: {summary.get('nb_visits', 0):>4} | "
            f"Unique: {summary.get('nb_uniq_visitor', summary.get('nb_uniq_visitors', 0))} | "
            f"Actions: {summary.get('nb_actions', 0)} | "
            f"Pageviews: {summary.get('nb_pageviews', 0)}"
        )

        top_pages = self.page_urls(period=period, date=date, filter_limit=10)
        if top_pages:
            print("\nTop pages:")
            for p in top_pages[:10]:
                label = p.get("label", "")
                visits = p.get("nb_visits", 0)
                hits = p.get("nb_hits", p.get("nb_pageviews", 0))
                print(f"  {label[:60]:60} | visits {visits:>4} | hits {hits:>4}")

        events = self.events(period=period, date=date, filter_limit=10)
        if events:
            print("\nTop event categories:")
            for e in events[:10]:
                label = e.get("label", "")
                count = e.get("nb_events", e.get("nb_visits", 0))
                print(f"  {label[:50]:50} | events {count:>4}")

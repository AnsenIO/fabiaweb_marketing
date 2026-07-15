#!/usr/bin/env python3
"""X/Twitter MCP server using OAuth 2.0 user-context auth."""

import os
import base64
import json
from pathlib import Path

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load env from project root
REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".." / "fabiabox_marketing" / ".env")

mcp = FastMCP("x_oauth2")

TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
BASE_URL = "https://api.twitter.com/2"


def _get_token() -> str:
    """Return a valid OAuth 2.0 access token, refreshing if needed."""
    access_token = os.getenv("ACCESS_TOKEN", "")
    refresh_token = os.getenv("REFRESH_TOKEN", "")
    client_id = os.getenv("CLIENT_ID", "")
    client_secret = os.getenv("CLIENT_SECRET", "")

    # Try current token with a lightweight v2 call
    test = requests.get(
        f"{BASE_URL}/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    if test.status_code == 200:
        return access_token

    # Refresh
    if not refresh_token:
        raise RuntimeError("Access token expired and no refresh token available")

    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    resp = requests.post(
        TOKEN_URL,
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=30,
    )
    resp.raise_for_status()
    token_data = resp.json()

    # Update in-memory env (won't persist to file, but enough for this process)
    os.environ["ACCESS_TOKEN"] = token_data["access_token"]
    if token_data.get("refresh_token"):
        os.environ["REFRESH_TOKEN"] = token_data["refresh_token"]

    return token_data["access_token"]


def _v2_post(endpoint: str, payload: dict) -> dict:
    token = _get_token()
    resp = requests.post(
        f"{BASE_URL}{endpoint}",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def _v2_get(endpoint: str, params: dict | None = None) -> dict:
    token = _get_token()
    resp = requests.get(
        f"{BASE_URL}{endpoint}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
def x_create_tweet(text: str) -> dict:
    """Create an X/Twitter tweet. Max 280 characters."""
    return _v2_post("/tweets", {"text": text})


@mcp.tool()
def x_reply(text: str, tweet_id: str) -> dict:
    """Reply to an X/Twitter tweet."""
    return _v2_post(
        "/tweets",
        {"text": text, "reply": {"in_reply_to_tweet_id": tweet_id}},
    )


@mcp.tool()
def x_get_profile(username: str) -> dict:
    """Get an X/Twitter user profile by username."""
    return _v2_get(f"/users/by/username/{username}", {"user.fields": "public_metrics,description"})


@mcp.tool()
def x_get_me() -> dict:
    """Get the authenticated user's profile."""
    return _v2_get("/users/me")


@mcp.tool()
def x_search_tweets(query: str, max_results: int = 10) -> dict:
    """Search X/Twitter tweets by keyword or phrase."""
    return _v2_get(
        "/tweets/search/recent",
        {"query": query, "max_results": min(max_results, 100), "tweet.fields": "author_id,created_at"},
    )


@mcp.tool()
def x_get_user_tweets(username: str, max_results: int = 10) -> dict:
    """Get recent tweets from a specific user."""
    profile = x_get_profile(username)
    user_id = profile["data"]["id"]
    return _v2_get(
        f"/users/{user_id}/tweets",
        {"max_results": min(max_results, 100), "tweet.fields": "created_at"},
    )


@mcp.tool()
def x_get_timeline(max_results: int = 10) -> dict:
    """Get the authenticated user's home timeline."""
    me = x_get_me()
    user_id = me["data"]["id"]
    return _v2_get(
        f"/users/{user_id}/timelines/reverse_chronological",
        {"max_results": min(max_results, 100), "tweet.fields": "created_at,author_id"},
    )


@mcp.tool()
def x_like(tweet_id: str) -> dict:
    """Like an X/Twitter tweet."""
    me = x_get_me()
    user_id = me["data"]["id"]
    return _v2_post(f"/users/{user_id}/likes", {"tweet_id": tweet_id})


@mcp.tool()
def x_retweet(tweet_id: str) -> dict:
    """Retweet an X/Twitter tweet."""
    me = x_get_me()
    user_id = me["data"]["id"]
    return _v2_post(f"/users/{user_id}/retweets", {"tweet_id": tweet_id})


@mcp.tool()
def x_follow(username: str) -> dict:
    """Follow an X/Twitter user by username."""
    me = x_get_me()
    user_id = me["data"]["id"]
    profile = x_get_profile(username)
    target_id = profile["data"]["id"]
    return _v2_post(f"/users/{user_id}/following", {"target_user_id": target_id})


if __name__ == "__main__":
    mcp.run(transport="stdio")

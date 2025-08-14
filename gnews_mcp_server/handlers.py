"""
GNews MCP Server Handlers

This module implements the tool functions for the GNews API MCP server.
It provides functions to search for news articles and get top headlines using the GNews API.
"""

import os
from datetime import datetime
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GNEWS_KEY = os.getenv("GNEWS_KEY")

# Base URL for GNews API
GNEWS_BASE_URL = "https://gnews.io/api/v4"


def validate_and_convert_date(date_str: str) -> str:
    """
    Validate YYYY-MM-DD date format and convert to ISO 8601 format for the API.

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        ISO 8601 formatted date string (YYYY-MM-DDTHH:MM:SS.sssZ)

    Raises:
        ValueError: If date format is invalid
    """
    try:
        # Parse the YYYY-MM-DD date
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        # Convert to ISO 8601 format expected by the API
        return date_obj.strftime("%Y-%m-%dT00:00:00.000Z")
    except ValueError:
        raise ValueError(
            f"Invalid date format: {date_str}. Use YYYY-MM-DD format (e.g., 2024-01-15)"
        )


async def make_gnews_request(endpoint: str, params: dict) -> dict:
    """Make a request to the GNews API with error handling."""
    if not GNEWS_KEY:
        raise ValueError(
            "GNews API key not set. Please set GNEWS_KEY environment variable."
        )

    # Add API key to params
    params["apikey"] = GNEWS_KEY

    # Construct URL
    url = f"{GNEWS_BASE_URL}/{endpoint}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)

            # Try to parse JSON response
            try:
                data = response.json()
            except Exception:
                data = None

            # Check for API errors
            if response.status_code != 200:
                if data and "errors" in data:
                    error_msg = (
                        data["errors"][0] if data["errors"] else "Unknown API error"
                    )
                else:
                    error_msg = response.text or f"HTTP {response.status_code}"
                raise ValueError(f"GNews API error: {error_msg}")

            return data

        except httpx.RequestError as e:
            raise ValueError(f"Request error: {e}")
        except Exception as e:
            if "GNews API error" in str(e) or "API key" in str(e):
                raise
            raise ValueError(f"Unexpected error: {e}")


async def search_news(query: str, **kwargs) -> dict:
    """
    Search for news articles using keywords with various filtering options.

    Args:
        query: Search keywords (required)
        language: 2-letter language code (default: 'en')
        country: 2-letter country code

        in: Attributes to search in (default: 'title,description')
        start_date: Filter articles published after this date (YYYY-MM-DD)
        end_date: Filter articles published before this date (YYYY-MM-DD)
        sortby: Sort by 'publishedAt' or 'relevance' (default: 'publishedAt')

    Returns:
        Dict containing totalArticles and articles array
    """
    # Extract parameters with defaults
    language = kwargs.get("language", "en")
    country = kwargs.get("country")
    max_articles = 10  # Fixed at 10 articles
    in_attr = kwargs.get("in", "title,description")
    start_date = kwargs.get("start_date")
    end_date = kwargs.get("end_date")
    sortby = kwargs.get("sortby", "publishedAt")

    # Validate required parameters
    if not query or not query.strip():
        raise ValueError("Search query 'query' is required and cannot be empty")

    # Validate and convert date formats if provided
    api_start_date = None
    api_end_date = None
    if start_date:
        api_start_date = validate_and_convert_date(start_date)
    if end_date:
        api_end_date = validate_and_convert_date(end_date)

    # Validate sortby parameter
    if sortby not in ["publishedAt", "relevance"]:
        raise ValueError("'sortby' must be 'publishedAt' or 'relevance'")

    # Validate language code format
    if len(language) != 2 or not language.isalpha():
        raise ValueError("'language' must be a 2-letter language code")

    # Validate country code format if provided
    if country and (len(country) != 2 or not country.isalpha()):
        raise ValueError("'country' must be a 2-letter country code")

    # Build request parameters
    params = {
        "q": query.strip(),
        "lang": language.lower(),  # API still expects 'lang' parameter
        "max": max_articles,
        "in": in_attr,
        "sortby": sortby,
    }

    # Add optional parameters
    if country:
        params["country"] = country.lower()
    if api_start_date:
        params["from"] = api_start_date  # API still expects 'from' parameter
    if api_end_date:
        params["to"] = api_end_date  # API still expects 'to' parameter

    # Make API request
    response = await make_gnews_request("search", params)

    return response


async def get_top_headlines(**kwargs) -> dict:
    """
    Get current trending news headlines based on Google News ranking.

    Args:
        category: News category (default: 'general')
        language: 2-letter language code (default: 'en')
        country: 2-letter country code

        start_date: Filter articles published after this date (YYYY-MM-DD)
        end_date: Filter articles published before this date (YYYY-MM-DD)
        query: Search keywords within headlines

    Returns:
        Dict containing totalArticles and articles array
    """
    # Extract parameters with defaults
    category = kwargs.get("category", "general")
    language = kwargs.get("language", "en")
    country = kwargs.get("country")
    max_articles = 10  # Fixed at 10 articles
    start_date = kwargs.get("start_date")
    end_date = kwargs.get("end_date")
    query = kwargs.get("query")

    # Validate category
    valid_categories = [
        "general",
        "world",
        "nation",
        "business",
        "technology",
        "entertainment",
        "sports",
        "science",
        "health",
    ]
    if category not in valid_categories:
        raise ValueError(f"'category' must be one of: {', '.join(valid_categories)}")

    # Validate and convert date formats if provided
    api_start_date = None
    api_end_date = None
    if start_date:
        api_start_date = validate_and_convert_date(start_date)
    if end_date:
        api_end_date = validate_and_convert_date(end_date)

    # Validate language code format
    if len(language) != 2 or not language.isalpha():
        raise ValueError("'language' must be a 2-letter language code")

    # Validate country code format if provided
    if country and (len(country) != 2 or not country.isalpha()):
        raise ValueError("'country' must be a 2-letter country code")

    # Build request parameters
    params = {
        "category": category,
        "lang": language.lower(),  # API still expects 'lang' parameter
        "max": max_articles,
    }

    # Add optional parameters
    if country:
        params["country"] = country.lower()
    if api_start_date:
        params["from"] = api_start_date  # API still expects 'from' parameter
    if api_end_date:
        params["to"] = api_end_date  # API still expects 'to' parameter
    if query:
        params["q"] = query.strip()

    # Make API request
    response = await make_gnews_request("top-headlines", params)

    return response


# Tool function mapping
TOOL_FUNCTIONS = {
    "search_news": search_news,
    "get_top_headlines": get_top_headlines,
}

# GNews MCP Server

A Model Context Protocol (MCP) server for fetching news articles and headlines using the GNews API.

## Features

- **Search News**: Search for news articles using keywords with various filtering options
- **Top Headlines**: Get current trending headlines based on Google News ranking
- **Comprehensive Filtering**: Filter by language, country, date range, category, and more
- **Schema Validation**: Full input/output validation using JSON Schema
- **Error Handling**: Robust error handling and meaningful error messages

## Installation

### Prerequisites

- Python 3.11 or higher
- [UV package manager](https://github.com/astral-sh/uv)
- GNews API key from [gnews.io](https://gnews.io/)

### Install from Git

```bash
uvx --from git+https://github.com/yourusername/gnews-mcp-server gnews-server
```

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gnews-mcp-server.git
   cd gnews-mcp-server
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Set up environment variables:
   ```bash
   # Create .env file
   echo "GNEWS_KEY=your_gnews_api_key_here" > .env
   ```

4. Run tests:
   ```bash
   uv run python test_server.py
   ```

## Configuration

### Environment Variables

- `GNEWS_KEY` (required): Your GNews API key from [gnews.io](https://gnews.io/)
- `DEBUG` (optional): Set to `true` for debug logging

### Getting a GNews API Key

1. Visit [gnews.io](https://gnews.io/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Set it as the `GNEWS_KEY` environment variable

## Available Tools

### 1. search_news

Search for news articles using keywords with various filtering options.

**Parameters:**
- `q` (required): Search keywords (supports logical operators AND, OR, NOT)
- `language`: 2-letter language code (default: "en") - supported values: ar, zh, nl, en, fr, de, el, hi, it, ja, ml, mr, no, pt, ro, ru, es, sv, ta, te, uk
- `country`: 2-letter country code - supported values: au, br, ca, cn, eg, fr, de, gr, hk, in, ie, it, jp, nl, no, pk, pe, ph, pt, ro, ru, sg, se, ch, tw, ua, gb, us
- `in`: Search in "title", "description", "content" (default: "title,description")
- `sortby`: Sort by "publishedAt" or "relevance" (default: "publishedAt")
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format

Returns exactly 10 articles.

**Example:**
```json
{
  "q": "artificial intelligence",
  "language": "en",
  "country": "us",
  "sortby": "relevance",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

### 2. get_top_headlines

Get current trending headlines based on Google News ranking.

**Parameters:**
- `category`: Category ("general", "world", "nation", "business", "technology", "entertainment", "sports", "science", "health") - default: "general"
- `language`: 2-letter language code (default: "en") - supported values: ar, zh, nl, en, fr, de, el, hi, it, ja, ml, mr, no, pt, ro, ru, es, sv, ta, te, uk
- `country`: 2-letter country code - supported values: au, br, ca, cn, eg, fr, de, gr, hk, in, ie, it, jp, nl, no, pk, pe, ph, pt, ro, ru, sg, se, ch, tw, ua, gb, us
- `q`: Search keywords within headlines
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format

Returns exactly 10 articles.

**Example:**
```json
{
  "category": "technology",
  "language": "en",
  "country": "us"
}
```

## MCP Client Configuration

### Claude Desktop

Add to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "gnews": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/yourusername/gnews-mcp-server",
        "gnews-server"
      ],
      "env": {
        "GNEWS_KEY": "your_gnews_api_key_here"
      }
    }
  }
}
```

### Other MCP Clients

The server communicates using the standard MCP protocol over stdio. Refer to your MCP client's documentation for configuration details.

## Query Syntax

The GNews API supports advanced query syntax for the `q` parameter:

### Phrase Search
- `"Apple iPhone"` - Exact phrase matching

### Logical Operators
- `Apple AND iPhone` - Both terms must be present
- `Apple OR Microsoft` - Either term must be present
- `Apple NOT iPhone` - First term without second term

### Complex Queries
- `(Apple AND iPhone) OR (Google AND Pixel)` - Complex logical combinations
- `"machine learning" AND NOT "deep learning"` - Phrase with exclusion

## Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| Arabic | ar | Italian | it |
| Chinese | zh | Japanese | ja |
| Dutch | nl | Norwegian | no |
| English | en | Portuguese | pt |
| French | fr | Russian | ru |
| German | de | Spanish | es |
| Greek | el | Swedish | sv |
| Hindi | hi | Ukrainian | uk |

## Supported Countries

| Country | Code | Country | Code |
|---------|------|---------|------|
| Australia | au | Japan | jp |
| Brazil | br | Netherlands | nl |
| Canada | ca | Norway | no |
| China | cn | Pakistan | pk |
| Egypt | eg | Portugal | pt |
| France | fr | Singapore | sg |
| Germany | de | Spain | es |
| India | in | Sweden | se |
| Italy | it | United Kingdom | gb |
| United States | us | (and more...) |

## Testing

The server includes comprehensive tests:

```bash
# Run all tests
uv run python test_server.py

# Test features:
# - Schema validation
# - Input/output validation  
# - Error handling
# - Tool functionality
```

## Development

### Project Structure

```
gnews-mcp-server/
├── gnews_mcp_server/
│   ├── __init__.py
│   ├── __main__.py         # Entry point
│   ├── server.py           # MCP server implementation
│   ├── handlers.py         # Tool implementations
│   └── tools.json          # Tool schemas
├── test_cases.json         # Test definitions
├── test_server.py          # Test framework
├── pyproject.toml          # Project configuration
└── README.md
```

### Adding New Features

1. Update tool schemas in `gnews_mcp_server/tools.json`
2. Implement tool functions in `gnews_mcp_server/handlers.py`
3. Add tests to `test_cases.json`
4. Run tests: `uv run python test_server.py`

## Error Handling

The server provides comprehensive error handling:

- **Validation Errors**: Invalid parameters are caught and reported
- **API Errors**: GNews API errors are properly formatted
- **Network Errors**: Connection issues are handled gracefully
- **Schema Validation**: Input/output validation ensures data integrity

## Rate Limits

GNews API rate limits depend on your subscription plan:
- **Free**: 100 requests per day
- **Paid Plans**: Higher limits available

The server will return appropriate error messages when rate limits are exceeded.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- [GNews API Documentation](https://gnews.io/docs/)
- [MCP Protocol Specification](https://github.com/modelcontextprotocol)
- [Issues and Bug Reports](https://github.com/yourusername/gnews-mcp-server/issues)

## Changelog

### v0.1.0
- Initial release
- Search news functionality
- Top headlines functionality
- Comprehensive schema validation
- Full test suite
# Link Extraction Tool

A small data-collection utility that extracts links from an HTML file and exports
them as a clean CSV dataset.

This project is intentionally simple and is being improved as a portfolio-friendly
data engineering starter project.

## What It Does

- Parses an input HTML file for `<a href="...">` links
- Converts relative links to absolute links
- Deduplicates and sorts links
- Writes output to CSV with a `Link` header
- Exposes a reusable CLI interface

## Project Structure

- `link_scraper5.py` - core extraction logic + CLI entrypoint
- `tests/test_link_scraper5.py` - automated tests for core behavior
- `requirements.txt` - project dependencies

## Quick Start

1. Create and activate a virtual environment
2. Install dependencies
3. Run the scraper

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python link_scraper5.py --input path/to/bookmarks.html --output links.csv
```

## CLI Usage

```bash
python link_scraper5.py --help
```

Arguments:

- `--input` (required): Path to input HTML file
- `--output` (optional): Output CSV path (default: `links.csv`)

## Example Output

```csv
Link
https://example.com
https://example.com/docs
```

## Run Tests

```bash
python -m pytest
```

## Why This Is Useful

This tool is a practical first step for:

- bookmark mining,
- source catalog building,
- and simple web-data ingestion workflows.

It demonstrates data cleaning fundamentals (normalization, deduplication,
deterministic sorting) in a compact pipeline.

## Next Improvements

- Add metadata extraction (domain, path, query params)
- Add optional JSON/Parquet outputs
- Add SQLite/PostgreSQL sink
- Add CI workflow and linting

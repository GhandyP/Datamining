import argparse
import csv
import importlib
import logging
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

LOGGER = logging.getLogger("link_scraper")


class HrefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for key, value in attrs:
            if key == "href" and value:
                self.links.append(value)


def extract_links(html_content: str, base_url: str) -> list[str]:
    try:
        scrapy_http = importlib.import_module("scrapy.http")
        text_response_cls = getattr(scrapy_http, "TextResponse")
        response = text_response_cls(
            url=base_url, body=html_content.encode("utf-8"), encoding="utf-8"
        )
        links = response.css("a::attr(href)").getall()
        absolute_links = [response.urljoin(link) for link in links]
    except ImportError:
        parser = HrefParser()
        parser.feed(html_content)
        absolute_links = [urljoin(base_url, link) for link in parser.links]

    return sorted(set(absolute_links))


def write_csv(links: list[str], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Link"])
        for link in links:
            csv_writer.writerow([link])


def scrape_links(input_path: Path, output_path: Path) -> int:
    if not input_path.exists():
        raise FileNotFoundError(f"Input HTML file not found: {input_path}")

    html_content = input_path.read_text(encoding="utf-8")
    base_url = input_path.resolve().as_uri()

    links = extract_links(html_content, base_url)
    write_csv(links, output_path)

    LOGGER.info("Saved %d unique links to %s", len(links), output_path)
    return len(links)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract unique links from an HTML file."
    )
    parser.add_argument("--input", required=True, help="Path to input HTML file.")
    parser.add_argument(
        "--output", default="links.csv", help="Path to output CSV file."
    )
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    try:
        scrape_links(input_path=input_path, output_path=output_path)
        return 0
    except FileNotFoundError as error:
        LOGGER.error(str(error))
        return 1
    except Exception as error:  # pragma: no cover
        LOGGER.exception("Unexpected error: %s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

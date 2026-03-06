import csv
import re
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urljoin

import pytest

import link_scraper5


class FakeSelector:
    def __init__(self, links: list[str]):
        self._links = links

    def getall(self) -> list[str]:
        return self._links


class FakeTextResponse:
    def __init__(self, url: str, body: bytes, encoding: str):
        self.url = url
        self._html = body.decode(encoding)

    def css(self, query: str) -> FakeSelector:
        assert query == "a::attr(href)"
        links = re.findall(r'href=["\']([^"\']+)["\']', self._html)
        return FakeSelector(links)

    def urljoin(self, link: str) -> str:
        return urljoin(self.url, link)


@pytest.fixture
def fake_scrapy(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_module = SimpleNamespace(TextResponse=FakeTextResponse)
    monkeypatch.setattr(
        link_scraper5.importlib,
        "import_module",
        lambda module_name: fake_module,
    )


def test_extract_links_deduplicates_and_sorts(fake_scrapy: None) -> None:
    html = """
    <html><body>
      <a href="/z">Zed</a>
      <a href="https://example.com/a">A</a>
      <a href="/z">Duplicate</a>
      <a href="b">Bee</a>
    </body></html>
    """

    links = link_scraper5.extract_links(html, "https://example.com/base/index.html")

    assert links == [
        "https://example.com/a",
        "https://example.com/base/b",
        "https://example.com/z",
    ]


def test_scrape_links_raises_for_missing_input(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        link_scraper5.scrape_links(
            input_path=tmp_path / "missing.html",
            output_path=tmp_path / "links.csv",
        )


def test_scrape_links_writes_csv_with_header(fake_scrapy: None, tmp_path: Path) -> None:
    input_html = tmp_path / "bookmarks.html"
    output_csv = tmp_path / "links.csv"
    input_html.write_text(
        """
        <a href="/beta">Beta</a>
        <a href="https://example.com/alpha">Alpha</a>
        <a href="/beta">Beta Duplicate</a>
        """,
        encoding="utf-8",
    )

    count = link_scraper5.scrape_links(input_path=input_html, output_path=output_csv)

    assert count == 2
    with output_csv.open("r", encoding="utf-8", newline="") as csv_file:
        rows = list(csv.reader(csv_file))

    assert rows == [
        ["Link"],
        ["file:///beta"],
        ["https://example.com/alpha"],
    ]

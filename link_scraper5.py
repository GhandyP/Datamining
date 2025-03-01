import scrapy
import csv

class LinkSpider(scrapy.Spider):
    name = 'linkspider'
    start_urls = ['file:///c:/Users/ghand/Documents/favoritos/favoritos_01_03_25.html']

    def parse(self, response):
        links = response.css('a::attr(href)').getall()
        absolute_links = [response.urljoin(link) for link in links]
        sorted_links = sorted(list(set(absolute_links)))

        csv_data = [['Link']]
        for link in sorted_links:
            csv_data.append([link])

        csv_filename = 'links.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(csv_data)

        self.log(f'Saved {len(sorted_links)} unique links to {csv_filename}')
"""
Scrapy spider for ikman.lk vehicle listings.
"""

# import scrapy


class IkmanSpider:
    """Spider that crawls ikman.lk vehicle category pages."""

    name = "ikman"
    start_urls = ["https://ikman.lk/en/ads/sri-lanka/vehicles"]

    def parse(self, response):
        """Parse listing index pages and follow pagination."""
        # TODO: implement Scrapy spider logic
        ...

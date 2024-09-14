from abc import ABC, abstractmethod


"""
爬虫的接口.
"""
class CrawlerBase(ABC):
    @abstractmethod
    def crawl(self):
        pass
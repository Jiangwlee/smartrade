from crawlers.utils.logger import get_logger

logger = get_logger()

def crawl():
    logger.info("Hello world, let's crawl")


if __name__ == '__main__':
    crawl()
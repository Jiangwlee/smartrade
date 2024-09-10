from crawlers.utils.logger import getLogger

logger = getLogger()

def crawl():
    logger.info("Hello world, let's crawl")


if __name__ == '__main__':
    crawl()
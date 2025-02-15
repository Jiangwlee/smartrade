"""
服务层: 封装主要业务逻辑.
"""

from crawlers.db.downloader import Downloader
from crawlers.utils.dateutil import compare_date
from crawlers.utils.logger import get_logger
from crawlers.experiment.dataset import DatasetGenerator

log = get_logger()

def download_hangqing(start: str, end: str):
    """
    下载行情并存入数据库.
    --
    @param start: 起始日期. 格式为 %Y%m%d, 比如: 20240101
    @param end:   结束日期. 格式为 %Y%m%d, 比如: 20240102
    """
    if compare_date(start, end) == 1:
        log.warning(f"起始日期 {start} 大于结束日期 {end}.")
        return
    downloader = Downloader(start, end)
    downloader.run()

def make_dataset(start: str, end: str, filepath: str, is_for_train: bool):
    """
    构建数据集.
    --
    @param start: 起始日期. 格式为 %Y%m%d, 比如: 20240101
    @param end:   结束日期. 格式为 %Y%m%d, 比如: 20240102
    @param filepath: File path
    @param is_for_train: True for train, False for prediction
    """
    if compare_date(start, end) == 1:
        log.warning(f"起始日期 {start} 大于结束日期 {end}.")
        return
    generator = DatasetGenerator(start, end, is_for_train)
    generator.generate()
    generator.save(filepath)


if __name__ == '__main__':
    # download_one_day('20240912')
    # make_dataset('20240913', '20240913', "C:\\Users\\admin\\Downloads\\dataset-240913.csv", False)
    download_hangqing('20240918', '20240918')
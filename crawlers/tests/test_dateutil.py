from datetime import datetime
from crawlers.utils.dateutil import previousDate, DateIterator, offsetInMinutes, getLastNTradeDate

def test_previousDate():
    assert previousDate('20240913') == '20240912'

def test_dateIterator():
    iter = DateIterator("20240831", "20240902")
    assert iter.next() == '20240831'
    assert iter.next() == '20240901'
    assert iter.next() == '20240902'
    assert iter.next() == '20240902'
    assert iter.prev() == '20240901'
    assert iter.prev() == '20240831'
    assert iter.prev() == '20240831'
    assert iter.next() == '20240901'

def test_dateIterator_with_validator():
    validator = lambda x : x in ["20240905"]
    iter = DateIterator("20240831", "20240910", validator=validator)
    assert iter.next() == '20240905'
    assert iter.next() == '20240910'

def test_offsetInMinutes():
    assert offsetInMinutes(datetime.strptime("2024-01-01 09:30:00", "%Y-%m-%d %H:%M:%S")) == 5
    assert offsetInMinutes(datetime.strptime("2024-01-01 09:31:00", "%Y-%m-%d %H:%M:%S")) == 6
    assert offsetInMinutes(datetime.strptime("2024-01-01 09:32:30", "%Y-%m-%d %H:%M:%S")) == 7

def test_getLastNTradeDate():
    result = getLastNTradeDate(180)
    assert len(result) == 180
    assert result[0] < result[-1]
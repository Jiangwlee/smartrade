from crawlers.utils.hqutil import tag_stock

def test_tag_stock():
    assert tag_stock('002205', 44700, 44700, 40600, 44700, 44700) == '一字板'
    assert tag_stock('002593', 94100, 81700, 90800, 99900, 81700) == '天地板'
    assert tag_stock('002593', 90800, 99900, 90800, 99900, 81700) == '地天板'
    assert tag_stock('600824', 53000, 53000, 48200, 53000, 51000) == 'T字板'
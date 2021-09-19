import pytest

from sgcarmart_crawler.crawler import crawl_from_sgcarmart


def test_crawler_used_car_listing():
    output = crawl_from_sgcarmart("https://www.sgcarmart.com/used_cars/info.php?ID=1020939&DL=3283")
    assert output["success"] == True
    assert output["payload"]["price"] == "$19,800"
    assert output["payload"]["open_market_value"] == "$11,333"

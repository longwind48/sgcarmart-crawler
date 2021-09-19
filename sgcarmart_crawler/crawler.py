from lxml import html
import requests
import itertools
from typing import List, Any, Dict


def flatten_car_info_entities(entities: List[Any]) -> List[str]:
    """Turn list of 'lxml.html.HtmlElement' elements into a flatten list of str
    Args:
        entities (List[Any]): list of 'lxml.html.HtmlElement' elements, generated from tree.xpath()

    Returns:
        List[str]: List of extracted strings from xpath
    """
    entities_raw = [x.text_content().split() for x in entities]
    entities_list = list(itertools.chain.from_iterable(entities_raw))
    return entities_list


def extract_entities_a(tree: html.HtmlElement) -> Dict:
    """Scrape car info stage A

    Args:
        tree (html.HtmlElement): html element object generated from page.content

    Returns:
        Dict: dict of relevant car info key-value pairs
    """
    entities_a = tree.xpath("//tr[@class='row_bg']")
    entities_list = flatten_car_info_entities(entities_a)
    output = dict(price=entities_list[1], depreciation=entities_list[3], coe_registration_date=entities_list[7][:11])
    return output


def extract_entities_b(tree: html.HtmlElement) -> Dict:
    """Scrap car info stage B

    Args:
        tree (html.HtmlElement): html element object generated from page.content

    Returns:
        Dict: dict of relevant car info key-value pairs
    """
    entities_b = tree.xpath("//tr/td[@class='even_row']")
    entities_list = flatten_car_info_entities(entities_b)
    output = dict(
        mileage=" ".join(entities_list[1:3]),
        road_tax=entities_list[7],
        deregistration_value=entities_list[11],
        coe=entities_list[17],
        engine_cap=entities_list[20],
        curb_weight=" ".join(entities_list[24:26]),
        manufactured_year=entities_list[27],
        transmission=entities_list[29],
        open_market_value=entities_list[31],
        additional_registration_fee=entities_list[33],
        power=" ".join(entities_list[35:39]),
        number_of_owners=entities_list[-1],
    )
    return output


def crawl_from_sgcarmart(url: str) -> Dict:
    """Crawl car info from sgcarmart listing

    Args:
        url (str): url of car listing

    Returns:
        Dict: payload containing extracted car info of car listing
    """
    page = requests.get(url)
    extracted_dict = dict(success=False, url=url, payload={})
    if page.status_code != 200:
        return extracted_dict

    tree = html.fromstring(page.content)
    extracted_dict["success"] = True
    extracted_dict["payload"].update(extract_entities_a(tree))
    extracted_dict["payload"].update(extract_entities_b(tree))
    return extracted_dict


print(crawl_from_sgcarmart("https://www.sgcarmart.com/used_cars/info.php?ID=1020939&DL=3283"))

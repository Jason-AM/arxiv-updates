import xml.etree.ElementTree as et

import requests
from ratelimit import limits, sleep_and_retry

BASE_XML_TAG = "{http://purl.org/rss/1.0/}"


def _get_title(xml_element):
    title_text_uncleaned = xml_element.find(f"{BASE_XML_TAG}title").text
    return title_text_uncleaned.split(". (")[0]


def _get_link(xml_element):
    return xml_element.find(f"{BASE_XML_TAG}link").text


def _get_abstract(xml_element):
    """Set up for future use"""
    abstract_uncleaned = xml_element.find(f"{BASE_XML_TAG}description").text
    return abstract_uncleaned.replace("<p>", "").replace("</p>", "")


@sleep_and_retry
@limits(calls=1, period=3)
def get_title_link_abs_from_rss(topic: str):

    reqested = requests.get(f"http://arxiv.org/rss/{topic}")
    requested_content = reqested.content
    root = et.fromstring(requested_content)

    titles_and_links = {
        (_get_title(child), _get_link(child), _get_abstract(child))
        for child in root.findall(f"{BASE_XML_TAG}item")
    }

    return titles_and_links

import re
import urllib.parse as urlparse

import tldextract

from pyutils.text import regex_lib

# TODO: get repeated urls (clean first)


DOMAIN_CORRECTIONS = {
    'youtu': 'youtube'
}


def get_urls(text):
    regex = re.compile(regex_lib.url())

    return regex.findall(text)


def get_domain(url):
    extract_result = tldextract.extract(url)

    domain = ''
    if extract_result.subdomain not in ['', 'www']:
        domain += f'{extract_result.subdomain}.'

    domain += extract_result.domain

    return DOMAIN_CORRECTIONS.get(domain, domain)


def get_unique_domains(urls):
    domains = [get_domain(url) for url in urls]
    return list(set(domains))


def get_links_from_domains(domains, urls):
    return [url for url in urls if get_domain(url) in domains]


def split_url(url):
    """Slipts a url in endpoint and query parameters.
    """
    parsed_url = urlparse.urlparse(url)

    endpoint = parsed_url.netloc + parsed_url.path
    query_params = urlparse.parse_qs(parsed_url.query)

    return endpoint, query_params


def clean_url(url):
    """Removes query part (returns netloc + path).
    """
    parsed_url = urlparse.urlparse(url)
    return parsed_url.netloc + parsed_url.path

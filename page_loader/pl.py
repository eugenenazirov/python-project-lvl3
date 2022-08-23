from urllib.error import HTTPError
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
import logging


headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 \
                Safari/537.36"}


def make_soup(html_file):
    return BeautifulSoup(html_file, 'html.parser')


def get_html_page(link):
    response = requests.get(link, headers=headers)
    text = response.text
    status = response.status_code
    if status != 200:
        logging.error(f'Bad request! URL: {link}. Status: {status}')
        raise HTTPError(
            code=status,
            msg=f"Bad request! HTML page {link=} won't be downloaded.",
            hdrs=response.headers,
            fp=response.raw,
            url=link)
    return text


def get_tags(src_soup, tag_type):
    return src_soup.find_all(tag_type)


def get_link_tags(src_soup):
    return src_soup.find_all('link')


def has_protocol(link: str):
    if not link:
        return
    return any((link.startswith('http'), link.startswith('https')))


def is_local(src_url: str, resource_url: str):
    src_host = urlparse(src_url).hostname
    resource_host = urlparse(resource_url).hostname
    same_hosts = src_host == resource_host
    doesnt_have_protocol = not has_protocol(resource_url)
    return same_hosts or doesnt_have_protocol


def make_full_link(src_url, resource_link):
    logging.debug('Making full web link to download...')
    site = os.path.split(src_url)[0]
    return urljoin(site, resource_link)


def process_tag(tag, params):
    logging.debug(f"Start to process {tag=}")
    if tag.name == ('link'):
        logging.debug('Got link tag to process')
        resource_link = tag.get('href')
    else:
        logging.debug('Got tag to process')
        resource_link = tag.get('src')

    src_link = params.get('src_link')
    output_path = params.get('output_path')
    name = params.get('name')

    if not all((resource_link, is_local(
            src_url=src_link,
            resource_url=resource_link))):
        logging.debug(f"{resource_link} is not local. It won't be downloaded.")
        return

    original_link = resource_link
    if not has_protocol(resource_link):
        logging.debug(f"{resource_link} doesn't have any protocol.\
             Need to make full web link to downloaded.")
        resource_link = make_full_link(src_link, resource_link)
        logging.debug("Full web link made successfully.")
    path_to_resource = save_resource(resource_link, output_path, name)
    logging.debug("Resource has been downloaded.")
    return original_link, path_to_resource


def download_resource(tags, params):
    old_and_new_links = []
    for tag in tags:
        old_and_new_links.append(process_tag(tag, params=params))
    return old_and_new_links


def make_file_name(url: str, file_ext='.html'):
    root_ext = os.path.splitext(url)
    parse_link = root_ext[0]
    parse_link = url.split('/')
    parse_link.pop(0)
    parse_link.pop(0)
    if url.endswith('/'):
        parse_link.pop(-1)
    if url.endswith(file_ext):
        link_end = os.path.splitext(parse_link[-1])
        parse_link.pop(-1)
        parse_link.append(link_end[0])
    parse_link_to_str = '-'.join(parse_link)
    spec_sym_to_dash = ''
    for char in parse_link_to_str:
        if not char.isalnum():
            spec_sym_to_dash += '-'
        else:
            spec_sym_to_dash += char
    result = spec_sym_to_dash + file_ext
    return result


def replace_link(html_file, src_link, local_link):
    if src_link in html_file:
        html_file = html_file.replace(src_link, local_link)
    return html_file


def change_links(html: str, links: list):
    for link_pair in links:
        if link_pair:
            src_link = link_pair[0]
            local_link = link_pair[1]
            html = replace_link(html, src_link, local_link)
    return html


def save_resource(url, path, name):
    response = requests.get(url)
    content = response.content
    status = response.status_code

    if status != 200:
        logging.error(f'Bad request! URL: {url}. Status: {status}')
        raise HTTPError(
            code=status,
            msg=f"Bad request! Resource: {url} won't be downloaded.",
            hdrs=response.headers,
            fp=response.raw,
            url=url
        )

    dir_name = os.path.splitext(name)[0] + '_files'
    dir_path = os.path.join(path, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    file_ext = os.path.splitext(url)[1]
    if file_ext:
        local_name = make_file_name(url, file_ext=file_ext)
    else:
        local_name = make_file_name(url)

    local_full_path = os.path.join(dir_path, local_name)
    local_tag_path = os.path.join(dir_name, local_name)

    with open(local_full_path, 'wb') as f:
        f.write(content)
    return local_tag_path

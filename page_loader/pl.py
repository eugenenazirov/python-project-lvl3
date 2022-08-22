import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin


headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 \
                Safari/537.36"}


def make_soup(html_file):
    return BeautifulSoup(html_file, 'html.parser')


def get_html_page(link):
    return requests.get(link, headers=headers).text


def get_img_tags(src_soup):
    return src_soup.find_all('img')


def has_protocol(link: str):
    return any((link.startswith('http'), link.startswith('https')))


def is_local(src_url: str, resource_url: str):
    src_host = urlparse(src_url).hostname
    resource_host = urlparse(resource_url).hostname
    same_hosts = src_host == resource_host
    doesnt_have_protocol = not has_protocol(resource_url)
    return same_hosts or doesnt_have_protocol


def make_full_link(src_url, img_link):
    site = os.path.split(src_url)[0]
    return urljoin(site, img_link)


def save_img(url, path, name):
    img_content = requests.get(url).content
    dir_name = os.path.splitext(name)[0] + '_files'
    dir_path = os.path.join(path, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    assets_path = os.path.join(dir_path, 'assets')
    if not os.path.exists(assets_path):
        os.mkdir(assets_path)
    local_name = os.path.split(url)[1]
    local_full_path = os.path.join(assets_path, local_name)
    local_tag_path = os.path.join(dir_name, 'assets', local_name)
    with open(local_full_path, 'wb') as f:
        f.write(img_content)
    return local_tag_path


def process_tag(tag, params):
    if tag.name == ('link'):
        resource_link = tag.get('href')
    else:
        resource_link = tag.get('src')

    src_link = params.get('src_link')
    output_path = params.get('output_path')
    name = params.get('name')

    if not all((resource_link, is_local(
            src_url=src_link,
            resource_url=resource_link))):
        return

    original_link = resource_link
    if not has_protocol(resource_link):
        resource_link = make_full_link(src_link, resource_link)
    path_to_img = save_resource(resource_link, output_path, name)

    return original_link, path_to_img


def download_resource(img_tags, params):
    old_and_new_links = []
    for tag in img_tags:
        old_and_new_links.append(process_tag(tag, params=params))
    return old_and_new_links


def make_file_name(url: str, file_ext='.html'):
    root_ext = os.path.splitext(url)
    parse_link = root_ext[0]
    parse_link = url.split('/')
    parse_link.pop(0)
    parse_link.pop(0)
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


def change_links(html: str, links: list):
    for link_pair in links:
        if link_pair:
            src_link = link_pair[0]
            local_link = link_pair[1]
        if src_link in html:
            html = html.replace(src_link, local_link)
    return html


def get_link_tags(src_soup):
    return src_soup.find_all('link')


def save_resource(url, path, name):
    content = requests.get(url).content
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

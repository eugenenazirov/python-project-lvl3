import requests
import os
from bs4 import BeautifulSoup


headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 \
                Safari/537.36"}


def get_html_page(link):
    return requests.get(link, headers=headers).text


def make_file_name(link: str):
    root_ext = os.path.splitext(link)
    parse_link = root_ext[0]
    parse_link = link.split('/')
    parse_link.pop(0)
    parse_link.pop(0)
    if link.endswith('.html'):
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
    result = spec_sym_to_dash + '.html'
    return result


def get_img_tags(src_soup):
    return src_soup.find_all('img')


def is_link_local(link):
    return not any((link.startswith('http'), link.startswith('https')))


def make_full_link(src_link, img_link):
    site = os.path.split(src_link)[0]
    return site + '/' + img_link


def save_img(link, path, name):
    img_content = requests.get(link).content
    dir_name = os.path.splitext(name)[0] + '_files'
    dir_path = os.path.join(path, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    assets_path = os.path.join(dir_path, 'assets')
    if not os.path.exists(assets_path):
        os.mkdir(assets_path)
    local_name = os.path.split(link)[1]
    local_full_path = os.path.join(assets_path, local_name)
    local_tag_path = os.path.join(dir_name, 'assets', local_name)
    with open(local_full_path, 'wb') as f:
        f.write(img_content)
    return local_tag_path


def download_images(src_link, img_tags, output_path, name):
    old_and_new_links = []
    for tag in img_tags:
        img_link = tag.get('src')
        if img_link:
            img_link_original = img_link
            if is_link_local(img_link):
                img_link = make_full_link(src_link, img_link)
            path_to_img = save_img(img_link, output_path, name)
            old_and_new_links.append((img_link_original, path_to_img))
    return old_and_new_links


def change_image_links(html: str, links: list):
    for link_pair in links:
        src_link = link_pair[0]
        local_link = link_pair[1]
        if src_link in html:
            html = html.replace(src_link, local_link)
    return html


def make_soup(html_file):
    return BeautifulSoup(html_file, 'html.parser')

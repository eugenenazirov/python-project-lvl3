import requests
import os
from bs4 import BeautifulSoup


# tmp_dir = tempfile.TemporaryDirectory()

# tmp_name = tmp_dir.name
# print(type(tmp_name))

# path = Path(tmp_name, 'hexlet.html')
# print(path)

def make_file_name(link: str):
    root_ext = os.path.splitext(link)
    parse_link = root_ext[0]
    parse_link = link.split('/')
    parse_link.pop(0)
    parse_link.pop(0)
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


def save_img(link, img, path, name):
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
    with open(local_full_path, 'w') as f:
        f.write(img)
    return local_tag_path


def download_images(img_tags, output_path, name):
    old_and_new_links = []
    for tag in img_tags:
        link = tag.get('src')
        img_text = requests.get(link).text
        path_to_img = save_img(link, img_text, output_path, name)
        old_and_new_links.append((link, path_to_img))
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


def download(link, output):
    src = requests.get(link).text
    filename = make_file_name(link)
    soup = make_soup(src)
    src_img_tags = get_img_tags(soup)
    web_and_local_links = download_images(src_img_tags, output, filename)
    soup_html = soup.prettify()
    html_localized_img = change_image_links(soup_html, web_and_local_links)
    output_path = os.path.join(output, filename)
    with open(output_path, 'w+') as output_file:
        output_file.write(html_localized_img)
    return output_path

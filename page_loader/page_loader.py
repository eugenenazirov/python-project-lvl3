from page_loader import pl
import os


def download(url, output):
    src = pl.get_html_page(url)
    filename = pl.make_file_name(url)
    soup = pl.make_soup(src)
    soup_html = soup.prettify()

    params = {
        'src_link': url,
        'output_path': output,
        'name': filename
    }

    src_img_tags = pl.get_img_tags(soup)
    web_and_local_links = []
    web_and_local_links.extend(pl.download_resource(src_img_tags, params))

    src_link_tags = pl.get_link_tags(soup)
    web_and_local_links.extend(pl.download_resource(src_link_tags, params))

    localized_html = pl.change_links(soup_html, web_and_local_links)
    output_path = os.path.join(output, filename)
    with open(output_path, 'w+') as output_file:
        output_file.write(localized_html)
    return output_path

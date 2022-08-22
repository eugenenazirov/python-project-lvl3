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

    web_and_local_links = []

    img_tags = pl.get_tags(soup, 'img')
    web_and_local_links.extend(pl.download_resource(img_tags, params))

    link_tags = pl.get_tags(soup, 'link')
    web_and_local_links.extend(pl.download_resource(link_tags, params))

    script_tags = pl.get_tags(soup, 'script')
    web_and_local_links.extend(pl.download_resource(script_tags, params))

    localized_html = pl.change_links(soup_html, web_and_local_links)
    output_path = os.path.join(output, filename)
    with open(output_path, 'w+') as output_file:
        output_file.write(localized_html)
    return output_path

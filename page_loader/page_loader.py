from page_loader import pl
import os


def download(link, output):
    src = pl.get_html_page(link)
    filename = pl.make_file_name(link)
    soup = pl.make_soup(src)
    src_img_tags = pl.get_img_tags(soup)
    web_local_links = pl.download_images(link, src_img_tags, output, filename)
    soup_html = soup.prettify()
    html_localized_img = pl.change_image_links(soup_html, web_local_links)
    output_path = os.path.join(output, filename)
    with open(output_path, 'w+') as output_file:
        output_file.write(html_localized_img)
    return output_path

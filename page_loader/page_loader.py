from page_loader import pl
import os
import logging


def download(url, output):
    src = pl.get_html_page(url)
    logging.info('Download html page successfully.')
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
    logging.info('Downloaded images.')

    link_tags = pl.get_tags(soup, 'link')
    web_and_local_links.extend(pl.download_resource(link_tags, params))
    logging.info('Downloaded link local content.')

    script_tags = pl.get_tags(soup, 'script')
    web_and_local_links.extend(pl.download_resource(script_tags, params))
    logging.info('Downloaded script local content.')
    logging.info('All content are successfully downloaded')

    localized_html = pl.change_links(soup_html, web_and_local_links)
    logging.info('Changed links to local paths.')
    output_path = os.path.join(output, filename)
    with open(output_path, 'w+') as output_file:
        output_file.write(localized_html)
    logging.info('Page is successfully downloaded!')
    return output_path

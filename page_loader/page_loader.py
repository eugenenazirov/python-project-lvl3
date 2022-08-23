from page_loader import pl
import os
import logging
from .progress_bar import bar


def download(url, output):
    if not os.path.exists(output):
        logging.debug(f"Path: {output} doesn't exists!")
        raise FileNotFoundError(f"Path: {output} doesn't exists!")

    src = pl.get_html_page(url)
    logging.debug('Download html page successfully.')
    bar.next()

    filename = pl.make_file_name(url)
    bar.next()
    soup = pl.make_soup(src)
    bar.next()
    soup_html = soup.prettify()
    bar.next()

    params = {
        'src_link': url,
        'output_path': output,
        'name': filename
    }

    web_and_local_links = []

    img_tags = pl.get_tags(soup, 'img')
    web_and_local_links.extend(pl.download_resource(img_tags, params))
    logging.debug('Downloaded images.')
    bar.next()

    link_tags = pl.get_tags(soup, 'link')
    web_and_local_links.extend(pl.download_resource(link_tags, params))
    logging.debug('Downloaded link local content.')
    bar.next()

    script_tags = pl.get_tags(soup, 'script')
    web_and_local_links.extend(pl.download_resource(script_tags, params))
    logging.debug('Downloaded script local content.')
    bar.next()
    logging.debug('All content are successfully downloaded')
    bar.next()

    localized_html = pl.change_links(soup_html, web_and_local_links)
    logging.debug('Changed links to local paths.')
    bar.next()
    output_path = os.path.join(output, filename)
    with open(output_path, 'w+') as output_file:
        output_file.write(localized_html)
    bar.next()
    logging.debug('Page was successfully downloaded!')
    bar.finish()
    return output_path

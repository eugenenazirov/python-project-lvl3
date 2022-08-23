from page_loader import download
from page_loader.pl import eprint
from requests.exceptions import ConnectionError
from urllib.error import HTTPError
import argparse
import os
import logging
import sys


def main():
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        level=logging.INFO,
        stream=sys.stderr)

    pgloader = argparse.ArgumentParser(
        prog='page-loader',
        description='Downloads HTML pages on your machine.')
    pgloader.add_argument('url')
    pgloader.add_argument('-o', '--output', help='path to output html file')
    args = pgloader.parse_args()
    output = args.output

    try:
        if output:
            path_to_page = download(
                args.url,
                output=output)
        else:
            current_dir = os.getcwd()
            path_to_page = download(args.url, output=current_dir)
        print(f'Page was successfully downloaded as {path_to_page}')
        sys.exit(0)
    except (HTTPError, ConnectionError):
        eprint("Error! Check out your url and internet connection.")
        sys.exit(1)
    except FileNotFoundError:
        eprint("Error! Check out the path that you try to download page.")
        sys.exit(1)
    except Exception as exc:
        eprint(f"Unknown Error: {exc} \
Please report it to me: evgenynazirov@yandex.kz")
        sys.exit(1)


if __name__ == '__main__':
    main()

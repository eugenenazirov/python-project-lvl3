from page_loader import download
from page_loader.pl import eprint
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
    except HTTPError:
        eprint("Check out your url and internet connection.")
    except FileNotFoundError:
        eprint("Check out the directory in that you try to download page.")
    except Exception as exc:
        eprint(f"Unknown Error: {exc} \
Please report it to me: evgenynazirov@yandex.kz")
        sys.exit(1)
    finally:
        sys.exit()


if __name__ == '__main__':
    main()

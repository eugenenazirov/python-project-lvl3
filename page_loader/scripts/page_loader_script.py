from page_loader import download
import argparse
import os


def main():
    pgloader = argparse.ArgumentParser(
        prog='page-loader',
        description='Downloads HTML pages on your machine.')
    pgloader.add_argument('url')
    pgloader.add_argument('-o', '--output', help='path to output html file')
    args = pgloader.parse_args()
    output = args.output
    if output:
        path_to_page = download(
            args.url,
            output=output)
    else:
        current_dir = os.getcwd()
        path_to_page = download(args.url, output=current_dir)
    print(path_to_page)


if __name__ == '__main__':
    main()

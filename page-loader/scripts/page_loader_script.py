from page_loader import page_loader
import argparse
import os


def main():
    pgloader = argparse.ArgumentParser(prog='page-loader', description='Downloads\
        HTML pages on your machine.')
    pgloader.add_argument('url')
    pgloader.add_argument('-o', '--output', help='path to output html file')
    args = pgloader.parse_args()
    output = args.output
    if output:
        path_to_page = page_loader(
            args.first_file,
            output=output)
    else:
        current_dir = os.getcwd()
        path_to_page = page_loader(args.first_file, args.second_file,
        output = current_dir)
    print(path_to_page)


if __name__ == '__main__':
    main()

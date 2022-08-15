import requests


# tmp_dir = tempfile.TemporaryDirectory()

# tmp_name = tmp_dir.name
# print(type(tmp_name))

# path = Path(tmp_name, 'hexlet.html')
# print(path)

def make_file_name(link: str):
    if link.startswith('https://') or link.startswith('http://'):
        parse_link = link.split('/')
        parse_link.remove('https:')
        parse_link.remove('')
        parse_link_to_str = '-'.join(parse_link)
        spec_sym_to_dash = ''
        for char in parse_link_to_str:
            if not char.isalnum():
                spec_sym_to_dash += '-'
            else:
                spec_sym_to_dash += char
        result = spec_sym_to_dash + '.html'
        return result


def download(link, output):
    src = requests.get(link).text
    filename = make_file_name(link)
    # with open(path):
    #     pass
    return filename

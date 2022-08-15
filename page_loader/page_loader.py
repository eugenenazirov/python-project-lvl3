import requests


# tmp_dir = tempfile.TemporaryDirectory()

# tmp_name = tmp_dir.name
# print(type(tmp_name))

# path = Path(tmp_name, 'hexlet.html')
# print(path)
def make_file_name(link):
    if link.



def download(link, path):
    src = requests(link).text
    filename = make_file_name(link)
    with open()

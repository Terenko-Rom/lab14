import http.client
from urllib.parse import urlparse
from html.parser import HTMLParser
class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return ''.join(self.text)
def download_text_from_url(url, file_name):
    try:
        parsed_url = urlparse(url)
        connection = http.client.HTTPSConnection(parsed_url.netloc)
        connection.request("GET", parsed_url.path or "/")
        response = connection.getresponse()
        if response.status == 200:
            html = response.read().decode("utf-8")
            parser = TextExtractor()
            parser.feed(html)
            text = parser.get_text()
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(text)
        else:
            print(f"Помилка доступу до {url}: статус {response.status}")
    except Exception as e:
        print(f"Не вдалося завантажити текст з {url}: {e}")
def main():
    with open("webpages.txt", "r", encoding="utf-8") as file:
        urls = file.readlines()
    for index, url in enumerate(urls):
        url = url.strip()
        text_file_name = f"{index}.txt"
        download_text_from_url(url, text_file_name)

if __name__ == "__main__":
    main()
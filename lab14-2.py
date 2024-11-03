import http.client
import os
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
class ImageExtractor(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.images = []
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            if 'src' in attrs_dict:
                img_url = urljoin(self.base_url, attrs_dict['src'])
                self.images.append(img_url)
    def get_images(self):
        return self.images
def download_images_from_url(url, folder_name):
    try:
        parsed_url = urlparse(url)
        connection = http.client.HTTPSConnection(parsed_url.netloc)
        connection.request("GET", parsed_url.path or "/")
        response = connection.getresponse()
        
        if response.status == 200:
            html = response.read().decode("utf-8")
            parser = ImageExtractor(url)
            parser.feed(html)
            images = parser.get_images()
            
            for i, img_url in enumerate(images):
                try:
                    img_parsed_url = urlparse(img_url)
                    img_connection = http.client.HTTPSConnection(img_parsed_url.netloc)
                    img_connection.request("GET", img_parsed_url.path)
                    img_response = img_connection.getresponse()
                    
                    if img_response.status == 200:
                        img_data = img_response.read()
                        img_name = os.path.join(folder_name, f"{i}.jpg")
                        with open(img_name, "wb") as img_file:
                            img_file.write(img_data)
                    else:
                        print(f"Помилка завантаження зображення {img_url}: статус {img_response.status}")
                except Exception as e:
                    print(f"Не вдалося завантажити зображення {img_url}: {e}")
        else:
            print(f"Помилка доступу до {url}: статус {response.status}")
    except Exception as e:
        print(f"Не вдалося завантажити зображення з {url}: {e}")
def main():
    os.makedirs("images", exist_ok=True)
    with open("webpages.txt", "r", encoding="utf-8") as file:
        urls = file.readlines()
    for url in urls:
        url = url.strip()
        download_images_from_url(url, "images")
if __name__ == "__main__":
    main()
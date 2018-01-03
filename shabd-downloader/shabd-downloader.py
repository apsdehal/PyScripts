import requests as r
from bs4 import BeautifulSoup as BS
from tqdm import tqdm
import sys
import os

MAIN_URL = "http://djpunjabz.com/view-shabad-gurbani.html"


def main(url):
    res = r.get(url)
    soup = BS(res.content, "lxml")

    anchors = soup.find_all("a")

    for anchor in anchors:
        if 'title' in anchor.attrs:
            get_album(anchor.attrs['href'])

    res.close()


def get_album(url):
    res = r.get(url)
    soup = BS(res.content, "lxml")

    djs = soup.find_all("p", "dj")

    for dj in djs:
        anchor = dj.find("a")
        if 'title' in anchor.attrs:
            get_song(anchor.attrs['title'], anchor.attrs['href'])

    res.close()


def get_song(album_title, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    res = r.get(url, headers=headers)
    soup = BS(res.content, "lxml")
    title = "_".join(list(map(lambda x: x.capitalize(),
                              url.split("/")[-1][:-5].split("-")))) \
            + ".mp3"
    audio_src = soup.find("audio").find("source").attrs['src']

    res = r.get(audio_src, stream=True)

    album_title = "_".join(album_title.split(" "))
    if not os.path.exists(album_title):
        os.makedirs(album_title)
    title = os.path.join(album_title, title)

    print("[+] Downloading ", title, " from ", audio_src)
    total_size = int(res.headers.get('content-length', 0))

    if not os.path.exists(title):
        with open(title, "wb+") as f:
            for data in tqdm(res.iter_content(chunk_size=1024 * 1024), total=total_size, unit='B',
                             unit_scale=True):
                # if data:
                f.write(data)
    res.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main(MAIN_URL)

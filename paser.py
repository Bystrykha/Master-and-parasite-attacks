#!/usr/bin/env python3
from bs4 import BeautifulSoup
from requests import get
from time import sleep
from wget import download


def get_image_url(link):
    while True:
        resp2 = get(link)
        resp_text2 = resp2.text
        soup2 = BeautifulSoup(resp_text2, features="lxml")
        showcase2 = str(soup2.find_all('a', class_="JS-Popup"))
        fields = showcase2.split("\"")
        if len(fields) < 3:
            sleep(2)
            continue
        else:
            return fields[3]


def images_download():
    f = open("links.txt", "r")
    counter = 0
    while True:
        link = f.readline()
        if not link:
            break
        else:
            sleep(6)
            download(link, f"C:/Users/Asus/go/ImageServer/images/image{counter}")
            counter += 1
    return counter


if __name__ == "__main__":
    links = []
    dom = "https://wallpaperscraft.ru"
    page = "/all/3415x3415/page"
    for i in range(2, 600):
        resp = get(dom + page + str(i))
        resp_text = resp.text
        soup = BeautifulSoup(resp_text, features="lxml")
        showcase = soup.find_all('a', class_="wallpapers__link")
        for j in showcase:
            a = str(j)
            url2 = dom + (a.split("\"")[3])
            a = get_image_url(url2)
    print(images_download())

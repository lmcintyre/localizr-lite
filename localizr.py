from bs4 import BeautifulSoup
from pathlib import Path
from urllib import parse
import os


def main():

    parent = Path(__file__).resolve().parent

    for file in os.listdir(parent):

        if not file.endswith(".html"):
            continue

        with open(file) as fp:
            soup = BeautifulSoup(fp, "lxml")

        for i, tag in enumerate(soup.find_all("img")):
            img = tag["src"]
            if parse.urlparse(img)[1]:
                print(f"has netloc: {img}")

            # tag["src"] = f"img{i}.png"
            # print(tag["src"])

        # for tag in soup.find_all("img"):
        #     print(tag)


if __name__ == "__main__":
    main()

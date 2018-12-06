from bs4 import BeautifulSoup
from pathlib import Path
from urllib import parse
import os


def main():

    print("Fixing paths, please wait")
    parent = Path(__file__).resolve().parent.joinpath("html")

    for i, file in enumerate(os.listdir(parent)):
        if not file.endswith(".html"):
            continue

        realfile = parent.joinpath(file)

        with open(realfile, encoding="utf8") as fp:
            soup = BeautifulSoup(fp, "lxml")

        for tag in soup.find_all("img"):
            img = tag["src"]
            if parse.urlparse(img)[1]:
                newimg = os.path.splitext(file)[0] + os.path.splitext(parse.urlparse(img)[2])[1]
                mediapath = os.path.join(os.path.dirname("..\\"), "media")
                imgmediapath = os.path.join(mediapath, newimg)

                # check existence at 3 because relative wouldn't work here, but we need it in html
                if os.path.exists(imgmediapath[3:]):
                    tag["src"] = imgmediapath
                    with open(realfile, "w", encoding="utf8") as fp:
                        fp.write(str(soup.prettify()))


if __name__ == "__main__":
    main()

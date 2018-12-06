from bs4 import BeautifulSoup
from pathlib import Path
from urllib import parse
from urllib import request
from urllib import error
import shutil
import os


def download(file, root, path):
    try:
        with open(os.path.join(root, path), "w+b") as img, request.urlopen(file) as response:
            print(f"Writing to: {os.path.join(root.parent, path)} from {file}")
            shutil.copyfileobj(response, img)
    except error.HTTPError:
        print(f"Failed to download from {file}")


def localize(file, root):
    realfile = root.joinpath(file)

    with open(realfile, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, "lxml")

    imgs = soup.find_all("img")
    multi = len(imgs) > 1

    for i, tag in enumerate(imgs):
        img = tag["src"]
        if parse.urlparse(img)[1]:
            media = os.path.join(os.path.dirname("..\\"), "media")
            begin = os.path.splitext(file)[0].strip()
            end = os.path.splitext(parse.urlparse(img)[2])[1].strip()

            if multi:
                newimg = begin + f"_{i}" + end
            else:
                newimg = begin + end

            imgmediapath = os.path.join(media, newimg)

            # check existence at 3 because relative wouldn't work here, but we need it in html
            # first check our best guess (multis seem to always have a suffix
            # if our best guess didn't work we attempt to add _0 to it because idk
            # if THAT doesn't work, we download the file under the original expected filename
            if not os.path.exists(imgmediapath[3:]):
                origmediapath = imgmediapath
                imgmediapath = os.path.join(media, begin + "_0" + end)
                if not os.path.exists(imgmediapath[3:]) and i < 1:
                    print(f"Could not find images for {begin}, downloading...")
                    download(img, root, origmediapath)
                    if not os.path.exists(origmediapath[3:]):
                        print("i have failed you")
                    imgmediapath = origmediapath

            tag["src"] = imgmediapath
            with open(realfile, "w", encoding="utf8") as fp:
                fp.write(str(soup.prettify()))


def main():
    print("Fixing paths, please wait")
    parent = Path(__file__).resolve().parent.joinpath("html")

    for file in os.listdir(parent):
        if not file.endswith(".html"):
            continue
        localize(file, parent)


if __name__ == "__main__":
    main()

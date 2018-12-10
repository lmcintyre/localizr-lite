from bs4 import BeautifulSoup
from pathlib import Path
from urllib import parse
from urllib import request
from urllib import error
import shutil
import os


# def download(file, root, path):
    # try:
    #     with open(os.path.join(root, path), "w+b") as img, request.urlopen(file) as response:
    #         print(f"Writing to: {os.path.join(root.parent, path)} from {file}")
    #         shutil.copyfileobj(response, img)
    # except error.HTTPError:
    #     print(f"Failed to download from {file}")
    # print("Download disabled for now")


def getpath(file, src, index=-1):
    media = os.path.join(os.path.dirname("..\\"), "media")
    begin = os.path.splitext(file)[0].strip()
    end = os.path.splitext(parse.urlparse(src)[2])[1].strip()

    if index >= 0:
        filepath = begin + f"_{index}" + end
    else:
        filepath = begin + end

    return os.path.join(media, filepath)


def localize(file, root):
    realfile = root.joinpath(file)

    with open(realfile, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, "lxml")

    imgs = soup.find_all("img")
    vids = soup.find_all("embed", attrs={"type": "video/mp4"})
    audio = soup.find_all("embed", attrs={"type": "audio/mpeg"})
    multi = len(imgs) + len(vids) + len(audio) > 1
    tagtotal = 0

    for tag in vids:
        print(f"Video: {tag}")

        vid = "".join(tag["src"].split(" "))
        if parse.urlparse(vid)[1]:
            savepath = getpath(file, vid)
            spex = os.path.exists(savepath[3:])
            if spex:
                print(f"{savepath} exists: {spex}")

    for tag in audio:
        print(f"Audio: {tag}")

        aud = "".join(tag["src"].split(" "))
        if parse.urlparse(aud)[1]:
            savepath = getpath(file, aud)
            #TODO handle as according to cases when audio is not downloaded
        else:
            tag["src"] = aud
            if os.path.exists(aud[3:]):
                print(f"{aud} exists: {os.path.exists(aud[3:])}")


    for i, tag in enumerate(imgs):
        print(f"Image: {tag}")

        img = "".join(tag["src"].split(" "))
        if parse.urlparse(img)[1]:
            savepath = getpath(file, img)
            savepathind = getpath(file, img, index=i)
            savepathindcor = getpath(file, img, index=i-1)

            spex = os.path.exists(savepath[3:])
            spindex = os.path.exists(savepathind[3:])
            spindcor = os.path.exists(savepathindcor[3:])

            if spex:
                print(f"{savepath} exists: {spex}")
            elif spindex:
                print(f"{savepathind} exists: {spindex}")
            elif spindcor:
                print(f"{savepathindcor} exists: {spindcor}")


        # img = tag["src"]
        # if parse.urlparse(img)[1]:
        #     media = os.path.join(os.path.dirname("..\\"), "media")
        #     begin = os.path.splitext(file)[0].strip()
        #     end = os.path.splitext(parse.urlparse(img)[2])[1].strip()
        #
        #     if multi:
        #         newimg = begin + f"_{i}" + end
        #     else:
        #         newimg = begin + end
        #
        #     imgmediapath = os.path.join(media, newimg)
        #
        #     # check existence at 3 because relative wouldn't work here, but we need it in html
        #     # first check our best guess (multis seem to always have a suffix
        #     # if our best guess didn't work we attempt to add _0 to it because idk
        #     # if THAT doesn't work, we download the file under the original expected filename
        #     if not os.path.exists(imgmediapath[3:]):
        #         origmediapath = imgmediapath
        #         imgmediapath = os.path.join(media, begin + "_0" + end)
        #         if not os.path.exists(imgmediapath[3:]) and i < 1:
        #             print(f"Could not find images for {begin}, downloading...")
        #             download(img, root, origmediapath)
        #             if not os.path.exists(origmediapath[3:]):
        #                 print("i have failed you")
        #             imgmediapath = origmediapath

            # tag["src"] = imgmediapath

    # with open(realfile, "w", encoding="utf8") as fp:
    #     fp.write(str(soup.prettify()))


def main():
    print("Fixing paths, please wait")
    parent = Path(__file__).resolve().parent.joinpath("html")

    for file in os.listdir(parent):
        if not file.endswith(".html"):
            continue
        localize(file, parent)


if __name__ == "__main__":
    main()

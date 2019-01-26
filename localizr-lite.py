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
    print(f"File: {file}:")
    realfile = root.joinpath(file)

    with open(realfile, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, "lxml")

    imgs = soup.find_all("img")
    vids = soup.find_all("embed", attrs={"type": "video/mp4"})
    audio = soup.find_all("embed", attrs={"type": "audio/mpeg"})
    multi = (len(imgs) + len(vids) + len(audio)) > 1
    tagtotal = 0
    imgtotal = 0

    for tag in vids:
        # print(f"\tVideo: {tag}")

        vid = "".join(tag["src"].split(" "))

        savepath = vid

        if not os.path.splitext(vid)[1]:
            loc = len(vid) - 3
            savepath = vid[:loc] + "." + vid[loc:]

        if parse.urlparse(vid)[1]:
            # print(parse.urlparse(vid)[1])
            savepath = getpath(file, vid)

        if savepath:
            # print(f"\tvid savepath: {savepath}")
            spexmov = os.path.exists(savepath[3:] + ".mov")
            spexmp4 = os.path.exists(savepath[3:] + ".mp4")
            if spexmov:
                savepath = savepath + ".mov"
            elif spexmp4:
                savepath = savepath + ".mp4"

        print(f"\t{savepath} exists: {os.path.exists(savepath[3:])}")

    for tag in audio:
        # print(f"\tAudio: {tag}")

        aud = "".join(tag["src"].split(" "))
        savepath = aud

        if parse.urlparse(aud)[1]:
            savepath = getpath(file, aud)
            # TODO handle as according to cases when audio is not downloaded
        else:
            tag["src"] = aud

        spex = os.path.exists(savepath[3:])
        print(f"\t{aud} exists: {spex}")

    for i, tag in enumerate(imgs):
        # print(f"\tImage: {tag} | {i}")

        img = "".join(tag["src"].split(" "))
        savepath = img
        tparse = parse.urlparse(img)[1]
        local = "tumblr" in tparse
        if tparse:
            savepath = getpath(file, img)
            savepathind = getpath(file, img, index=i)
            savepathindcor = getpath(file, img, index=i-1)
            spindex = os.path.exists(savepathind[3:])
            spindcor = os.path.exists(savepathindcor[3:])

        spex = os.path.exists(savepath[3:])

        if local:
            if spex:
                print(f"\t{savepath} exists: {spex}")
                location = spex
            elif spindex:
                print(f"\t{savepathind} exists: {spindex}")
                location = spindex
            elif spindcor:
                print(f"\t{savepathindcor} exists: {spindcor}")
                location = spindcor



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

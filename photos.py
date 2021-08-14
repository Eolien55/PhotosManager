import shutil
import os
import requests
import json
import re
import PIL.Image
import PIL.ExifTags
import hachoir.metadata
import hachoir.parser
from sys import argv


def get_exif(filename):
    try:
        img = PIL.Image.open(filename)
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        return exif
    except:
        return


def lonlat(gps):
    results = []
    for i in ["GPSLongitude", "GPSLatitude"]:
        ref = gps[i + "Ref"]
        val = gps[i]
        val = (val[0] + (val[1] / 60) + (val[2] / 3600)) * (
            1 if ref in ["N", "E"] else -1
        )
        val = eval(str(val))
        results.append(val)
    return results


months = {
    "01": "Janvier",
    "02": "F\u00e9vrier",
    "03": "Mars",
    "04": "Avril",
    "05": "Mai",
    "06": "Juin",
    "07": "Juillet",
    "08": "Ao\u00fbt",
    "09": "Septembre",
    "10": "Octobre",
    "11": "Novembre",
    "12": "D\u00e9cembre",
}

if len(argv) > 1:
    file = argv[1]
else:
    file = "."

for folder, _, files in os.walk(file):
    folder = os.path.abspath(folder)
    print(folder)
    for file in files:
        try:
            format = re.findall(r"\.[A-Za-z0-9_]+$", file)[0]
        except:
            continue
        file = folder + "/" + file
        if format not in [".mov", ".MOV"]:
            exif = get_exif(file)
            if exif is None:
                continue
            if "DateTime" not in exif:
                continue
            DateTime = exif["DateTime"]
            year = DateTime[:4]
            month = months[DateTime[5:7]]
            if "GPSInfo" in exif:
                gps = {
                    PIL.ExifTags.GPSTAGS.get(i): exif["GPSInfo"][i]
                    for i in exif["GPSInfo"]
                }
                lon, lat = lonlat(gps)
                params = {
                    "lon": str(lon),
                    "lat": str(lat),
                    "zoom": 10,
                    "format": "jsonv2",
                    "accept-language": "fr",
                }
                while 1:
                    try:
                        adress = requests.get(
                            "https://nominatim.openstreetmap.org/reverse", params=params
                        ).text
                        break
                    except:
                        print("retry")

                adress = json.loads(adress).get("display_name")
                if adress:
                    adress = adress.split(", ")
                    city = adress[0]
                    country = adress[-1]
                else:
                    city = None
                    country = None
            else:
                city = None
                country = None
        else:
            try:
                parser = hachoir.parser.createParser(file)
                with parser:
                    metadata = hachoir.metadata.extractMetadata(parser)
                    metadata
                    metadata = metadata.exportDictionary(human=False)
                DateTime = metadata["Metadata"]["creation_date"]
                year = DateTime[:4]
                month = months[DateTime[5:7]]
                city, country = None, None
            except:
                continue

        if city and country:
            if not os.path.exists(
                os.path.abspath(".") + f"/{country}/{city}/{year}/{month}"
            ):
                os.makedirs(os.path.abspath(".") + f"/{country}/{city}/{year}/{month}")
            name = (
                str(
                    len(
                        os.listdir(
                            os.path.abspath(".") + f"/{country}/{city}/{year}/{month}"
                        )
                    )
                    + 1
                )
                + format
            )
            newfile = os.path.abspath(".") + f"/{country}/{city}/{year}/{month}/{name}"
        else:
            if not os.path.exists(os.path.abspath(".") + f"/{year}/{month}"):
                os.makedirs(os.path.abspath(".") + f"/{year}/{month}")
            name = (
                str(len(os.listdir(os.path.abspath(".") + f"/{year}/{month}")) + 1)
                + format
            )
            newfile = os.path.abspath(".") + f"/{year}/{month}/{name}"
        shutil.move(file, newfile)

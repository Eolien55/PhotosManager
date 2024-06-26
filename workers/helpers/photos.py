import shutil
import os
from time import sleep, time
from types import FunctionType
import requests
import json
import re
import hachoir.metadata
import hachoir.parser


def lonlat(gps):
    if not tuple(filter(lambda x: "GPS" in x, gps)):
        return "Ville inconnue", "Pays inconnu"
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

authorized_formats = ("GIF", "JPG", "JPEG", "PNG", "TIFF", "MOV", "MP4")


def lonlat_to_city_country(lon, lat):
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
                "https://nominatim.openstreetmap.org/reverse",
                params=params,
            ).text
            break
        except:
            pass

    adress = json.loads(adress).get("display_name")
    if adress:
        adress = adress.split(", ")
        city = adress[0]
        country = adress[-1]
    else:
        city = "Ville inconnue"
        country = "Pays inconnu"

    return city, country


def exif_to_city_country(exif: dict):
    gps_exif = {k.split(":")[-1]: v for k, v in exif.items() if "EXIF:" in k}
    try:
        lon, lat = lonlat(gps_exif)
        city, country = lonlat_to_city_country(lon, lat)
    except Exception as e:

        city, country = "Ville inconnue", "Pay inconnu"

    return city, country


def photo_employee_job(root, filename: str, get_exif: FunctionType, process_id, lock):
    format = filename.split(".")[-1]
    if format.upper() not in authorized_formats:
        return
    exif = get_exif(filename)
    with hachoir.parser.createParser(filename) as parser:
        metadata = hachoir.metadata.extractMetadata(parser)
        metadata = metadata.exportDictionary(human=False)
    DateTime = metadata["Metadata"]["creation_date"]
    year = DateTime[:4]
    month = months[DateTime[5:7]]
    lock.acquire()
    started = time()
    if exif and bool(filter(lambda x: "GPS" in x.upper(), exif)):
        city, country = exif_to_city_country(exif)
    else:
        city, country = "Ville inconnue", "Pays inconnu"

    sleep(1.5 - (started - time()))
    lock.release()

    if not os.path.exists(
        os.path.join(
            root,
            country,
            city,
            year,
            month,
        )
    ):
        os.makedirs(
            os.path.join(
                root,
                country,
                city,
                year,
                month,
            )
        )

    shutil.move(
        filename,
        os.path.join(
            root,
            country,
            city,
            year,
            month,
            """{}-{}{}{}""".format(
                DateTime[:10],
                len(
                    list(
                        map(
                            lambda file: re.match(
                                r"^{}-[0-9]+\..+$".format(DateTime[:10]), file
                            ),
                            os.listdir(
                                os.path.join(root, country, city, year, month),
                            ),
                        )
                    )
                ),
                " (" + str(process_id) + ")",
                "." + format,
            ),
        ),
    )

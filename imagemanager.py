from PIL import Image
from datetime import datetime
import locale

def resize_image(filepath):
    try:
        image = Image.open(filepath)
        width = image.size[0]
        height = image.size[1]
        landscape = True if width > height else False
        minwidth = 1819 if landscape else 1311
        minheight = 1311 if landscape else 1819
        ratioWE = width / height
        ratioEW = height / width
        if width < minwidth or height < minheight:
            print("Image too small, resizing it")
            newwidth = 0
            newheight = 0
            if width < minwidth:
                newwidth = minwidth
                newheight = minwidth * ratioEW
            if newheight < minheight:
                newheight = minheight
                newwidth = minheight * ratioWE

            image_resized = image.resize((int(newwidth), int(newheight)))
            image.close()
            image_resized.save(filepath)
            image_resized.close()
    except Exception as e:
        print("Error while resizing the image : " + str(e))

def get_datetime_taken(filepath):
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    image = Image.open(filepath)
    exif = image.getexif()

    if exif and exif[306]:
        return datetime.strptime(exif[306], "%Y:%m:%d %H:%M:%S").strftime('%A %d/%m/%Y %H:%M:%S')

    return None
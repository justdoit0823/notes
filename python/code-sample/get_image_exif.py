
import PIL.ExifTags
from PIL import Image
import sys


exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGS
}


def get_exif(im):
    return {
        PIL.ExifTags.TAGS[k]: v
        for k, v in im._getexif().items()
        if k in PIL.ExifTags.TAGS
}

def main():
    f = sys.argv[1]
    im1 = Image.open(f)
    print(get_exif(im1))


if __name__ == '__main__':
    main()

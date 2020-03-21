import os
from collections import namedtuple
from pathlib import Path
import string
import random

from PIL import Image
from PIL.ImageFile import ImageFile

from werkzeug.utils import secure_filename

from configuration import SoccerConfig

Chunk = namedtuple("Chunk", "path url")
STORAGE_PATH = Path(SoccerConfig.STORAGE_PATH)


def url(filename, subdir: str) -> str:
    """Get url file

    Args:
        filename: filename
        subdir: subdirectory

    Returns:
        str url
    """
    if not filename:
        return ""

    static_url = SoccerConfig.STATIC_URL
    if subdir:
        static_url = static_url + "/" + subdir
    
    return static_url + "/" + filename


def path(filename: str, subdir: str) -> Path:
    """Get full file path

    Args:
        filename: filename
        subdir: subdirectory

    Returns:
        str full path
    """
    upload_dir = Path(SoccerConfig.STORAGE_PATH)
    if subdir:
        upload_dir = upload_dir / subdir

    return upload_dir / filename


def save(file, subdir: str, filename=None, close_after=True) -> str:
    """Save file

    Args:
        file: save able file ex: (FileStorage, ImageFile)
        subdir: sub directory
        filename: filename of file
        close_after: close file after done ?

    Returns:
        str filename
    """
    upload_dir = Path(SoccerConfig.STORAGE_PATH)
    if subdir:
        upload_dir = upload_dir / subdir

    # make sure upload directory exists
    if not upload_dir.is_dir():
        upload_dir.mkdir(parents=True)

    if not filename:
        filename = file.filename

    # make sure filename is safe and no collision
    filename = safe_filename(filename)
    while (upload_dir / filename).is_file():
        filename = safe_filename(file.filename)

    if isinstance(file, ImageFile):
        if file.mode in ('RGBA', 'LA', '1', 'P'):
            file = file.convert("RGB")

        size = (1312, 984) # untuk membatasi ukuran image yang di upload
        if file.size[0] > size[0] or file.size[1] > size[1]:
            file.thumbnail(size, Image.ANTIALIAS)
            file.save(str(upload_dir / filename), quality=90)
        else:
            file.save(str(upload_dir / filename), quality=90)
    else:
        file.save(str(upload_dir / filename))

    if close_after:
        file.close()

    return filename


def safe_filename(filename, maxchar=40):
    """Secure filename and add random string

    Args:
        filename: filename
        maxchar: maximum character

    Example Result:
    [nama_file]_randomgstring - inifilecermin_awkwards.jpg
    """
    name, ext = os.path.splitext(filename)

    random_str = '_' + ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(10)
    )

    name_max = maxchar - len(ext) - len(random_str)
    if len(name) > name_max:
        name = name[:name_max]

    name = "%s%s%s" % (name, random_str, ext)

    return secure_filename(name)
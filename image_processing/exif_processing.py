import logging

from PIL import Image
from PIL.ExifTags import TAGS

from model.image_exif_info import ImageExifInfo, ExifDataKey
from model.image_meta_info import ImageMetaInfo


def extract_exif_info_from_image(image: Image, meta_info: ImageMetaInfo = None) -> ImageExifInfo:
    """
    Method extracts exif data from image.
    :param image: image to extract exif data
    :param meta_info: if exif data is not provided in image information must be given in meta
    :return: exif information
    """

    # Extracting the exif metadata
    exif_data = image.getexif()

    # Creating image exif data dictionary
    exif_data_dict = {}

    # Looping through all the tags present in exif data
    for tag_key, tag_value in exif_data.items():
        # Getting the tag name instead of tag id
        tag_name = TAGS.get(tag_key, tag_key)

        # Adding new entry to the dictionary
        exif_data_dict[tag_name] = tag_value

    if ExifDataKey.GPS_INFO in exif_data_dict and ExifDataKey.GPS_INFO in exif_data_dict:
        return ImageExifInfo.from_exif_data(exif_data_dict)
    else:
        logging.warning("DateTime and GPSInfo not provided in image exif data. Trying to use meta data")
        if meta_info is not None:
            return ImageExifInfo.from_meta_info(meta_info)
        else:
            raise Exception("DateTime and GPSInfo not provided in image meta and exif data")

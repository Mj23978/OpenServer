import base64
from PIL import Image
import io


def base64_to_image(base64_string, output_path):
    """
    This function converts a base64 string to an image.
    """
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    image.save(output_path)


def image_to_base64(image_path):
    """
    This function converts an image to a base64 string.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


def read_image(image_path):
    try:
        img = Image.open(image_path)
        return img
    except IOError:
        print("Unable to load image")
        return None

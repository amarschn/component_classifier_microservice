"""
Functions generate images from a step file.

Author: Drew
"""

import cadquery as cq
import re
from wand.image import Image
from wand.color import Color
import os
import requests


VIEWS = {'x': (1, 0, 0),
         '-x': (-1, 0, 0),
         'y': (0, 1, 0),
         '-y': (0, -1, 0),
         'z': (0, 0, 1),
         '-z': (0, 0, -1)}

URL = "http://component_classifier_ai_1:5000/api/classify_image/"


def create_images(connector_file, folder='ortho_views'):
    """Generate images from STEP file."""
    if not os.path.exists(folder):
        os.mkdir(folder)
    connector = cq.importers.importStep(connector_file).combine()

    image_filenames = []

    for view_name in VIEWS:
        v = VIEWS[view_name]
        svg = connector.toSvg(view_vector=v)
        svg = process_svg(svg)
        img_name = os.path.join(folder, connector_file.split(".")[0] + "_" + view_name + '.png')
        image_filenames.append(img_name)
        svg_blob = svg.encode('utf-8')
        with Image(blob=svg_blob, format='svg') as img:
            img.format = "png"
            img.trim()
            img.transform(resize='200x200')
            # TODO: figure out a better way to add a border resulting in a 200x200 image
            width, height = img.size
            height_border = (200 - height)/2
            width_border = (200 - width)/2
            img.border(Color('#FFFFFF'), width_border, height_border)
            img.sample(200, 200)

            img.save(filename=img_name)

    # Return the list of filenames
    return image_filenames


def process_svg(svg):
    """Hacky way to remove hidden lines from cadquery exports - 
    better way would be to modify cq source"""

    # TODO: remove the entire hidden line group with some regex magic
    new_svg = re.sub('(160, 160, 160)', '255, 255, 255', svg, re.DOTALL)
    return new_svg


def get_image_class(image_file):
    """Get classification of image file"""
    files = {'image': open(image_file, 'rb')}
    payload = {'filename': 'hello.png'}
    r = requests.post(URL, files=files, data=payload)
    return r.text


def classify_images(image_files):
    """Classify a list of image files"""
    classifications = {}

    for image in image_files:
        classification = get_image_class(image)
        classifications[image] = classification
    return classifications

def classify_step(step_file):
    """Creates images of a step file and classifies them"""
    image_files = create_images(step_file)
    return classify_images(image_files)


if __name__ == '__main__':
    # create_images('USB_Micro-B_Molex_47346-0001.step')
    create_images('Conn_HIROSE_ZX62WD1-B-5PC_eec.STEP')
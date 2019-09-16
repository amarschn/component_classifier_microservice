from PIL import Image as I
from PIL import ImageDraw as D
import glob

def classification_image():
    image_files = glob.glob('./*.png')
    # image_files = create_images(step_file)
    # classifications = classify_images(image_files)
    new_img = I.new('RGB', (1200, 200))
    x_offset = 0
    border = I.new('RGB', (200,200))

    for i,im in enumerate(image_files):
        img = I.open(im)
        if i==1:
            draw = D.Draw(img)
            draw.rectangle((0,0,200,10), fill=(255,0,0))
            
        new_img.paste(img, (x_offset, 0))
        x_offset += 200
    new_img.save('classification.png')
    return 'classification.png'

if __name__ == '__main__':
    classification_image()
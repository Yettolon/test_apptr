from datetime import datetime
from os.path import splitext
from PIL import Image


from sit.settings import IMAGE_FOR_AVA

def timestapppp(instance, filename):
    
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])

class Waters:
    def process(self, image):
        img = Image.new("RGBA", image.size)
        watermark = Image.open(IMAGE_FOR_AVA)
        img.paste(watermark, (0,0))
        new_img = Image.new("RGBA", image.size)
        new_img = Image.alpha_composite(new_img, image)
        new_img = Image.alpha_composite(new_img, img)
        
        return new_img
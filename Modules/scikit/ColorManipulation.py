
from skimage.color import rgb2gray

def convertRGB2Gray(img):
    return (rgb2gray(img) * 255).astype('uint8')



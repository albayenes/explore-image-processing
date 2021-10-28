
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

def convertRGB2Gray(img):
    plt.imshow(rgb2gray(img), cmap="gray")
    print(rgb2gray(img).dtype)
    plt.show()
    return (rgb2gray(img) * 255).astype('uint8')



import PIL
from PIL import Image

#from JSONextractor import *
import JSONextractor

path = r'''C:\Users\User\Desktop\Mask_RCNN-master\samples\dances''' ##TODO: path to your working folder
jsonName = "ballet.json"                ##TODO: your json file name

paths = [path + "/" + jsonName,
         path,
         path + "/" + "pngImages",
         path + "/" + "bmpImages",
         path + "/" + "normalImages"]


test = JSONextractor(paths)
test.extraction()
test.testing()

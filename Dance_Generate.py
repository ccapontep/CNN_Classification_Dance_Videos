import json
import urllib.request
import os

import skimage.draw
import skimage.io

import numpy as np
import scipy.misc
from PIL import Image, ImageDraw, ImageFont


json_output_filename = "dataset.json"
dataset_labelbox_path = "dataset/labelbox/"

activities = ["BreakDancing", "Cheer", "Tango", "Ballet", "BatonTwirling", "BellyDancing"]


dataset_path = "dataset/trainval/"
dataset = {}

# Create dataset directory if it doesn't exist:
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

if not os.path.exists(dataset_path + "images/"):
    os.makedirs(dataset_path + "images/")

if not os.path.exists(dataset_path + "masks/"):
    os.makedirs(dataset_path + "masks/")


# Read all json files taken from LabelBox:
for activity in activities:
    json_path = dataset_labelbox_path + activity + ".json"
    print("Reading", json_path)
    skipped = 0
    # Open json file:
    with open(json_path) as json_file:
        json_data = json.load(json_file)

    # Extract data from json file:
    for idx, elem in enumerate(json_data):
        if elem["Label"] == "Skip":
            continue

        masks_dict = {}

        # Download image:
        img_url = elem["Labeled Data"]
        img_path = dataset_path + "images/" + activity + "_" + str(idx) + ".png"
        if not os.path.isfile(img_path):
            try:
                urllib.request.urlretrieve(img_url, img_path)
            except TimeoutError:
                print("TimeoutError")
                continue
        
        image = skimage.io.imread(img_path)
        # print(img_url)
        # print(img_path)
        # print(image.shape)

        h, w = image.shape[:2]

	    #image = Image.open(img_path)
		# w, h = im.size

        # Create masks from the polygons:
        mask_idx = 0
        for mask_class, mask_class_coordinates in elem["Label"].items():

            for poly_coord in mask_class_coordinates:
                #print("poly_coord:", poly_coord)

                # print(poly_coord)
                x = [int(coord["x"]) for coord in poly_coord]
                y = [int(coord["y"]) for coord in poly_coord]

                polygon = [{'all_points_y': y, 'name': 'polygon', 'all_points_x': x}]

                mask_path = dataset_path + "masks/" + activity + "_" + str(idx) + "_" + str(mask_idx) + ".png"

                if not os.path.isfile(mask_path):
                    rr, cc = skimage.draw.polygon(y, x, shape=(h, w))
                    mask = np.zeros([h, w])
                    mask[rr, cc] = 1
                    mask = np.flipud(mask)
                    scipy.misc.imsave(mask_path, mask)

                masks_dict[mask_path] = {"class": mask_class, "polygon": polygon}
                mask_idx = mask_idx + 1

        if masks_dict != {}:
            dataset[img_path] = masks_dict

    print("Total skipped images for " + json_path + ": " + str(skipped))

# Write dictionary onto a JSON file:
with open(dataset_path + json_output_filename, "w") as fp:
    json.dump(dataset, fp)
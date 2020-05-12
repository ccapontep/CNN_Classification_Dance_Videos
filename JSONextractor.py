import json
import urllib.request
import os
import PIL 
from PIL import Image, ImageDraw, ImageFont
import numpy as np
#import opencv

class JSONextractor():

    def __init__(self, paths):

        self.path = paths[0]
        self.directoryPath = paths[1]
        self.pngPath = paths[2]
        self.bmpPath = paths[3]
        self.normalPath = paths[4]
        self.keyDict = {}
        self.numberOfLabels = 0
        self.classes =[]
        self.numObject = []

        self.nomeBase = "image"
        self.labels = []

        os.chdir(self.directoryPath)

        if not os.path.exists(self.pngPath):
            os.makedirs(self.pngPath)

        if not os.path.exists(self.bmpPath):
            os.makedirs(self.bmpPath)

        if not os.path.exists(self.normalPath):
            os.makedirs(self.normalPath)

        b = json.load(open(self.path))
        for xx in range(len(b)):
            name = ''
            if b[xx]['Label'] == "Skip":
                continue
            for x in b[xx]['Label'].keys():
                name = x
                if name not in self.classes:
                    self.classes.append(name)
                    self.numObject.append(1)
                    self.labels.append(0)
                else:
                    self.numObject[self.classes.index(name)] += 1
        self.initStampa(self.classes, self.numObject)

    def initStampa(self, ogg, num):
        print("there are ", len(ogg), " objects.")
        count = 0
        for x in range(len(ogg)):
            print (ogg[x], " appears ", num[x], " times.")
            count += num[x]

        print ("There are ", count, " objects labeled in total.")


    def extraction(self):

        b = json.load(open(self.path))
        self.numberOfLabels = len(b)
        name = ''
        for immNum in range(len(b)):
            #input("Key to continue")
            if b[immNum]['Label'] == "Skip":
                continue
            name = self.nomeBase + str(immNum)
            imm = b[immNum]['Labeled Data']
            os.chdir(self.normalPath)
            #urllib.request.urlretrieve(imm, name + ".png")
            urllib.request.urlretrieve(imm, name)
            self.converti(name)
            nameFile = name
            if "Mask" in b[immNum].keys():
                print("single mask")
                for x in b[immNum]['Label'].keys():
                    name = x
                nameApp = name
                name = self.nomeBase + str(immNum) + name
                imm = b[immNum]['Mask'][nameApp]
                os.chdir(self.pngPath)
                urllib.request.urlretrieve(imm, name + ".png")
                os.chdir(self.bmpPath)
                #self.converti(name)
                #nameFile = name
            else:
                for x in range(len(self.labels)):
                    self.labels[x] = 0
                if len(b[immNum]['Label']) == -1:
                    print("ou")
                    for x in b[immNum]['Label'].keys():
                        print("printo")
                        print(name)
                        name = x
                    print("ciao")
                    nameApp = name
                    print(name)
                    name = self.nomeBase + str(immNum) + name
                    imm = b[immNum]['Masks'][nameApp]
                    os.chdir(self.pngPath)
                    urllib.request.urlretrieve(imm, name + ".png")
                    os.chdir(self.bmpPath)
                else:
                    iter = 0
                    for x in b[immNum]['Label'].keys():
                        try:
                            iter = 0

                            name = x
                            nameObj = x
                            name = self.nomeBase + str(immNum) + name + str(self.labels[self.classes.index(name)])
                            self.labels[self.classes.index(x)] += 1
                            imm = b[immNum]['Masks'][x]
                            os.chdir(self.pngPath)
                            urllib.request.urlretrieve(imm, name + ".png")
                            os.chdir(self.bmpPath)
                            vector = []
                            lim2 = len(b[immNum]['Label'][x])
                            #print("The number of objects "+ str(x)+ " is "+ str(lim2))
                            vector.append([])
                            y = 0
                            for y in range(lim2):
                                vector[iter].append([])
                                lim3 = len(b[immNum]['Label'][x][y])
                                #print("Number of points for the label "+ str(x) + " number "+ str(y) + " is "+ str(lim3))
                                #print(b[immNum]['Label'][x][y])
                                z = 0
                                for z in range(lim3):
                                    w = 0

                                    vector[iter][y].append(b[immNum]['Label'][x][y][z]['x'])
                                    vector[iter][y].append(b[immNum]['Label'][x][y][z]['y'])
                                    #for w in b[immNum]['Label'][x][y][z]:
                                    #    print("sto inserendo ")
                                    #    print(b[immNum]['Label'][x][y][z][w])
                                    #    vector[iter][y].append(b[immNum]['Label'][x][y][z][w])
                            iter += 1
                            im = Image.open(self.pngPath + "/" + nameFile + ".png")
                            #im.show()
                            width, height = im.size
                            #print("e quindi ho un vettore di ")
                            #print(len(vector[0]))
                            #print(vector[0])
                            x = 0
                            for x in range(len(vector[0])):
                                #[0] to eliminate the extra square bracket
                                img_size = (width, height)
                                poly = Image.new('RGB', img_size)
                                poly = poly.transpose(Image.FLIP_TOP_BOTTOM)
                                pdraw = ImageDraw.Draw(poly)
                                pdraw.polygon(vector[0][x],fill=(255, 255, 255, 127), outline=(255, 255, 255, 255))
                                #poly = poly.rotate(180)
                                poly = poly.transpose(Image.FLIP_TOP_BOTTOM)
                                #poly.show()
                                file_out = self.bmpPath + "/" + nameFile + nameObj + str(x) + ".bmp"
                                poly.save(file_out)
                                file_out = self.pngPath + "/" + nameFile + nameObj + str(x) + ".png"
                                poly.save(file_out)
                                #Image.alpha_composite(im, poly).save(self.bmpPath + "/" + nameFile + nameObj + str(y) + "TEST" ".bmp")

                        except:
                            KeyError


    def stampa(self):
        print(self.keyDict)

    def converti(self, name):
        try:
            #path = self.pngPath + "/" + name + ".png"
            path = self.normalPath + "/" + name
            img = Image.open(path)
            file_out = self.bmpPath + "/" + name + ".bmp"
            img.save(file_out)
            file_out_1 = self.pngPath + "/" + name + ".png"
            img.save(file_out_1)
        except:
            OSError
            KeyError

    def testing(self):
        jsonPath = self.path
        b = json.load(open(jsonPath))
        classes = []
        image_ids = []  # riempire con gli id di tutte le immagini non skippate
        for xx in range(len(b)):
            if b[xx]['Label'] == "Skip":
                continue
            else:
                image_ids.append(xx)
            for x in b[xx]['Label'].keys():
                name = x
                if name not in classes:
                    classes.append(name)
        print("classes--> ", classes)
        print("images_ids --> ", image_ids)

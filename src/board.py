import math
import numpy as np
import sys
import cv2
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

class board(object):
    def __init__(self, width, height, bgcolor, verbose=False):
        self.verbose = verbose
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.array = np.ones((height, width)) * bgcolor
        self.components = []
        self.bboxes = []
        self.empty_region = np.where(self.array!=self.bgcolor)
        
    def add_drawing(self, drawing, x_offset, y_offset):
        expected_region = self.array[y_offset:y_offset+drawing.h, x_offset:x_offset+drawing.w]
        if (self.width<x_offset+drawing.array.shape[1]) | (self.height<y_offset+drawing.array.shape[0]):
            if self.verbose:
                print("I'm not allowed to draw outside the board!")
        elif len(np.where(expected_region!=self.bgcolor)[0])!=0:
            if self.verbose:
                print("I'm not allowed to draw on top of an existing drawing!")
        else:
            try:
                if self.bgcolor == 255: #white
                    self.array[y_offset:y_offset+drawing.h, x_offset:x_offset+drawing.w] = np.invert(drawing.array)
                else:
                    self.array[y_offset:y_offset+drawing.h, x_offset:x_offset+drawing.w] = drawing.array
                drawing.x_offset = x_offset
                drawing.y_offset = y_offset
                self.components.append(drawing)
                self.bboxes.append({
                    'label': drawing.label,
                    'xmin': drawing.x_offset,
                    'xmax': drawing.x_offset+drawing.w,
                    'ymin': drawing.y_offset,
                    'ymax': drawing.y_offset+drawing.h 
                })
                self.empty_region = np.where(self.array!=self.bgcolor)
            except Exception as e:
                print("I'm having a trouble drawing", drawing.label, drawing.idx)
                raise

    def save(self, imagepath):
        self.imagepath = imagepath
        cv2.imwrite(self.imagepath, self.array)
    
    def label(self, labelpath):
        try:
            self.imagepath
        except NameError:
            print("Please save the board first!")
        else:
            filepath, file_extension = os.path.splitext(self.imagepath)
            filename = os.path.basename(filepath)
            self.labelpath = labelpath
            with open(self.labelpath, 'w') as f:
                f.write('filename,width,height,class,xmin,ymin,xmax,ymax\n')
                for bbox in self.bboxes:
                    f.write(
                        '%s,%d,%d,%s,%d,%d,%d,%d\n'%(
                            filename,
                            self.width,
                            self.height,
                            bbox['label'],
                            bbox['xmin'],
                            bbox['ymin'],
                            bbox['xmax'],
                            bbox['ymax']
                        )
                    )

                    
    def show(self):
        try:
            self.imagepath
        except NameError:
            print("Please save the board first!")
        else:
            try:
                self.labelpath
            except NameError:
                print("Please label the board first!")
            else:
                labels = pd.read_csv(self.labelpath)
                img = cv2.imread(self.imagepath)
                for index, row in labels.iterrows():
                    img = cv2.rectangle(
                        img,
                        (row['xmin'], row['ymin']), (row['xmax'], row['ymax']),
                        (255,0,0), 2
                    )
                    img = cv2.putText(
                        img, row['class'],
                        (row['xmin'], row['ymax']),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0,0,255), 2
                    )
                plt.imshow(img)

    def change_bgcolor(self, probability, new_bgcolor):
        prob = np.random.random()
        if prob<=probability:
            self.array[self.array==self.bgcolor] = new_bgcolor
            self.bgcolor = new_bgcolor
                
    def add_email(self, email, x_offset, y_offset):
        pass

    def add_noise(self):
        pass

    #This is slow!
    def add_perspective(self, probability, m=-0.9):
        prob = np.random.random()
        if prob<=probability:
            img = Image.fromarray(self.array)
            xshift = abs(m) * self.width
            self.width += int(round(xshift))
            self.img = img.transform(
                (self.width, self.height),
                Image.AFFINE,
                (1, m, -xshift if m > 0 else 0, 0, 1, 0),
                Image.BICUBIC
            )
            self.array = np.array(self.img)

    def apply_gradient(self, probability, mode, gradient=1., initial_opacity=1.):
        """
        Applies a black gradient to the image, going from left to right.

        Arguments:
        ---------
        path_in: string
        path to image to apply gradient to
        path_out: string (default 'out.png')
        path to save result to
        gradient: float (default 1.)
        gradient of the gradient; should be non-negative;
        if gradient = 0., the image is black;
        if gradient = 1., the gradient smoothly varies over the full width;
        if gradient > 1., the gradient terminates before the end of the width;
        initial_opacity: float (default 1.)
        scales the initial opacity of the gradient (i.e. on the far left of the image);
        should be between 0. and 1.; values between 0.9-1. give good results
        """
        prob = np.random.random()
        if prob<=probability:
            # get image to operate on
            input_im = Image.fromarray(self.array)
            if input_im.mode != 'RGBA':
                input_im = input_im.convert('RGBA')
            if mode == 'horizontal':
	        # create a gradient that
	        # starts at full opacity * initial_value
	        # decrements opacity by gradient * x / width
                alpha_gradient = Image.new('L', (self.width, 1), color=0xFF)
                for x in range(self.width):
                    a = int((initial_opacity * 255.) * (1. - gradient * float(x)/self.width))
                    if a > 0:
                        alpha_gradient.putpixel((x, 0), a)
                    else:
                        alpha_gradient.putpixel((x, 0), 0)
            elif mode == 'vertical':
	        # create a gradient that
	        # starts at full opacity * initial_value
	        # decrements opacity by gradient * x / height
                alpha_gradient = Image.new('L', (1, self.height), color=0xFF)
                for y in range(self.height):
                    a = int((initial_opacity * 255.) * (1. - gradient * float(y)/self.height))
                    if a > 0:
                        alpha_gradient.putpixel((0, y), a)
                    else:
                        alpha_gradient.putpixel((0, y), 0)

            alpha = alpha_gradient.resize((self.width, self.height))
            # create black image, apply gradient
            black_im = Image.new('RGBA', (self.width, self.height), color=0) # i.e. black
            black_im.putalpha(alpha)
            # make composite with original image
            self.img = Image.alpha_composite(input_im, black_im)
            self.array = np.array(self.img)



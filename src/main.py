"""
usage:

python main.py 42 10 100        

"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as spim
import cv2
import os
import sys
from drawing import *
from board import *

def main(seed, no, size):
    data_path = '../data/'

    # get the drawings
    circles = np.load(os.path.join(data_path, 'circle.npy'))
    envelopes = np.load(os.path.join(data_path, 'envelope.npy'))
    hexagons = np.load(os.path.join(data_path, 'hexagon.npy'))
    lines = np.load(os.path.join(data_path, 'line.npy'))
    octagons = np.load(os.path.join(data_path, 'octagon.npy'))
    squares = np.load(os.path.join(data_path, 'square.npy'))
    zigzags = np.load(os.path.join(data_path, 'zigzag.npy'))
    triangles = np.load(os.path.join(data_path, 'triangle.npy'))

    data = [
        {'dataset': circles, 'label': 'circle'},
        {'dataset': envelopes, 'label': 'envelope'},
        {'dataset': hexagons, 'label': 'hexagon'},
        {'dataset': lines, 'label': 'line'},
        {'dataset': octagons, 'label': 'octagon'},
        {'dataset': squares, 'label': 'square'},
        {'dataset': zigzags, 'label': 'zigzag'},
        {'dataset': triangles, 'label': 'triangle'}
    ]

    drawing_types = np.random.randint(0, len(data), size)
    drawing_indices = [np.random.randint(0, len(data[x]['dataset']), 1)[0] for x in drawing_types]
    
    #initialize a board
    width = 4640
    height = 3480
    bgcolor = 255 #white
    brd = board(width, height, bgcolor)
    
    for (t,i) in zip(drawing_types, drawing_indices):
        dataset = data[t]['dataset']
        label = data[t]['label']
        #print(label, i)
        array = data[t]['dataset'][i]
        dr = drawing(label, i, array)
        dr.rotate(0.8)
        dr.scale(1.0, 10, 3)
        brd.add_drawing(dr, np.random.randint(0, high=width), np.random.randint(0, high=height))

    #change the background color of the board
    brd.change_bgcolor(0.8, np.random.random_integers(200, 255, 1)[0])
    brd.apply_gradient(0.8, mode='horizontal', gradient=np.random.uniform(0, 10), initial_opacity=np.random.random())
    brd.apply_gradient(0.8, mode='vertical', gradient=np.random.uniform(0, 10), initial_opacity=np.random.random())
#    brd.add_perspective(0.5, m=np.random.uniform(-0.1, 0.1)) #Bboxes are not correctly updated for this yet
    plt.figure(figsize=(25,25))
    plt.imshow(brd.array, cmap='gray')
    brd.save('../boards/board{}_{}.jpg'.format(seed, no))
    brd.label('../labels/board{}_{}.csv'.format(seed, no))
    brd.show()

if __name__ == "__main__":
    seed = int(sys.argv[1])
    nos = int(sys.argv[2])
    size = int(sys.argv[3])
    np.random.seed(seed)
    for no in range(nos):
        print(seed, no)
        main(seed, no, size)

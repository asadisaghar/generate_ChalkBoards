"""
usage:

python main.py --seed 42 --no_boards 10 --no_drawings 100 --width 600 --height 300 --scale_min 0.5 --scale_max 1       

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.ndimage as spim
import cv2
import os
import sys
import argparse
from drawing import *
from board import *

def check_path(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def combine_labels(labels_path, all_labels):
    print("Combining all labels into {}".format(os.path.join(labels_path, all_labels)))
    labels = pd.DataFrame()
    for label in os.listdir(labels_path):
        labels = labels.append(pd.read_csv(os.path.join(labels_path, label)))
    labels.to_csv(os.path.join(labels_path, all_labels), index=False)
    
def generate_board(no, args):    
    # get the drawings
    circles = np.load(os.path.join(args.data_path, 'circle.npy'))
    envelopes = np.load(os.path.join(args.data_path, 'envelope.npy'))
    hexagons = np.load(os.path.join(args.data_path, 'hexagon.npy'))
    lines = np.load(os.path.join(args.data_path, 'line.npy'))
    octagons = np.load(os.path.join(args.data_path, 'octagon.npy'))
    squares = np.load(os.path.join(args.data_path, 'square.npy'))
    zigzags = np.load(os.path.join(args.data_path, 'zigzag.npy'))
    triangles = np.load(os.path.join(args.data_path, 'triangle.npy'))

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

    drawing_types = np.random.randint(0, len(data), args.no_drawings)
    drawing_indices = [np.random.randint(0, len(data[x]['dataset']), 1)[0] for x in drawing_types]
    
    #initialize a board
    brd = board(args.width, args.height, args.background)
    
    for (t,i) in zip(drawing_types, drawing_indices):
        dataset = data[t]['dataset']
        label = data[t]['label']
        array = data[t]['dataset'][i]
        dr = drawing(label, i, array)
        dr.rotate(args.rotation_prob)
        dr.scale(args.scale_prob, args.scale_min, args.scale_max)
        brd.add_drawing(dr, np.random.randint(0, high=args.width), np.random.randint(0, high=args.height))

    #change the background color of the board
    brd.change_bgcolor(args.background_change_prob, np.random.random_integers(200, 255, 1)[0])
    brd.apply_gradient(args.horizontal_gradient_prob, mode='horizontal',
                       gradient=np.random.uniform(0, 10), initial_opacity=np.random.random())
    brd.apply_gradient(args.horizontal_vertical_prob, mode='vertical',
                       gradient=np.random.uniform(0, 10), initial_opacity=np.random.random())
#    brd.add_perspective(0.5, m=np.random.uniform(-0.1, 0.1)) #Bboxes are not correctly updated for this yet

    plt.figure(figsize=(25,25))
    plt.imshow(brd.array, cmap='gray')
    brd.save(os.path.join(args.boards_path, 'board{}_{}.jpg'.format(args.seed, no)))
    brd.label(os.path.join(args.labels_path, 'board{}_{}.csv'.format(args.seed, no)))

def main():
    parser = argparse.ArgumentParser()

    # general params
    parser.add_argument('--seed', type=int, default=42, help='random seed used for placing drawings on the board')
    parser.add_argument('--data_path', type=str, default='../data', help='path to the Google drawing data')
    parser.add_argument('--boards_path', type=str, default='../boards', help='path to the generated boards')
    parser.add_argument('--labels_path', type=str, default='../labels', help='path to the labels')
    parser.add_argument('--all_labels', type=str, default='all_labels.csv', help='combined labels filename')

    # board params
    parser.add_argument('--no_boards', type=int, default=10, help='number of random boards to generate')
    parser.add_argument('--height', type=int, default=3480, help='height of generated boards')
    parser.add_argument('--width', type=int, default=4640, help='width of generated boards')
    parser.add_argument('--background', type=int, default=255, help='base background color of generated boards')#white
    parser.add_argument('--background_change_prob', type=float, default=0.8, help='probability of changing background color')
    parser.add_argument('--horizontal_gradient_prob', type=float, default=0.8, help='probability of applying horizontal gradient')
    parser.add_argument('--horizontal_vertical_prob', type=float, default=0.8, help='probability of applying vertical gradient')        
    # drawing params
    parser.add_argument('--no_drawings', type=int, default=100, help='maximum number of drawings on each board')
    parser.add_argument('--rotation_prob', type=float, default=0.8, help='rotation probability')
    parser.add_argument('--scale_prob', type=float, default=1.0, help='scaling probability')
    parser.add_argument('--scale_min', type=float, default=3, help='min scale factor')
    parser.add_argument('--scale_max', type=float, default=10, help='max scale factor')
    
    parser.set_defaults()
    args = parser.parse_args()

    np.random.seed(args.seed)
    check_path(args.boards_path)
    check_path(args.labels_path)
    
    for no in range(args.no_boards):
        print(args.seed, no)
        generate_board(no, args)
    combine_labels(args.labels_path, args.all_labels)
    
if __name__ == "__main__":
    main()

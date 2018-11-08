"""Works for images annotated using BBOX Label Tool"""

import os
from PIL import Image

"""Paramters"""
input_annotation_path = "C:\\Users\\yea\\Desktop\\dataset\\augmented_dataset\\annotations"
images_path = 'C:\\Users\\yea\\Desktop\\dataset\\augmented_dataset\\images'

images_name = os.listdir(images_path)
txt_name = os.listdir(input_annotation_path)
output_annotation_path = "C:\\Users\\yea\\Desktop\\dataset\\augmented_dataset\\result"

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

""" Process """
for i in range(len(images_name)):
    """ Open input text files """
    txt_path = input_annotation_path +"\\" + txt_name[i]
    txt_file = open(txt_path, "r")
    lines = txt_file.read().split('\n')  # for ubuntu, use "\r\n" instead of "\n"

    """ Open output text files """
    txt_outpath = output_annotation_path +"\\"+ txt_name[i]
    txt_outfile = open(txt_outpath, "w")

    """ Convert the data to YOLO format """
    for line in lines:
        if (len(line) >= 2):
            elems = line.split(' ')
            im = Image.open(str(images_path +"\\"+ images_name[i]))
            w = int(im.size[0])
            h = int(im.size[1])
            k = 0
            xmin = elems[0 + k]
            xmax = elems[2 + k]
            ymin = elems[1 + k]
            ymax = elems[3 + k]
            class_id = elems[4 + k]
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert((w, h), b)
            txt_outfile.write(str(class_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    txt_outfile.close()
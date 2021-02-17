from __future__ import print_function
from __future__ import division
import cv2 as cv
import numpy as np
import argparse
import glob
from PIL import Image
from PIL.ExifTags import TAGS
import os
scriptdir = os.path.dirname(os.path.realpath(__file__))

def GetFilesInFolder(path):
    return glob.glob(path, recursive=True)

def loadExposureSeq(files, times):
    images = []
    times = times
    # with open(os.path.join(path, 'list.txt')) as f:
    #     content = f.readlines()
    # for line in content:
    #     tokens = line.split()
    #     images.append(cv.imread(os.path.join(path, tokens[0])))
    #     times.append(1 / float(tokens[1]))
    for file in files:
        print("Processing: " +file)
        images.append(cv.imread(file))
    return images, np.asarray(times, dtype=np.float32)


def GetExifTime(filepaths):
    times = []
    for files in filepaths:
        # read the image data using PIL
        image = Image.open(files)
        # extract EXIF data
        exifdata = image.getexif()
        exposuretime = exifdata.get(33434)
        # data = exposuretime.decode()
        times.append(exposuretime)
    return times
        # print(exposuretime)
        # # iterating over all EXIF data fields
        # for tag_id in exifdata:
        #     # get the tag name, instead of human unreadable tag id
        #     tag = TAGS.get(tag_id, tag_id)
        #     data = exifdata.get(tag_id)
        #     # decode bytes 
        #     if isinstance(data, bytes):
        #         data = data.decode()
        #     print(f"{tag:25} | {tag_id}: {data} ")

PathToCheck = scriptdir + "\\images\\splitimages"
searchterm = PathToCheck + "\\*.JPG"

files = GetFilesInFolder(searchterm)
times = GetExifTime(files)
print(times)

# parser = argparse.ArgumentParser(description='Code for High Dynamic Range Imaging tutorial.')
# parser.add_argument('--input', type=str, help='Path to the directory that contains images and exposure times.')
# args = parser.parse_args()
# if not args.input:
#     parser.print_help()
#     exit(0)

images, times = loadExposureSeq(files,times)
calibrate = cv.createCalibrateDebevec()
print("Calibrating...")
response = calibrate.process(images, times)
merge_debevec = cv.createMergeDebevec()
print("Merging 1...")

hdr = merge_debevec.process(images, times, response)
print("Merging 2...")

tonemap = cv.createTonemap(2.2)
print("Tone Mapping...")

ldr = tonemap.process(hdr)
print("LDR Tone Mapping...")

merge_mertens = cv.createMergeMertens()
print("Fusion Merge & Tone Mapping...")

# fusion = merge_mertens.process(images)
# cv.imwrite(scriptdir + '/fusion.png', fusion * 255)
# print("Saving Fusion...")

# cv.imwrite(scriptdir + '/ldr.png', ldr * 255)
# print("Saving LDR...")

cv.imwrite(scriptdir+'/hdr10k.hdr', hdr / 10000)
print("Saving HDR...")

print("HDR Created!...")


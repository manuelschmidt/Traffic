#! /usr/bin/env python

import sys, argparse

import storage, cvutils, utils

from numpy.linalg.linalg import inv
from numpy import loadtxt

parser = argparse.ArgumentParser(description='The program displays feature or object trajectories overlaid over the video frames.', epilog = 'Either the configuration filename or the other parameters (at least video and database filenames) need to be provided.')
parser.add_argument('--cfg', dest = 'configFilename', help = 'name of the configuration file')
parser.add_argument('-d', dest = 'databaseFilename', help = 'name of the Sqlite database file')
parser.add_argument('-i', dest = 'videoFilename', help = 'name of the video file')
parser.add_argument('-t', dest = 'trajectoryType', help = 'type of trajectories to display', choices = ['feature', 'object'], default = 'feature')
parser.add_argument('-o', dest = 'homographyFilename', help = 'name of the image to world homography file')
parser.add_argument('--intrinsic', dest = 'intrinsicCameraMatrixFilename', help = 'name of the intrinsic camera file')
parser.add_argument('--distortion-coefficients', dest = 'distortionCoefficients', help = 'distortion coefficients', nargs = '*', type = float)
parser.add_argument('--undistorted-multiplication', dest = 'undistortedImageMultiplication', help = 'undistorted image multiplication', type = float)
parser.add_argument('-u', dest = 'undistort', help = 'undistort the video (because features have been extracted that way)', action = 'store_true')
parser.add_argument('-f', dest = 'firstFrameNum', help = 'number of first frame number to display', type = int)
parser.add_argument('-r', dest = 'rescale', help = 'rescaling factor for the displayed image', default = 1., type = float)
parser.add_argument('-s', dest = 'nFramesStep', help = 'number of frames between each display', default = 1, type = int)
parser.add_argument('--save-images', dest = 'saveAllImages', help = 'save all images', action = 'store_true')
parser.add_argument('--last-frame', dest = 'lastFrameNum', help = 'number of last frame number to save (for image saving, no display is made)', type = int)

args = parser.parse_args()

if args.configFilename: # consider there is a configuration file
    params = storage.ProcessParameters(args.configFilename)
    videoFilename = params.videoFilename
    databaseFilename = params.databaseFilename
    if params.homography is not None:
        homography = inv(params.homography)
    else:
        homography = None
    intrinsicCameraMatrix = params.intrinsicCameraMatrix
    distortionCoefficients = params.distortionCoefficients
    undistortedImageMultiplication = params.undistortedImageMultiplication
    undistort = params.undistort
    firstFrameNum = params.firstFrameNum
else:
    homography = None
    undistort = False
    intrinsicCameraMatrix = None
    distortionCoefficients = []
    undistortedImageMultiplication = None
    firstFrameNum = 0

if not args.configFilename and args.videoFilename is not None:
    videoFilename = args.videoFilename
if not args.configFilename and args.databaseFilename is not None:
    databaseFilename = args.databaseFilename
if not args.configFilename and args.homographyFilename is not None:
    homography = inv(loadtxt(args.homographyFilename))            
if not args.configFilename and args.intrinsicCameraMatrixFilename is not None:
    intrinsicCameraMatrix = loadtxt(args.intrinsicCameraMatrixFilename)
if not args.configFilename and args.distortionCoefficients is not None:
    distortionCoefficients = args.distortionCoefficients
if not args.configFilename and args.undistortedImageMultiplication is not None:
    undistortedImageMultiplication = args.undistortedImageMultiplication
if args.firstFrameNum is not None:
    firstFrameNum = args.firstFrameNum


objects = storage.loadTrajectoriesFromSqlite(databaseFilename, args.trajectoryType)
boundingBoxes = storage.loadBoundingBoxTableForDisplay(databaseFilename)
cvutils.displayTrajectories(videoFilename, objects, boundingBoxes, homography, firstFrameNum, args.lastFrameNum, rescale = args.rescale, nFramesStep = args.nFramesStep, saveAllImages = args.saveAllImages, undistort = (undistort or args.undistort), intrinsicCameraMatrix = intrinsicCameraMatrix, distortionCoefficients = distortionCoefficients, undistortedImageMultiplication = undistortedImageMultiplication)

import numpy as np
import cv2
import myfeatures, config
import pdb
import sys
import os
import scipy.io as sio
import glob
import csv
import pickle



class VideoFeatures(object):

    """Stores the features extracted from a video file"""

    def __init__(self, config):
        """Init the capture object

        :config: (Config) the config objects
        :returns: None

        """
        self._config = config
        self._outdir = dict()
        self._features = dict()
        # instantiates the different detectors
        self.featFcn = self.config.compute # converts the list of features to actual objects

    @property
    def config(self):
        """A config object"""
        return self._config


    @property
    def featFcn(self):
        """The feature computation functions"""
        return self._featFcn # return a dict

    @featFcn.setter
    def featFcn(self, lst):
        """Sets the features objects from the list (HOG...)"""
        self._featFcn = dict() # empty dict
        if 'HOG' in lst:
            self._featFcn['HOG'] = myfeatures.MyHOG(self.config)
        if 'SIFT' in lst:
            self._featFcn['SIFT'] = myfeatures.MySIFT(self.config)
        if 'DCT' in lst:
            self._featFcn['DCT'] = myfeatures.MyDCT(self.config)
        if 'AAM' in lst:
            self._featFcn['AAM'] = myfeatures.MyAAM(self.config)

    @property
    def features(self):
        """The dictionary of computed features, with keys the features and subkeys the files"""
        return self._features


    @features.setter
    def features(self, lst):
        """Sets a new feature dict with the correct keys"""
        self._features.clear()
        self._features = {feat: dict() for feat in self.config.compute}




    @property
    def folderpath(self):
        """The video ID to be processed"""
        return self._folderpath

    @folderpath.setter
    def folderpath(self, name):
        self._folderpath = name
        return



    def initFolder(self,foldername):
        """Init a new folder to be processed"""
        self.folderpath = foldername
        self.features = self.config.compute # we reset the features, will be a dictionary of dictionaries with keys the features and subkeys the files

    def processFolder(self):
        """Process all videos inside the folder"""
        FILE_TYPE = "*.mat"
        for matname in glob.glob("{}/{}".format(self.folderpath, FILE_TYPE)): # for all the mat files inside the folder
            # for all mat files inside the folder
            self.processMat(matname)
            if self.config.debug:
                break



    def processMat(self, matname):
        """Read a video from a matname

        :matname: (string) the path to the mat
        :returns: (np.ndarray) the video under matrix format

        """
        mat = sio.loadmat(matname) # we fetch the mat data
        matID = os.path.basename(matname)
        imgs = mat['ROIs'][0][0][0] # all the different images, in grayscale
        if self.config.resize: # if we want to resize the images
            imgs = [cv2.resize(frame, (self.config.std_dim, self.config.std_dim), interpolation=cv2.INTER_CUBIC) for frame in imgs]
        # self.cap = cv2.VideoCapture(matname) # initialise the cap object to read the video
        self.nframe = len(imgs) # the number of different images
        # we add the matID key to the features dictionary

        # actual feature computation
        for feat in self.config.compute: # for all features to compute
            self.features[feat][matID] = self.nframe * [0] # empty list of correct dimensions
            for framenbr, frame in enumerate(imgs): # for all the images in the ROI
                if self.config.verbose:
                    print("Computing feature {} for mat {}, frame # {}".format(feat, matID, framenbr))
                self.featFcn[feat].compute(frame) # we compute the feature
                self.features[feat][matID][framenbr] = self.featFcn[feat].fd # we store the feature desciptor
                if self.featFcn[feat].config.visualise and framenbr == 0: # if we want to visualise the feature
                    self.featFcn[feat].save_visu("{}/{}_visu_{}.jpg".format(self.folderpath, matID, feat)) # we save the visualisation
        return



    def save(self):
        """Saves the features as csv files"""
        for feat in self.config.compute: # for every features
            with open("{}/output_{}.csv".format(self.folderpath, feat.lower()), 'w') as csvfile:
                featwriter = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting = csv.QUOTE_MINIMAL)
                featwriter.writerow(["file", "frame_number", "feature_vector"])
                for matID in self.features[feat].keys(): # for all the files
                    for idx, fd in enumerate(self.features[feat][matID]): # for all possible feature descriptor
                        serialized = pickle.dumps(fd, protocol=0) # we serialize the object
                        featwriter.writerow([matID, idx+1, serialized]) # WARN: the frame number starts at 1


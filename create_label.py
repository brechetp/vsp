__doc__ = """This scripts creates the labels for each video"""
import mappings as mps
import pdb
import os
import glob
import myio as mio


mapp = mps.Mappings() # the mappings between words, phonemes and visemes

ROOTPATH='/Volumes/data/vsp/data/'
video_lst = ['08F']

labelfile = '/Users/Pierre/Documents/ws17/vsp/project/HW3/volunteer_labelfiles.mlf'
label_root = '/Users/Pierre/Documents/ws17/vsp/project/HW3/labels'

def parse_labelfile(label_filename):
    """Parse the label file to create the different label files for the different videos"""
    # the header before each file is of the form 
    # "Q:/Videos/TCD-TIMIT/volunteers/01M/Clips/straightcam/sa1.rec"
    # each file record is terminated with '.'

    videoID = '' # the video ID (01M...)
    fileID = '' # the file ID (sa1...)
    with open(label_filename, 'r') as lbl_file:
        lbl_file.readline() # we skip the header
        file_lines = lbl_file.readlines()
        label_lst = list() # the label list, one per folder
        for line in file_lines:
            line = line.strip()
            line = line.strip('"')
            line = line.split(' ') # each reco
            if len(line) == 1: # if we are at the beginning or end of a file
                if line[0] == '.': # we end a current file transcription
                    pass #TODO the trick is to create a new folder if the new video ID is different from the old one
                else: # the line is a path to the video file

                    new_videoID, fileID = parse_videopath(line[0]) # we parse the new videoID and file ID
                    if new_videoID != videoID and videoID != '': # we need to create a new folder and write the file to the previous one
                        label_dir = os.path.join(label_root, videoID)
                        if not os.path.isdir(label_dir):
                            os.mkdir(label_dir)
                        label_path = os.path.join(label_dir, 'labels.txt')
                        mio.write_list(label_lst, label_path) # saves the list to disk
                        videoID = new_videoID # change the video ID
                        label_lst.clear() # reset the label list (one per folder)
                    # end case
                    # else if new_fileID != fileID: # we are in the same folder bus a different file
                        # # we need to prefix the label list with the new file name

            else: # the line is frame1 frame2 phoneme
                phn = line[2]
                vis = mapp.phonemeToViseme(phn)
                new_label = "{} {} {} {} {}".format(fileID, line[0], line[1], phn, vis)
                label_lst.append(new_label)
            # end if
        # end for
    #end
    return

def parse_videopath(path):
    '''Parse the video path of the type "Q:/Videos/TCD-TIMIT/volunteers/01M/Clips/straightcam/sa1.rec"'''
    head, tail= os.path.split(path)
    dirs = head.split('/') # the different directories in the head
    videoID  = dirs[4]
    fileID = tail.split('.')[0].upper()
    return videoID, fileID



if __name__ == "__main__":
    
    parse_labelfile(labelfile)






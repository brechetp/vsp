import pdb
import capture
import sys
import config
import glob

if len(sys.argv) != 2:
    folderpath = "/Volumes/data/vsp/data/08F"
else:
    folderpath = sys.argv[1]

config = config.Config()
features = capture.VideoFeatures(config)
for folderpath in glob.glob("/Users/Pierre/Dropbox/TUM 1718 (1)/HW2_features/features_1-7/*"):
    print("Processing {}...".format(folderpath))
    features.initFolder(folderpath)
    features.load()
    pdb.set_trace()
    # features.processFolder()

    # features.save()

# features.computeFeatures()






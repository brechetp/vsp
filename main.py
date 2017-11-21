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
for folderpath in glob.glob("/Volumes/data/vsp/data/*"):
    print("Processing {}...".format(folderpath))
    features.initFolder(folderpath)
    features.processFolder()
    features.save()

# features.computeFeatures()






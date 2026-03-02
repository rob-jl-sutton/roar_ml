#author:rob-jl-sutton
#purpose of script is to generate
#patches for ML training of aneurysm segmentation
#
#
#0.0 import modules
import os.path
import glob

#2.0 perform recursive search to identify available roi files
matches = glob.glob("D:/**/*roi.nrrd", recursive = True)
ids = [match[3:9] for match in matches]
ids_unique = list(set(ids))
print(ids_unique)
os.makedirs(r"C:\Documents\ROAR workflow 6.0\volumes_patches", exist_ok=True)

"C:\Users\suttor\Documents\ROAR workflow 6.0"
#3.0 specify patch size and adjust number of patches if required


#recommended patch density


#4.0 save to single output file training_patches

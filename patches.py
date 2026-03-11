#author:rob-jl-sutton
#purpose of script is to generate
#patches for ML training of aneurysm segmentation

#0.0 import modules
import os.path
import glob
import SimpleITK as sitk
import random
import numpy as np

#1.0 perform recursive search to identify available roi files
matches = glob.glob("D:/**/*.nrrd", recursive = True)
ids = [match[3:9] for match in matches]
ids_unique = list(set(ids))
os.makedirs(r"C:\Users\suttor\Documents\ROAR workflow 6.0\volumes_patches", exist_ok=True)

#2.0 loop through nrrds and check metadata manually - confirming
for file_path in matches:
    #read image
    img = sitk.ReadImage(file_path)

    #access metadata
    spacing = img.GetSpacing()
    size = img.GetSize()
    origin = img.GetOrigin()
    
    #print metadata
    print(file_path)
    print(f'Spacing: {spacing}')
    print(f'Size: {size}')
    print(f'Origin: {origin}')
    print(10*'=')

#3.0 specify patch size and adjust number of patches if required
patch_size = 128 #1d voxel count for cubic patch i.e. for patch_size*patch_size*patch_size voxels
patches_per_volume = 10

for id in ids_unique:

    #find files containing matching id
    id_files = [m for m in matches if id in m]

    images = {}
    for f in id_files:
        if "mra_roi.nrrd" in f:
            images["mra"] = sitk.ReadImage(f)
        elif "cta_roi.nrrd" in f:
            images["cta"] = sitk.ReadImage(f)
        elif "dsa_roi.nrrd" in f:
            images["dsa"] = sitk.ReadImage(f)
        elif "dsa_roi_segmentation.seg.nrrd" in f:
            images["dsa_seg"] = sitk.ReadImage(f)

    if len(images) == 0:
        continue

    #all 4cm volumes have matched resolutions so no need for nearest neighbour here
    #use whichever is first in images as the reference image
    ref_img = list(images.values())[0]
    size = ref_img.GetSize()

    for p in range(patches_per_volume):

        #random start coordinate
        x0 = random.randint(0, size[0] - patch_size)
        y0 = random.randint(0, size[1] - patch_size)
        z0 = random.randint(0, size[2] - patch_size)

        for modality, img in images.items():

            if modality == "dsa_seg":
                patch = sitk.RegionOfInterest(
                    img,
                    size=[patch_size, patch_size, patch_size],
                    index=[x0, y0, z0]
                )

                patch_name = f"{modality}128_{id}_{p:03d}.nrrd"
                out_path = os.path.join(
                    r"C:\Users\suttor\Documents\ROAR workflow 6.0\volumes_patches",
                    patch_name
                )

                sitk.WriteImage(patch, out_path)
                continue

            arr_vol = sitk.GetArrayFromImage(img)

            if modality=='cta':
                vmin = arr_vol.min()
                vmax = arr_vol.max()

            elif modality in ['mra', 'dsa']:
                mean = arr_vol.mean()
                std = arr_vol.std()

            patch = sitk.RegionOfInterest(
                img,
                size=[patch_size, patch_size, patch_size],
                index=[x0, y0, z0]
            )

            arr = sitk.GetArrayFromImage(patch)

            if modality == 'cta':
                arr = (arr - vmin) / (vmax - vmin)

            elif modality in ['mra', 'dsa']:
                arr = (arr - mean) / std

            patch_name = f"{modality}128_{id}_{p:03d}.nrrd"
            out_path = os.path.join(
                r"C:\Users\suttor\Documents\ROAR workflow 6.0\volumes_patches",
                patch_name
            )

            patch_norm = sitk.GetImageFromArray(arr)
            patch_norm.CopyInformation(patch)
            patch = patch_norm
            sitk.WriteImage(patch, out_path)
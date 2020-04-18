import csv
import os
import shutil
import random

dataLen = {}
data = {}
remove_dir = []
path = os.getcwd()
image_set =  "./dataset_images"
style_set = "./dataset_styles"

for root, directories, files in os.walk(image_set):
  if len(files) > 200:
    dataLen[root] = len(files)
    data[root] = files
  else:
    if root != './dataset_images':
      remove_dir.append(root)

for i in remove_dir:
  folder = i.split('/')[-1]
  shutil.rmtree("{}".format(i))
  shutil.rmtree("{}/{}".format(style_set, folder))

smallest = min(list(dataLen.values()))

for i in data:
  folder = i.split('/')[-1]
  sample = random.sample(data[i], dataLen[i] - smallest)
  for file in sample:
    os.remove("{}/{}".format(i, file))
    jsonFile = file.split(".jpg")[0]
    os.remove("{}/{}/{}.json".format(style_set, folder, jsonFile))

print("Done")

import os
import shutil
from resizeimage import resizeimage
from PIL import Image

img_dir = "./dataset_images"
output_dir = './fashion_spark'

os.mkdir(output_dir)

for root, directories, files in os.walk(img_dir):
  label = root.split('/')[-1]
  if label != 'dataset_images':
    os.mkdir("{}/{}".format(output_dir, label))
  for f in files:
    if f == '.DS_Store':
      continue
    img_dir = '{}/{}'.format(root, f)
    im = Image.open(img_dir).convert('L')
    x, y = im.size
    fill_color = (255, 255, 255, 0)
    if x < y:
      size_x = y
      size_y = y
    else:
        size_x = x
        size_y = x
    new_im = Image.new('RGB', (size_x, size_y), fill_color)
    new_im.paste(im, (int((size_x - x) / 2), int((size_y - y) / 2)))
    width = 100
    img_rescaled = resizeimage.resize_cover(new_im, [width, width])

    img_rescaled.save("{}/{}/{}".format(output_dir, label, f))

print("Done")
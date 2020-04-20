import os
import shutil
from PIL import Image
from resizeimage import resizeimage
import joblib
from pyspark.ml.image import ImageSchema
from pyspark.sql.functions import lit
from pyspark.sql import SQLContext
from pyspark import SparkContext,SparkConf
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml import PipelineModel
from sparkdl import DeepImageFeaturizer

def rescale_image(img_dir, rescaled_dir):
  for root, directories, files in os.walk(img_dir):
    os.mkdir(rescaled_dir)
    for img in files:
      if '.DS_Store' in img:
        continue
      im = Image.open("{}/{}".format(root, img)).convert('L')
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
      width = 80
      img_rescaled = resizeimage.resize_cover(new_im, [width, width])
      img_rescaled.save("{}/rescaled/{}".format(root, img))

if __name__ == "__main__":
  sc = SparkContext()
  img_dic = joblib.load("dictionary.pkl")[0]
  featurizer = DeepImageFeaturizer(inputCol="image", outputCol="features", modelName="InceptionV3")
  lr = LogisticRegressionModel.load('./lrModel')
  p_model = PipelineModel(stages=[featurizer, lr])

  directory = "./media"
  rescaled_dir = "{}/rescaled".format(directory)

  rescale_image(directory, rescaled_dir)

  temp_df = ImageSchema.readImages(rescaled_dir)
  df = p_model.transform(temp_df)
  f = open("predict_output.txt", "r+")
  f.seek(0)
  f.truncate()
  for i in df.select(['image','prediction']).collect():
    print("{} = {}".format(i[0][0].split('/')[-1], img_dic[int(i[1])]))
    f.write("{} = {}\n".format(i[0][0].split('/')[-1], img_dic[int(i[1])]))
  f.close()

  shutil.rmtree(rescaled_dir)

  # spark-submit --packages databricks:spark-deep-learning:1.5.0-spark2.4-s_2.11 predict.py
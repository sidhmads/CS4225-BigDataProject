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
      width = 100
      img_rescaled = resizeimage.resize_cover(new_im, [width, width])
      img_rescaled.save("{}/rescaled/{}".format(root, img))

if __name__ == "__main__":
  sc = SparkContext()
  img_dic = joblib.load("dictionary.pkl")[0]
  featurizer = DeepImageFeaturizer(inputCol="image", outputCol="features", modelName="InceptionV3")
  lr = LogisticRegressionModel.load('./lrModel')
  p_model = PipelineModel(stages=[featurizer, lr])

  directory = "./predict_images"
  rescaled_dir = "{}/rescaled".format(directory)

  rescale_image(directory, rescaled_dir)

  temp_df = ImageSchema.readImages(rescaled_dir)
  df = p_model.transform(temp_df)
  for i in df.select(['image','prediction']).collect():
    print("{} = {}".format(i[0][0].split('/')[-1], img_dic[int(i[1])]))

  shutil.rmtree(rescaled_dir)

  # spark-submit --packages databricks:spark-deep-learning:1.5.0-spark2.4-s_2.11 predict.py
import os
import joblib
from pyspark.ml.image import ImageSchema
from pyspark.sql.functions import lit
from pyspark.sql import SQLContext
from pyspark import SparkContext,SparkConf
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml import Pipeline, PipelineModel
from sparkdl import DeepImageFeaturizer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

def getDataFrame(img_dir):
  dic = {}
  df_train = []
  df_test = []
  count = 0

  for root, directories, files in os.walk(img_dir):
    for file in directories:
      temp_df = ImageSchema.readImages(img_dir + "/" + file).withColumn("label", lit(count))
      train_df, test_df = temp_df.randomSplit([0.6, 0.4])
      df_train.append(train_df)
      df_test.append(test_df)
      if dic.get(count,None):
        continue
      else:
        dic[count] = file
        count += 1

  trained_df = df_train[0]
  for i in range(1, len(df_train)):
    trained_df = trained_df.unionAll(df_train[i])

  tested_df = df_test[0]
  for i in range(1, len(df_test)):
    tested_df = tested_df.unionAll(df_test[i])

  return trained_df, tested_df, dic

if __name__ == "__main__":

  sc = SparkContext()
  sqlContext = SQLContext(sc)

  directory = "./fashion_spark"

  train_df, test_df, dic = getDataFrame(directory)

  train_df = train_df.repartition(10)
  test_df = test_df.repartition(10)

  train_df.cache()

  featurizer = DeepImageFeaturizer(inputCol="image", outputCol="features", modelName="InceptionV3")
  lr = LogisticRegression(maxIter=20, regParam=0.05, elasticNetParam=0.3, labelCol="label")
  p = Pipeline(stages=[featurizer, lr])

  p_model = p.fit(train_df)

  p_model.stages[1].save('lrModel')
  joblib.dump((dic,), "dictionary.pkl", compress=3)

  test_df.cache()

  df = p_model.transform(test_df)
  df.show()

  predictionAndLabels = df.select("prediction", "label")
  evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
  print("Training set accuracy = " + str(evaluator.evaluate(predictionAndLabels)))

  print("Done")


  # spark-submit --executor-cores 3 --num-executors 8  --driver-memory 32g --executor-memory 16g --packages databricks:spark-deep-learning:1.5.0-spark2.4-s_2.11 classify_spark.py

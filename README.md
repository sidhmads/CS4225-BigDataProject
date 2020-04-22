# SparkFab! The Fashion Search

## Run the application

- Make the shell script executable by running the following command in terminal
``` 
  chmod +x ./run_application.sh
  ```
- Once it is executable, run the following comand in terminal
```
./run_application.sh
```
- Visit the URL http://127.0.0.1:8000/fashion to view the web application

## Run ElasticSearch Service

- Download ELK stack from the follwing website, https://www.elastic.co/downloads/ and setup Environment Variables

- Make the shell script executable by running the following command in terminal
``` 
  chmod +x ./setup_elastic.sh
  ```
- Once it is executable, run the following comand in terminal
```
./setup_elastic.sh
```
- Visit the URL http://127.0.0.1:8000/fashion to view the web application and use elasticsearch functionality

## Runing model with fashion-dataset from kaggle

### Downloading dataset from kaggle

- The dataset can be found here: https://www.kaggle.com/paramaggarwal/fashion-product-images-dataset

- Download the dataset and unzip it to this folder

### Getting the data ready for the model
- Make the shell script executable by running the following command in terminal
``` 
  chmod +x ./convert_dataset.sh
  ```
- Once it is executable, run the following comand in terminal
```
./convert_dataset.sh
```
This shell file does the following:
1. Partition the data:
    - converts all the images to individual labels according to the `styles.csv` file provided with the kaggle dataset.
2. Normalize the data
    - keeps all the labels with at least 200 images
    - normalizes those labels to have the same number of images.
3. Convert to grey scale
    - converts the normalized images to grey scale and store it in the `fashion_spark` directory.

### Creating the model
- Run this command in the terminal
```
spark-submit --packages databricks:spark-deep-learning:1.5.0-spark2.4-s_2.11 --executor-cores 5 --num-executors 24 --driver-memory 32g --executor-memory 32g ./classify_spark.py
```
- This will create `lrModel` directory that contains the trained model and a `dictionary.pkl` file that contains the labels used to train the model

### Predicting the results
- Place the images to be predicted in `media` directory
- Run this command in the terminal
```
spark-submit --packages databricks:spark-deep-learning:1.5.0-spark2.4-s_2.11 ./predict.py
```
- This will output the prediction labels for all the images

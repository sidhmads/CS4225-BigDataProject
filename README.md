# SparkFab! The Fashion Search

#### NOTE: Windows Compatible README

## A. Environment Setup

- Install pipenv in the system

```
pip install pipenv
```

- Clone the git repository

```
git clone https://github.com/sidhmads/CS4225-CS5425-BigDataProject.git
```

- Move to project directory

```
cd CS4225-CS5425-BigDataProject
```

- Downloading dataset from kaggle. The dataset can be found here: https://www.kaggle.com/paramaggarwal/fashion-product-images-dataset

- Download the dataset and unzip it inside the `CS4225-CS5425-BigDataProject/fashion` folder

- Make sure this folder structure exists `CS4225-CS5425-BigDataProject/fashion/fashion-dataset`

- `fashion_spark` directory with all the pre-processed and normalised images are already provided in this GitHub Repo. However if you wish to do that yourself, please remove `CS4225-CS5425-BigDataProject/fashion/fashion_spark` and do the following commands
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

- Start the pipenv shell virtual environment

```
pipenv shell
```

- Install the project dependencies (Takes longer time)

```
pipenv install
```

- View the dependencies installed
```
pipenv graph
```

## B. Chose the method you want to run this application
### 1. Running the application (With Elasticsearch Service)

- Download ELK stack from the follwing website for windows machine, https://www.elastic.co/downloads/ and setup the Environment Variables

- Make the shell script executable by running the following command in terminal

```
  chmod +x ./setup_elastic_data.sh
```

- Once it is executable, run the following comand in terminal. This will create metadata `elastic-data.csv` in the fashion-dataset folder `(./fashion/fashion-dataset)`

```
./setup_elastic_data.sh
```
- Start the elasticsearch service
  - If you have the .bat file (Run the bat file from elasticsearch bin folder)
  ```
    elasticsearch.bat
  ```
  - If you have elasticsearch installed as a service just run
  ```
    elasticsearch
  ```

- Change the input file path value in logstash.conf in fashion folder `(./fashion/logstash.conf)` to point to the `elastic-data.csv` that was created previously. This creates data stream pipeline and uploads data to the elastic cluster

```
input {
    file{
        path => ["absolutepath required"]
        start_position => "beginning"
        sincedb_path => "NULL"
    }
}
```
- Stream Data into elastic cluster using logstash (Open another terminal)

```
cd ./fashion
logstash -f logstash.conf
```
- If yours is a linux machine, you would need to change the following:
  - In `views.py`
    - In `runModel` function
      - Change the `.\predict.py` in `subprocess.Popen` method 
        - To `./predict.py`
- Make the shell script executable by running the following command in terminal

```
  chmod +x ./run_application.sh
```

- Once it is executable, run the following comand in terminal

```
./run_application.sh
```

- Visit the URL http://127.0.0.1:8000/fashion to view the web application

### 2. Running the application (Without Elasticsearch Service)

- If yours is a linux machine, you would need to change the following:
  - In `views.py`
    - In `runModel` function
      - Change the `.\predict.py` in `subprocess.Popen` method 
        - To `./predict.py`

- Make the shell script executable by running the following command in terminal

```
  chmod +x ./run_application.sh
```

- Once it is executable, run the following comand in terminal

```
./run_application.sh
```

- Visit the URL http://127.0.0.1:8000/fashion to view the web application
### 3.  Runing model with fashion-dataset from kaggle (In standalone mode)

#### Creating the model

- Run this command in the terminal

```
spark-submit --packages databricks:spark-deep-learning:1.5.0-spark2.4-s_2.11 --executor-cores 5 --num-executors 24 --driver-memory 32g --executor-memory 32g ./classify_spark.py
```

- This will create `lrModel` directory that contains the trained model and a `dictionary.pkl` file that contains the labels that is used to evaluate the model

### Predicting the results

- Create a folder called `media` in the `CS4225-CS5425-BigDataProject/fashion/` directory
- Place the images to be predicted in `media` folder
- Run this command in the terminal

```
spark-submit --packages databricks:spark-deep-learning:1.5.0-spark2.4-s_2.11 ./predict.py
```

- This will output the prediction labels for all the images in that `media` folder

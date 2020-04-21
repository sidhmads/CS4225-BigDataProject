import pandas as pd

images_df = pd.read_csv("./fashion-dataset/images.csv", error_bad_lines=False)
images_df = images_df.rename(columns=({'filename':'id'}))
images_df['id'] = images_df['id'].map(lambda val: val.split(".")[0]).astype(int)
styles_df = pd.read_csv("./fashion-dataset/styles.csv", error_bad_lines=False)
merged_df = images_df.merge(styles_df, on='id')
merged_df.to_csv("./fashion-dataset/elastic-data.csv", index=False)
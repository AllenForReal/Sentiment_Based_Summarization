import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('train-balanced-sarcasm.csv')

df = df.dropna()
df = df.drop_duplicates()
num_rows, num_columns = df.shape
print(f"Number of rows for the testing set: {num_rows}")
print(f"Number of columns for the testing set: {num_columns}")
df.head()
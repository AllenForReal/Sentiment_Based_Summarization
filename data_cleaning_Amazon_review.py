import pandas as pd
import torch
import numpy as np
import math




file_path1 = 'test.ft.txt'
file_path2 = 'train.ft.txt'

with open(file_path1, 'r') as file:
    lines = file.readlines()

df1 = pd.DataFrame(lines, columns=['text'])
df1['text'] = df1['text'].str.strip()

df1 = df1.dropna()
df1 = df1.drop_duplicates()
num_rows, num_columns = df1.shape
print(f"Number of rows for the testing set: {num_rows}")
print(f"Number of columns for the testing set: {num_columns}")

with open(file_path2, 'r') as file:
    lines = file.readlines()

df2 = pd.DataFrame(lines, columns=['text'])
df2['text'] = df2['text'].str.strip()

df2 = df2.dropna()
df2 = df2.drop_duplicates()
num_rows, num_columns = df2.shape
print(f"Number of rows for the training set: {num_rows}")
print(f"Number of columns for the training set: {num_columns}")

print(df1.head())
print(df2.head())

# test = pd.read_csv('test.ft.txt', sep='\n', header=None, names=['text'])
#
# train = pd.read_table('train.ft.txt')
# print(len(test))
# print(len(train))
# print(test.head(n=10))
# print(train.head())
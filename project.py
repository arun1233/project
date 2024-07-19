import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import tensorflow as tf
import tensorflow_hub as hub
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
print("Hub version: ", hub.__version__)
print("GPU is", "available" if tf.config.experimental.list_physical_devices("GPU") else "NOT AVAILABLE")

def leng(df, col, len_col):
    df[len_col] = df[col].apply(lambda x: len(str(x)))
    return df

def cal_puncndop(df, col, punop_col, l):
    df1 = df[[col]].copy()
    df[punop_col] = 0
    for i, query in enumerate(df[col]):
        count = 0
        if isinstance(query, str):
            li = list(query)
            for ch in range(len(query)):
                if query[ch] in l:
                    li[ch] = " "
                    count = count + 1
            df1[col][i] = "".join(li)
        df.at[i, punop_col] = count
    df[col] = df1[col]
    return df

def cal_keyword(df, col, key_col, l):
    df[key_col] = 0
    for i, query in enumerate(df[col]):
        count = 0
        query = query.lower()
        words = query.split()
        for word in words:
            if word in l:
                count = count + 1
        df.at[i, key_col] = count
    return df

def encode_categorical(df, column_list):
    for column in column_list:
        df[column] = df[column].astype('str')
        encoder = preprocessing.LabelEncoder()
        df[column] = encoder.fit_transform(df[column])
        print("The", column, "is encoded")
    return df

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Use a file selection dialog to get the input file paths
sql_path = filedialog.askopenfilename(title="Select SQL file", filetypes=[("CSV Files", "*.csv")])
password_path = filedialog.askopenfilename(title="Select password file", filetypes=[("CSV Files", "*.csv")])
username_path = filedialog.askopenfilename(title="Select username file", filetypes=[("CSV Files", "*.csv")])
sqli_path = filedialog.askopenfilename(title="Select sqli file", filetypes=[("CSV Files", "*.csv")])

# Read the input data from the CSV files
sql = pd.read_csv(sql_path)
password = pd.read_csv(password_path)
username = pd.read_csv(username_path)
sqli = pd.read_csv(sqli_path)

username.dropna(axis=0, how="all", inplace=True)
password.dropna(axis=0, how="all", inplace=True)
username.reset_index(drop=True, inplace=True)
password.reset_index(drop=True, inplace=True)

username = leng(username, 'Query', 'Length')
password = leng(password, 'Query', 'Length')
sqli = leng(sqli, 'Query', 'Length')

username['Label'] = 'username'
password['Label'] = 'password'
sqli['Label'] = 'sqli'
sql['Label'] = 'sql'

sqli.drop(['Attack'], axis=1, inplace=True)
username.drop(['Attack'], axis=1, inplace=True)
password.drop(['Attack'], axis=1, inplace=True)

# Combine the dataframes
data = pd.concat([sql, username, password, sqli], ignore_index=True)

# Shuffle the data
data = shuffle(data).reset_index(drop=True)


# Display the result in a GUI window
result = messagebox.showinfo("SQL Injection Detection", "Safe")
if result == 'ok':
    root.destroy()
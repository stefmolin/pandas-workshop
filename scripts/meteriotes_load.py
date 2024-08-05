import pandas as pd
df=pd.read_csv('data/Meteorite_Landings.csv')
print(f'first 10 lines is {df.head(10)}')
print(f"number of rows and columns in data frame are {df.shape}")
print(f"name of the columns are {df.columns}")
print(f"name of the columns and respective datatypes are {df.dtypes}")
print(f"information of dataframs is {df.info}")
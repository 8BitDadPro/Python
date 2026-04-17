
# '░' 'â'
# '█' 'â'

import requests
import pandas as pd
import matplotlib.pyplot as plt
import lxml

url = 'https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub'
df_list = pd.read_html(url, skiprows=1)
df = df_list[0]
df.to_csv('data.csv')

csv_file_x_cords = pd.read_csv('data.csv', usecols=[1])
csv_file_characters = pd.read_csv('data.csv', usecols=[2])
csv_file_y_cords = pd.read_csv('data.csv', usecols=[3])

x_cords = []
characters = []
y_cords = []
for index, row in csv_file_x_cords.iterrows():
    x_cords.append(row.iloc[0])

for index, row in csv_file_characters.iterrows():
    characters.append(row.iloc[0])

for index, row in csv_file_y_cords.iterrows():
    y_cords.append(row.iloc[0])

# grid = []
# for i in range(10):        
#     for x in range(100):
#         if x_cords[x] == x:
#             pass        
#         if y_cords[x] == i:
#                 if characters[x] == 'â':
#                     grid.append('░')
#                 elif characters[x] == 'â':
#                     grid.append('█')
#         else:
#             grid.append('')
#     grid.append('\n')

grid = []
for x in range(len(x_cords)):
    print(x_cords[x])

# print(*grid)
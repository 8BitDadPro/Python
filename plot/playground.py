import pandas as pd
import matplotlib.pyplot as plt

url = 'https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub'

# Read table from webpage
df = pd.read_html(url, skiprows=1)[0]

# Convert types
df['x'] = df[0].astype(int)
df['y'] = df[2].astype(int)
df['char'] = df[1].astype(str)


max_x = df['x'].max()
max_y = df['y'].max()

grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

for _, row in df.iterrows():
    grid[row['y']][row['x']] = row['char']

print("\nASCII Output:\n")
for row in reversed(grid):  # flip so origin is bottom-left
    print(''.join(row))

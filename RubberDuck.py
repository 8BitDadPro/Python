import pandas as pd
from hashlib import sha256

dict = pd.read_csv("100k-most-used-passwords-NCSC.csv", usecols=['password'])
df = pd.read_csv("users.csv", usecols=['usernames', 'password_hash'])

def convert_to_hash(word):
    pass_bytes = str(word).encode('utf-8')
    pass_hash = sha256(pass_bytes)
    digest = pass_hash.hexdigest()
    return digest

for x in range(len(df)):
    for i in dict.password:
        if df.password_hash.at[x] == str(convert_to_hash(i)):
            print("Username: " + str(df.usernames.at[x]) + ' | Un-Hashed pwd: ' + i + ' | Hashed pwd: ' + str(df.password_hash.at[x]))
            break
        else:
            continue
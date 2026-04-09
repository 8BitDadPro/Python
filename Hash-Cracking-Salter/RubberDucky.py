import pandas as pd
from hashlib import sha256
import time

def convert_to_hash(word):
    # """Hashes a word using SHA256."""
    pass_bytes = str(word).encode('utf-8')
    pass_hash = sha256(pass_bytes)
    return pass_hash.hexdigest()

if __name__ == '__main__':
    start_time = time.process_time()

    # 1. Load the data
    dict_df = pd.read_csv("100k-most-used-passwords-NCSC.csv", usecols=['password'])
    users_df = pd.read_csv("users.csv", usecols=['usernames', 'password_hash'])

    # 2. Pre-compute all dictionary hashes and store in a lookup map
    # This is the key optimization: Hash the 100k passwords ONLY ONCE.
    # The map will be { 'hashed_password': 'plain_text_password', ... }
    print("Hashing password dictionary...")
    password_map = {convert_to_hash(pwd): pwd for pwd in dict_df['password']}
    print("Hashing complete.")

    # 3. Find all matches in a single vectorized operation
    # '.isin()' is highly optimized to check for membership.
    # This creates a boolean Series: True if the user's hash is in our map, otherwise False.
    matches = users_df['password_hash'].isin(password_map.keys())

    # 4. Filter the user DataFrame to get only the rows that had a match
    found_df = users_df[matches].copy() # Use .copy() to avoid SettingWithCopyWarning

    # 5. Map the found hashes back to their original plain-text passwords
    # '.map()' uses our dictionary to look up the original password for each hash.
    found_df['un-hashed_pwd'] = found_df['password_hash'].map(password_map)

    end_time = time.process_time()

    # 6. Write the results to a file
    if not found_df.empty:
        print(f"\nFound {len(found_df)} matching passwords!")
        with open('slung_the_hash.txt', 'w') as f:
            f.write("--- Cracked Passwords ---\n")
            for index, row in found_df.iterrows():
                f.write(f"Username: {row['usernames']} | Un-Hashed pwd: {row['un-hashed_pwd']} | Hashed pwd: {row['password_hash']}\n")
        print("Results saved to 'slung_the_hash.txt'")
    else:
        print("\nNo matching passwords found.")

    print(f"\nTotal processing time: {end_time - start_time:.2f}s")
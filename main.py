import re
import sqlite3
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# Define a function to remove matras
def remove_matras(text):
    return transliterate(text, sanscript.SLP1, sanscript.DEVANAGARI).replace('\u093e', '').replace('\u093f', '').replace('\u0940', '').replace('\u0941', '').replace('\u0942', '').replace('\u0943', '').replace('\u0944', '').replace('\u0947', '').replace('\u0948', '').replace('\u094b', '').replace('\u094c', '').replace('\u0962', '').replace('\u0963', '')

# Katapayadi encoding mapping
katapayadi_mapping = {
    'क': 1, 'ख': 2, 'ग': 3, 'घ': 4, 'ङ': 5,
    'च': 6, 'छ': 7, 'ज': 8, 'झ': 9, 'ञ': 0,
    'ट': 1, 'ठ': 2, 'ड': 3, 'ढ': 4, 'ण': 5,
    'त': 6, 'थ': 7, 'द': 8, 'ध': 9, 'न': 0,
    'प': 1, 'फ': 2, 'ब': 3, 'भ': 4, 'म': 5,
    'य': 1, 'र': 2, 'ल': 3, 'व': 4, 'श': 5,
    'ष': 6, 'स': 7, 'ह': 8, 'ळ': 9,
}

def katapayadi_encode(word):
    # Reverse the word for Katapayadi encoding
    reversed_word = word[::-1]
    number = ''
    for char in reversed_word:
        if char in katapayadi_mapping:
            number += str(katapayadi_mapping[char])
    return number

# Read the input text from the file
with open('/Users/abhishekpurohit/Downloads/shs/mci.txt', 'r', encoding='utf-8') as file:
    input_text = file.read()

# Find all words between <k1> and <k2> tags
pattern = re.compile(r'<k1>(.*?)<k2>', re.DOTALL)
matches = pattern.findall(input_text)

# Process and remove matras, then encode using Katapayadi system
encoded_results = []
for k1_word in matches:
    k1_word_without_matras = remove_matras(k1_word)
    k1_encoded = katapayadi_encode(k1_word_without_matras)
    encoded_results.append((k1_word, k1_word_without_matras, k1_encoded))

# Print the encoded results
for original, without_matras, encoded in encoded_results:
    print(f"Original: {original}, Without Matras: {without_matras}, Encoded: {encoded}")

def create_and_populate_db(processed_words, db_path='words.db'):
    # Connect to the SQLite database (or create it)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT,
            encoded_word TEXT,
            encoded INTEGER
        )
    ''')
    
    # Insert data
    cursor.executemany('''
        INSERT INTO Words (word, encoded_word, encoded) VALUES (?, ?, ?)
    ''', processed_words)
    
    # Commit and close
    conn.commit()
    conn.close()

# Optionally, save the results to a file
with open('encoded_output.txt', 'w', encoding='utf-8') as file:
    processed_words = []
    for original, without_matras, encoded in encoded_results:
        processed_words.append((original, without_matras,encoded))
    create_and_populate_db(processed_words)

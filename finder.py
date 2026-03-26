from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher
import base64
import threading

lock=threading.Lock()

LEET_MAP = str.maketrans({
    '3': 'e',
    '0': 'o',
    '1': 'l',
    '@': 'a',
    '7': 't',
    '5': 's'
})

WORDS_TO_FIND = [w.lower() for w in ["macbeth", "romeo", "juliet", "hamlet", "ab"]]
WORDS_LIST_PATH = "./words_list.txt"
THREADS = 10

found = {} 
processed = 0



# encode to b64
def encode(word):
    return base64.b64encode(word.encode('utf-8')) 

# semi-match it
def fuzzy_match(encoded, word, threshold=0.7):
    wlen = len(word)
    for i in range(len(encoded) - wlen + 1):
        chunk = encoded[i:i+wlen]
        score = SequenceMatcher(None, chunk, word).ratio()
        if score >= threshold:
            return True, score
    return False, 0

def check(word_to_check):
    global processed

    # encode
    encoded = encode(word_to_check.strip()).decode('utf-8').lower()
    encoded = encoded.translate(LEET_MAP) # allow certain chars to be same like @ -> a etc.

    # process
    for word in WORDS_TO_FIND:
        match, score = fuzzy_match(encoded, word, 0.7) 
        if match:
            with lock:
                print(word)
                found[word_to_check.strip()] = word

    # printing logic
    with lock:
        processed += 1
        if processed % 100 == 0:
            print(processed)

with open(WORDS_LIST_PATH) as f:
    lines = f.readlines()
        
print(f"LENGTH: {len(lines)}")

# threads
with ThreadPoolExecutor(max_workers=THREADS) as executor:
    executor.map(check, lines)

print(found)

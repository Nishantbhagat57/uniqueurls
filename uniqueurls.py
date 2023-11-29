import sys
import sqlite3
import urllib.parse
import tempfile
from multiprocessing import Pool, cpu_count
from rapidfuzz import fuzz
import argparse

# Create ArgumentParser instance for handling command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("url_file", type=str, help="Path to the file containing URLs.")
parser.add_argument("-debug", type=str, help="Path to the debug log file.")
parser.add_argument("-ratio", type=int, default=85, help="Ratio for string similarity checks.")

# Parse arguments
args = parser.parse_args()

# Create temporary file for SQLite database
temp_db = tempfile.NamedTemporaryFile(delete=True)

# Create/connect to SQLite database
conn = sqlite3.connect(temp_db.name)
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE urls
    (origin TEXT, path TEXT)
''')

# Read URLs from file and insert into database
with open(args.url_file, 'r') as file:
    for line in file:
        line = line.strip()
        url = urllib.parse.urlparse(line)
        origin = url.scheme + "://" + url.netloc
        c.execute('INSERT INTO urls VALUES (?, ?)', (origin, line))
        
conn.commit()

# Function to perform fuzzy matching
def fuzzy_matching(paths):
    unique_paths = []
    for p in paths:
        if not any(fuzz.ratio(p[0], u) > args.ratio for u in unique_paths):
            unique_paths.append(p[0])
        elif args.debug:
            with open(args.debug, 'a') as debug_file:
                debug_file.write(f'{p[0]}\n')
    return unique_paths

# Select all origins
c.execute('SELECT DISTINCT origin FROM urls')
origins = c.fetchall()

# Start a multiprocessing Pool
pool = Pool(processes=cpu_count())
results = []
for o in origins:
    origin = o[0]
    c.execute('SELECT path FROM urls WHERE origin = ?', (origin,))
    paths = c.fetchall()
    results.append(pool.apply_async(fuzzy_matching, [paths]))

# Get process results from the output queue
output = [p.get() for p in results]

for path in output:
    for url in path:
        print(url)

# Close the connection, at this point the temporary database will be automatically deleted
conn.close()

import sys
import sqlite3
import urllib.parse
import tempfile
from fuzzywuzzy import fuzz, process
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
        # Parse URL
        url = urllib.parse.urlparse(line.strip())
        # Get origin from netloc and scheme, SQL escape via ? placeholder
        origin = url.scheme + "://" + url.netloc
        # Ensure that path is not empty before inserting into database
        if url.path:
            c.execute('INSERT INTO urls VALUES (?, ?)', (origin, url.path))

conn.commit()

# Open debug file (if specified) for writing
debug_file = None
if args.debug:
    debug_file = open(args.debug, 'w')

# Select all origins
c.execute('SELECT DISTINCT origin FROM urls')
origins = c.fetchall()

for o in origins:
    origin = o[0]
    c.execute('SELECT path FROM urls WHERE origin = ?', (origin,))
    paths = c.fetchall()

    unique_paths = []
    for path in paths:
        # If path is not args.ratio% similar to any path in unique paths, we add to unique paths
        if not any(fuzz.ratio(path[0], u) > args.ratio for u in unique_paths):
            unique_paths.append(path[0])
        elif debug_file:
            # Write removed URL to debug file
            debug_file.write(f'{origin}{path[0]}\n')

    for path in unique_paths:
        print(f'{origin}{path}')

# Close the connection, at this point the temporary database will be automatically deleted
conn.close()

# Close debug file (if opened)
if debug_file:
    debug_file.close()

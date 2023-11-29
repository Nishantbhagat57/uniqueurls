# uniqueurls
*"uniqueurls"* is a Python-based tool used for decluttering a list of URLs by performing string similarity comparisons. It generates a list of unique URLs by comparing the similarity of path components of URLs.

It helps professionals in the realm of pentesting and bug hunting streamline their process by efficiently filtering out similar URLs from a large dataset, thus enhancing the effectiveness and productivity of their workflow.

## Getting Started

### Prerequisites

- Python 3
- Python packages: `sqlite3`, `urllib.parse`, `tempfile`, `fuzzywuzzy`, `argparse`

### Installing

1. Clone the GitHub repository:

```bash
git clone https://github.com/Nishantbhagat57/uniqueurls.git
cd uniqueurls
```

2. Install the required Python packages:

```bash
pip3 install -r requirements.txt
```

## How It Works

*uniqueurls* uses an intelligent approach to analyze URLs and deduplicate them based on string similarity:

1. URLs are read from an input text file and stored in a temporary SQLite database.

2. URLs are then split into their respective origins (domain or hostname) and paths.

3. For each origin, paths are compared with each other for similarity. If the ratio of similarity between two paths is less than a specified percentage (default is 85%), the URLs are considered unique.

4. Unique URLs are then printed out and any URL found to be similar (or duplicate) is optionally logged in a debug file for review.

## Why uniqueurls?

While there are other deduplication tools available on GitHub, *uniqueurls* stands out for the following reasons:

- Contextual Analysis: Rather than just comparing URLs as a whole, *uniqueurls* examines the path of URLs for each specific domain/hostname, ensuring a thorough and context-based review.
- Configurable Similarity Ratio: The tool allows the user to define the ratio of similarity, providing flexibility in determining how stringent the comparison should be.
- Debug Log: Removed URLs can be logged for analysis, which aids in understanding the tool's operation and ensures transparency.

## Usage

```bash
python3 uniqueurls.py [url_file] [-debug [debug_file]] [-ratio [similarity_ratio]]
```

- `url_file`: (*required*) The path to the file containing URLs to be processed.
- `-debug [debug_file]`: (*optional*) The path to the debug file where removed URLs will be logged.
- `-ratio [similarity_ratio]`: (*optional*) The ratio for string similarity checks. Default value is 85 if not specified.

### Example

Input file *urls.txt* contains:

```
http://example.com/event/4v35s
http://example.com/event/4v38q
http://example.com/event/4v3bw
http://example.com/people/AMWarren
http://example.com/people/amy082600
http://xyz.example.com/job/Chicago-(US)-JobIL60606/772758
http://xyz.example.com/job/Chicago-(US)-JobIL60611/772757
```

Command:

```bash
python3 uniqueurls.py urls.txt -debug debug.txt -ratio 90
```

Output:

```
http://example.com/event/4v35s
http://example.com/people/AMWarren
http://example.com/people/amy082600
http://xyz.example.com/job/Chicago-(US)-JobIL60606/772758
```

*debug.txt* would contain:

```
http://example.com/event/4v38q
http://example.com/event/4v3bw
http://xyz.example.com/job/Chicago-(US)-JobIL60611/772757
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

# Wiki Downloader

`download_wiki.py` is a Python script designed to download and save pages from a specified wiki. It crawls the wiki starting from a given URL, downloads the pages, and saves them locally. The script also keeps track of the pages it has visited to avoid downloading the same page multiple times.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

You can install the required libraries using pip:

```sh
pip install requests beautifulsoup4
```

## Usage

To run the script, use the following command:

```sh
python download_wiki.py <base_url> <output_dir> [<user_agent>]
```

- `<base_url>`: The base URL of the wiki to download.
- `<output_dir>`: The directory where the downloaded pages will be saved.
- `<user_agent>` (optional): The user agent string to use for the requests. Defaults to `Wiki Offline Downloader/1.0 (Educational Purpose)`.

### Example

```sh
python download_wiki.py https://example-wiki.com /path/to/output
```

## Features

- Downloads and saves wiki pages starting from the specified base URL.
- Respects the wiki's servers by adding a delay between requests.
- Keeps track of visited URLs to avoid downloading the same page multiple times.
- Saves progress to a `progress.json` file in the output directory.

## Classes and Methods

### `WikiDownloader`

#### `__init__(self, base_url, output_dir, user_agent='Wiki Offline Downloader/1.0 (Educational Purpose)')`

Initializes the `WikiDownloader` with the base URL, output directory, and user agent.

#### `download_page(self, url)`

Downloads the content of the specified URL. Returns the page content as a string.

#### `save_page(self, url, content)`

Saves the downloaded page content to a file in the output directory.

#### `get_links(self, content, current_url)`

Extracts and returns a set of links from the downloaded page content.

#### `crawl(self, start_url, delay=1)`

Crawls the wiki starting from the specified URL. Adds a delay between requests to respect the wiki's servers.

#### `save_progress(self)`

Saves the progress (visited URLs) to a `progress.json` file in the output directory.

#### `load_progress(self)`

Loads the progress (visited URLs) from the `progress.json` file in the output directory.

## License

This script is for educational purposes only. Use it responsibly and respect the terms of service of the websites you download from.
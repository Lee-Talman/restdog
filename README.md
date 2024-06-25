# restdog
Python utility that duplicates file modifications over the web via REST API, (or to a local directory) powered by [watchdog](https://github.com/gorakhargosh/watchdog).

## Usage
```ps
$python restdog.py [-h] [--api] [--interval INTERVAL] [--file_types FILE_TYPES [FILE_TYPES ...]] source dest

positional arguments:
  source               # local source directory to watch files
  dest              # local destination directory or API endpoint

options:
  -h, --help            # show this help message and exit
  --interval            # update interval in seconds (default: 1800)
  --file_types          # whitespace-separated list of watched file types (default: ".csv" ".xls" ".xlsx" ".xlsm")
```

## Example
```ps
$python restdog.py "test\source" "test\dest"
# Watches your local directory at the relative path "test\source" for .csv, .xls, .xlsx, and .xlsm file modifications,
# Sends any changes to `test\dest` every 1800 seconds.
```
### Features:
- [x] Monitoring between local directories
- [x] Monitoring over REST API endpoints
- [ ] Run restdog as a Windows Service (coming soon)

### API Requests

If a file in your directory is:
| Created... 	| Modified... 	| Deleted/Moved... 	|
|:----------:	|:-----------:	|:----------------:	|
|    POST    	|     PUT     	|      DELETE      	|

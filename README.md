# restdog
Python utility that duplicates file modifications over the web via REST API, (or to a local directory) powered by [watchdog](https://github.com/gorakhargosh/watchdog).

## Usage
You can run `restdog.py` as a standalone command-line tool:
```ps
$python restdog.py [-h] [--api] [--interval INTERVAL] [--file_types FILE_TYPES [FILE_TYPES ...]] src_dir dest_dir

positional arguments:
  src_dir               # local source directory to watch files
  dest_dir              # local destination directory or API endpoint

options:
  -h, --help            # show this help message and exit
  --api                 # send to an API endpoint (default: False)
  --interval            # update interval in seconds (default: 3600)
  --file_types          # whitespace-separated list of watched file types (default: "*.csv" "*.xls" "*.xlsx" "*.xlsm")
```
Or install it into your local environment with `pip install restdog`, then invoke the CLI from another module with the `watch()` function:

```py
import restdog

restdog.watch()
```


## Example
```ps
$python restdog.py "test\source" "http://my-website.com/my-api/my-endpoint" --api --interval 5 --file_types "*.csv" "*.xlsx" "*.txt" 
# Watches your local directory at the relative path "test\source" for .csv, .xlsx, and .txt file modifications,
# Sends any changes to "http://my-website.com/my-api/my-endpoint" every 5 seconds.
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

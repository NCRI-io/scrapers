# Scrapers

This repository is a collection of web scraping tools used for Reddit, Twitter, and Facebook.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.
### Required Packages:
pandas\
time\
json\
requests\
datetime\
pickle\
facebook_scraper\
instaloader\
snscrape\
\
Example:
```bash
pip install pandas
```

## Usage

### Importing:
```python
# Twitter
from twitter_scraper import getNamedTweets
# Reddit
from redditsubmissions_scraper import get_posts
from redditcomments_scraper import get_comments
# datetime import needed for reddit scrapers
from datetime import datetime, timezone

# Facebook
from fb_scraper import scrape_comments
from fb_scraper import scrape_posts
```

### Twitter:
```python
df = getNamedTweets(keyword = 'ncri_io', start_date = '2022-3-1', end_date = '2022-3-15')
```
### Reddit Posts:
```python
since = int(datetime(2022, 3, 1, tzinfo=timezone.utc).timestamp())
get_posts(subreddit = "worldnews", term = 'Ukraine', since = since, path = 'worldnews_ukraine.csv')
print('done')
```
### Reddit Comments:
```python
since = int(datetime(2022, 3, 1, tzinfo=timezone.utc).timestamp())
get_comments(subreddit = "worldnews", since=since, path = 'worldnews_comments.csv')
print('done')
```

### Facebook Posts:
```python
fb_list = ['Page or group name or id']
cookies = ('name of .txt file containing cookies')
posts = scrape_posts(fb_list, 100, cookies, {"comments": True, "reactors": True, "allow_extra_requests": True, 'posts_per_page': 1})
```

### Facebook Comments:
```python
fb_list = ['Page or group name or id']
cookies = ('name of .txt file containing cookies')
comments = scrape_comments(fb_list, 100, cookies, {"comments": True, "reactors": True, "allow_extra_requests": True, 'posts_per_page': 1})
```

### Example of filtering posts or comments by keyword:
For posts replace the appropriate comment variables with post variables.
```python
words_list = ['']
comments_filtered = comments[comments['comment_text'].str.contains('|'.join(words_list))]
```
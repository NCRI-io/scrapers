# Scrapers

This repository is a collection of web scraping tools used for Reddit, Twitter, and Facebook.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.
### Required Packages:
pandas\
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
from twitter_scraper import getUserTweets

# Reddit
from redditsubmissions_scraper import get_posts
from redditcomments_scraper import get_comments
from datetime import datetime, timezone

# Facebook
from fb_scraper import scrape_comments
from fb_scraper import scrape_posts
```
### Cookies:
The Facebook scraper requires cookies to be passed in as an argument. To collect cookies in chrome download this [cookies extension](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid). To collect cookies in Firefox download this [cookies extension](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/). Make sure that you include both the c_user cookie and the xs cookie, you will get an InvalidCookies exception if you don't.

### Twitter:
```python
# Get tweets based on keyword
df = getNamedTweets(keyword = 'ncri_io', start_date = '2022-3-1', end_date = '2022-3-15')
# Get tweets of account
df = getUserTweets(name = 'ncri_io')
# Loop to get a list of user accounts
def getUserTweets_list(userlist):
    x = 0
    for username in userlist:
        df = getUserTweets(name = username)
        df.to_csv(userlist[x] + ".csv")
        x+=1
userlist = ['ncri_io', 'RutgersU']
getUserTweets_list(userlist)
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

### Scihub:
Enter the name of the doi file to be scraped in the "doi" variable. Ensure the "out" variable is set to the desired location for pdfs to be downloaded. Keep the scraper frequency around 500 to prevent running into the websites CAPTCHA. 

```python
doi = open('doi_file.txt', 'r')
lines = doi.read()
doi_list = lines.splitlines()
doi.close()

i = 0
for doi in doi_list:
    paper = ("https://doi.org/" + doi)
    paper_type = "doi"
    out = ("./journals/post_colonial/critical_inquiry/")
    scihub_download(paper, paper_type=paper_type, out=out)
    i+=1
    time.sleep(10)
    if i == 501:
        break
```

import json
import requests
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timezone
from pandas import json_normalize

# Standard
from datetime import datetime, timezone

# 3rd-Party
import pandas as pd
import requests

# Pushshift Beta Constants
BASE_URL = "https://beta.pushshift.io"
DATA_SOURCE = "reddit"
API_ENDPOINT = "search/comments"

def get_comments(subreddit: str, since: int, path: str, until: int = None, term: str = None) -> pd.DataFrame():
    """Gets Reddit Posts from Pushshift's Beta API within a specific timeframe

    Args:
        subreddit (str): Name of subreddit (exclude r/)
        since: UTC integer timestamp of how far back posts were made
        until [Optiona]: UTC integer timestamp to set timeline cap for posts
        term [Optional]: Word/phrase which is contained within the reddit post

    Returns:
        [pd.DataFrame()]: Pandas Dataframe of all the aggregated results
    """
    # Default query
    query = {
        'limit': 1000,
        'order': "desc",
        'since': since, 
        'sort': "id",
        'subreddit': subreddit, 
        'track_total_hits': True,         
    }

    
    # Append to query if provided
    if until is not None:
        query['until'] = until

    if term is not None:
        query['q'] = term

    # Get initial data from request
    response = requests.get(f'{BASE_URL}/{DATA_SOURCE}/{API_ENDPOINT}', params = query).json()
    total_num_hits = response['metadata']['es']['hits']['total']['value']
    print(f"Total Number of Posts Returned from API: {total_num_hits}")
    posts = response['data']
    posts = [{'author_flair_richtext': post.get('author_flair_richtext'), 
              'controversiality': post.get('controversiality'), 
              'body': post.get('body').replace('\n', ' '), 
              'total_awards_received': post.get('total_awards_received'), 
              'subreddit_id': post.get('subreddit_id'), 
              'subreddit': post.get('subreddit'), 
              'link_id': post.get('link_id'), 
              'score': post.get('score'), 
              'is_submitter': post.get('is_submitter'), 
              'can_gild': post.get('can_gild'), 
              'id': post.get('id'), 
              'author_premium': post.get('author_premium'), 
              'locked': post.get('locked'), 
              'created_utc': post.get('created_utc'), 
              'edited': post.get('edited'), 
              'author': post.get('author'), 
              'treatment_tags': post.get('treatment_tags'), 
              'author_flair_background_color': post.get('author_flair_background_color'), 
              'body_sha1': post.get('body_sha1'), 
              'updated_utc': post.get('updated_utc'), 
              'score_hidden': post.get('score_hidden'), 
              'subreddit_name_prefixed': post.get('subreddit_name_prefixed'), 
              'parent_id': post.get('parent_id'), 
              'top_awarded_type': post.get('top_awarded_type'), 
              'no_follow': post.get('no_follow'), 
              'author_flair_type': post.get('author_flair_type'), 
              'permalink': post.get('permalink'), 
              'author_flair_css_class': post.get('author_flair_css_class'), 
              'unrepliable_reason': post.get('unrepliable_reason'), 
              'gilded': post.get('gilded'), 
              'author_patreon_flair': post.get('author_patreon_flair'), 
              'collapsed': post.get('collapsed'), 
              'collapsed_reason': post.get('collapsed_reason'), 
              'send_replies': post.get('send_replies'), 
              'author_flair_text': post.get('author_flair_text'), 
              'archived': post.get('archived'), 
              'collapsed_reason_code': post.get('collapsed_reason_code'), 
              'author_flair_text_color': post.get('author_flair_text_color'), 
              'retrieved_utc': post.get('retrieved_utc'), 
              'author_fullname': post.get('author_fullname'), 
              'subreddit_type': post.get('subreddit_type'), 
              'associated_award': post.get('associated_award'), 
              'distinguished': post.get('distinguished'), 
              'author_flair_template_id': post.get('author_flair_template_id'), 
              'stickied': post.get('stickied'), 
              'all_awardings': post.get('all_awardings'), 
              'author_is_blocked': post.get('author_is_blocked'), 
              'comment_type': post.get('comment_type'), 
              'collapsed_because_crowd_control': post.get('collapsed_because_crowd_control'), 
              'id_str': post.get('id_str'), 
              'utc_datetime_str': post.get('utc_datetime_str')}
             for post in posts
            ]
    posts_so_far = len(posts)
    df = json_normalize(posts)
    df.to_csv(path, index=False)
    
    
    # Pagination to grab the remaining data
    while posts_so_far < total_num_hits:
        query['max_id'] = (posts[-1]['id']) - 1
        new_response = requests.get(f'{BASE_URL}/{DATA_SOURCE}/{API_ENDPOINT}', params = query).json()
        new_posts = new_response['data']
        posts = [{'author_flair_richtext': post.get('author_flair_richtext'), 
              'controversiality': post.get('controversiality'), 
              'body': post.get('body').replace('\n', ' '), 
              'total_awards_received': post.get('total_awards_received'), 
              'subreddit_id': post.get('subreddit_id'), 
              'subreddit': post.get('subreddit'), 
              'link_id': post.get('link_id'), 
              'score': post.get('score'), 
              'is_submitter': post.get('is_submitter'), 
              'can_gild': post.get('can_gild'), 
              'id': post.get('id'), 
              'author_premium': post.get('author_premium'), 
              'locked': post.get('locked'), 
              'created_utc': post.get('created_utc'), 
              'edited': post.get('edited'), 
              'author': post.get('author'), 
              'treatment_tags': post.get('treatment_tags'), 
              'author_flair_background_color': post.get('author_flair_background_color'), 
              'body_sha1': post.get('body_sha1'), 
              'updated_utc': post.get('updated_utc'), 
              'score_hidden': post.get('score_hidden'), 
              'subreddit_name_prefixed': post.get('subreddit_name_prefixed'), 
              'parent_id': post.get('parent_id'), 
              'top_awarded_type': post.get('top_awarded_type'), 
              'no_follow': post.get('no_follow'), 
              'author_flair_type': post.get('author_flair_type'), 
              'permalink': post.get('permalink'), 
              'author_flair_css_class': post.get('author_flair_css_class'), 
              'unrepliable_reason': post.get('unrepliable_reason'), 
              'gilded': post.get('gilded'), 
              'author_patreon_flair': post.get('author_patreon_flair'), 
              'collapsed': post.get('collapsed'), 
              'collapsed_reason': post.get('collapsed_reason'), 
              'send_replies': post.get('send_replies'), 
              'author_flair_text': post.get('author_flair_text'), 
              'archived': post.get('archived'), 
              'collapsed_reason_code': post.get('collapsed_reason_code'), 
              'author_flair_text_color': post.get('author_flair_text_color'), 
              'retrieved_utc': post.get('retrieved_utc'), 
              'author_fullname': post.get('author_fullname'), 
              'subreddit_type': post.get('subreddit_type'), 
              'associated_award': post.get('associated_award'), 
              'distinguished': post.get('distinguished'), 
              'author_flair_template_id': post.get('author_flair_template_id'), 
              'stickied': post.get('stickied'), 
              'all_awardings': post.get('all_awardings'), 
              'author_is_blocked': post.get('author_is_blocked'), 
              'comment_type': post.get('comment_type'), 
              'collapsed_because_crowd_control': post.get('collapsed_because_crowd_control'), 
              'id_str': post.get('id_str'), 
              'utc_datetime_str': post.get('utc_datetime_str')}
             for post in new_posts
        ]
        df = json_normalize(new_posts)
        df.to_csv(path, mode='a', index=False, header=False)
        posts_so_far += len(new_posts)
        if posts_so_far%100000 == 0:
            print(posts_so_far)
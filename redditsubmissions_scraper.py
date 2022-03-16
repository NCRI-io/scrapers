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
API_ENDPOINT = "search/submissions"

def get_posts(subreddit: str, since: int, path: str, until: int = None, term: str = None):
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
    posts = [{'link_flair_richtext': post.get('link_flair_richtext'), 
              'link_flair_background_color': post.get('link_flair_background_color'), 
              'author_flair_richtext': post.get('author_flair_richtext'), 
              'over_18': post.get('over_18'), 
              'hide_score': post.get('hide_score'), 
              'total_awards_received': post.get('total_awards_received'), 
              'subreddit': post.get('subreddit'), 
              'subreddit_id': post.get('subreddit_id'), 
              'score': post.get('score'), 
              'suggested_sort': post.get('suggested_sort'), 
              'num_comments': post.get('num_comments'), 
              'whitelist_status': post.get('whitelist_status'), 
              'removed_by': post.get('removed_by'), 
              'author_created_delta': post.get('author_created_delta'), 
              'can_gild': post.get('can_gild'), 
              'is_robot_indexable': post.get('is_robot_indexable'), 
              'is_created_from_ads_ui': post.get('is_created_from_ads_ui'), 
              'spoiler': post.get('spoiler'), 
              'author_premium': post.get('author_premium'), 
              'post_hint': post.get('post_hint'), 
              'id': post.get('id'), 
              'locked': post.get('locked'), 
              'created_utc': post.get('created_utc'), 
              'link_flair_template_id': post.get('link_flair_template_id'), 
              'thumbnail': post.get('thumbnail'), 
              'discussion_type': post.get('discussion_type'), 
              'edited': post.get('edited'), 
              'allow_live_comments': post.get('allow_live_comments'), 
              'author': post.get('author'), 
              'treatment_tags': post.get('treatment_tags'), 
              'author_flair_background_color': post.get('author_flair_background_color'), 
              'link_flair_text_color': post.get('link_flair_text_color'), 
              'updated_utc': post.get('updated_utc'), 
              'is_video': post.get('is_video'), 
              'is_original_content': post.get('is_original_content'), 
              'subreddit_name_prefixed': post.get('subreddit_name_prefixed'), 
              'top_awarded_type': post.get('top_awarded_type'), 
              'domain': post.get('domain'), 
              'no_follow': post.get('no_follow'), 
              'author_flair_type': post.get('author_flair_type'), 
              'awarders': post.get('awarders'), 
              'media_only': post.get('media_only'), 
              'permalink': post.get('permalink'), 
              'content_categories': post.get('content_categories'), 
              'wls': post.get('wls'), 
              'author_flair_css_class': post.get('author_flair_css_class'), 
              'pinned': post.get('pinned'), 
              'gilded': post.get('gilded'), 
              'hidden': post.get('hidden'), 
              'author_patreon_flair': post.get('author_patreon_flair'), 
              'title': post.get('title'), 
              'author_flair_text': post.get('author_flair_text'), 
              'send_replies': post.get('send_replies'), 
              'archived': post.get('archived'), 
              'author_flair_text_color': post.get('author_flair_text_color'), 
              'num_crossposts': post.get('num_crossposts'), 
              'thumbnail_width': post.get('thumbnail_width'), 
              'is_self': post.get('is_self'), 
              'retrieved_utc': post.get('retrieved_utc'), 
              'author_fullname': post.get('author_fullname'), 
              'link_flair_css_class': post.get('link_flair_css_class'), 
              'selftext': post.get('selftext').replace('\n', ' '), 
              'upvote_ratio': post.get('upvote_ratio'), 
              'link_flair_text': post.get('link_flair_text'), 
              'subreddit_type': post.get('subreddit_type'), 
              'is_meta': post.get('is_meta'), 
              'is_crosspostable': post.get('is_crosspostable'), 
              'subreddit_subscribers': post.get('subreddit_subscribers'), 
              'distinguished': post.get('distinguished'), 
              'author_flair_template_id': post.get('author_flair_template_id'), 
              'removed_by_category': post.get('removed_by_category'), 
              'url': post.get('url'), 
              'thumbnail_height': post.get('thumbnail_height'), 
              'parent_whitelist_status': post.get('parent_whitelist_status'), 
              'stickied': post.get('stickied'), 
              'link_flair_type': post.get('link_flair_type'), 
              'all_awardings': post.get('all_awardings'), 
              'pwls': post.get('pwls'), 
              'quarantine': post.get('quarantine'), 
              'category': post.get('category'), 
              'view_count': post.get('view_count'), 
              'contest_mode': post.get('view_count'), 
              'is_reddit_media_domain': post.get('is_reddit_media_domain'), 
              'author_created_utc': post.get('author_created_utc'), 
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
        posts = [{'link_flair_richtext': post.get('link_flair_richtext'), 
              'link_flair_background_color': post.get('link_flair_background_color'), 
              'author_flair_richtext': post.get('author_flair_richtext'), 
              'over_18': post.get('over_18'), 
              'hide_score': post.get('hide_score'), 
              'total_awards_received': post.get('total_awards_received'), 
              'subreddit': post.get('subreddit'), 
              'subreddit_id': post.get('subreddit_id'), 
              'score': post.get('score'), 
              'suggested_sort': post.get('suggested_sort'), 
              'num_comments': post.get('num_comments'), 
              'whitelist_status': post.get('whitelist_status'), 
              'removed_by': post.get('removed_by'), 
              'author_created_delta': post.get('author_created_delta'), 
              'can_gild': post.get('can_gild'), 
              'is_robot_indexable': post.get('is_robot_indexable'), 
              'is_created_from_ads_ui': post.get('is_created_from_ads_ui'), 
              'spoiler': post.get('spoiler'), 
              'author_premium': post.get('author_premium'), 
              'post_hint': post.get('post_hint'), 
              'id': post.get('id'), 
              'locked': post.get('locked'), 
              'created_utc': post.get('created_utc'), 
              'link_flair_template_id': post.get('link_flair_template_id'), 
              'thumbnail': post.get('thumbnail'), 
              'discussion_type': post.get('discussion_type'), 
              'edited': post.get('edited'), 
              'allow_live_comments': post.get('allow_live_comments'), 
              'author': post.get('author'), 
              'treatment_tags': post.get('treatment_tags'), 
              'author_flair_background_color': post.get('author_flair_background_color'), 
              'link_flair_text_color': post.get('link_flair_text_color'), 
              'updated_utc': post.get('updated_utc'), 
              'is_video': post.get('is_video'), 
              'is_original_content': post.get('is_original_content'), 
              'subreddit_name_prefixed': post.get('subreddit_name_prefixed'), 
              'top_awarded_type': post.get('top_awarded_type'), 
              'domain': post.get('domain'), 
              'no_follow': post.get('no_follow'), 
              'author_flair_type': post.get('author_flair_type'), 
              'awarders': post.get('awarders'), 
              'media_only': post.get('media_only'), 
              'permalink': post.get('permalink'), 
              'content_categories': post.get('content_categories'), 
              'wls': post.get('wls'), 
              'author_flair_css_class': post.get('author_flair_css_class'), 
              'pinned': post.get('pinned'), 
              'gilded': post.get('gilded'), 
              'hidden': post.get('hidden'), 
              'author_patreon_flair': post.get('author_patreon_flair'), 
              'title': post.get('title'), 
              'author_flair_text': post.get('author_flair_text'), 
              'send_replies': post.get('send_replies'), 
              'archived': post.get('archived'), 
              'author_flair_text_color': post.get('author_flair_text_color'), 
              'num_crossposts': post.get('num_crossposts'), 
              'thumbnail_width': post.get('thumbnail_width'), 
              'is_self': post.get('is_self'), 
              'retrieved_utc': post.get('retrieved_utc'), 
              'author_fullname': post.get('author_fullname'), 
              'link_flair_css_class': post.get('link_flair_css_class'), 
              'selftext': post.get('selftext').replace('\n', ' '), 
              'upvote_ratio': post.get('upvote_ratio'), 
              'link_flair_text': post.get('link_flair_text'), 
              'subreddit_type': post.get('subreddit_type'), 
              'is_meta': post.get('is_meta'), 
              'is_crosspostable': post.get('is_crosspostable'), 
              'subreddit_subscribers': post.get('subreddit_subscribers'), 
              'distinguished': post.get('distinguished'), 
              'author_flair_template_id': post.get('author_flair_template_id'), 
              'removed_by_category': post.get('removed_by_category'), 
              'url': post.get('url'), 
              'thumbnail_height': post.get('thumbnail_height'), 
              'parent_whitelist_status': post.get('parent_whitelist_status'), 
              'stickied': post.get('stickied'), 
              'link_flair_type': post.get('link_flair_type'), 
              'all_awardings': post.get('all_awardings'), 
              'pwls': post.get('pwls'), 
              'quarantine': post.get('quarantine'), 
              'category': post.get('category'), 
              'view_count': post.get('view_count'), 
              'contest_mode': post.get('view_count'), 
              'is_reddit_media_domain': post.get('is_reddit_media_domain'), 
              'author_created_utc': post.get('author_created_utc'), 
              'id_str': post.get('id_str'), 
              'utc_datetime_str': post.get('utc_datetime_str')}
             for post in new_posts
            ]
        df = json_normalize(posts)
        df.to_csv(path, mode='a', index=False, header=False)
        posts_so_far += len(new_posts)
        if posts_so_far%100000 == 0:
            print(posts_so_far)

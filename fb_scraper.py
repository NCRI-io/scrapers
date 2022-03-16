from facebook_scraper import get_posts
import pandas as pd

def scrape_comments(fb_group_list, pages, cookies_file, options):
    """
    Made this dataframe based on: https://github.com/kevinzg/facebook-scraper
    
    Args:
        fb_group_list(str, list): a list of Facebook pages to scrape, must be public
        pages(int): number of pages to collect
        cookies_file(str): file location of cookies data
        options(dict): dictionary of options for collection, dictionary options can be found in the link above
        
    Returns:
        DataFrame: a DataFrame containing comments and associated information from posts scraped. Posts scraped are gathered from 'fb_group_list' posts that 
                   that contain words inputted in 'words_list'
    """
    # If content in the 'comment_text' column is the commenters name it is most likely because they commented with just a picture and no text
    post_list = []
    df_comments = pd.DataFrame()
    for fb_group in fb_group_list:
        for post in get_posts(fb_group, pages = pages, cookies = cookies_file, options = options):
            post['text'] = post['text'].split('\n',1)[0]
            comments_list = []
            replies_list = []
            
            print(post['text']+'\n')
            post_list.append(post)
            x = 0
                
            while x < len(post_list):
                comments_list = post_list[x]['comments_full']
                x+=1

                if comments_list != []:
                    i = 0
                    comment_text = comments_list[i]['comment_text']

                    for comment in comment_text:
                        while i < len(comments_list):
                            comments_list[i]['comment_text'] = comments_list[i]['comment_text'].split('\n',1)[0]
                            replies_list = comments_list[i]['replies']
                            i+=1

                            if replies_list != []:
                                z = 0

                                while z < len(replies_list):
                                    replies_list[z]['comment_text'] = replies_list[z]['comment_text'].split('\n',1)[0]
                                    z+=1
            df_comments = df_comments.append(comments_list)
    print('Done')
    return df_comments

# Only collects posts
def scrape_posts(fb_group_list, pages, cookies_file, options):
    post_list = []
    df_posts = pd.DataFrame()
    for fb_group in fb_group_list:
        for post in get_posts(fb_group, pages = pages, cookies = cookies_file, options = options):
            post['text'] = post['text'].split('\n',1)[0]
            print(post['text']+'\n')
            post_list.append(post)
        df_posts = df_posts.append(post_list)
    return df_posts
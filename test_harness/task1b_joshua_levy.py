import pandas as pd
import requests 
import time
import re

#### PART 1: Collect links to all articles ####
# Read in task1a results to get links to each issue-page

task1a_df = pd.read_csv('test_harness/task1a_joshua_levy.csv')

# TODO: REMOVE THIS SUBSET TOOL
task1a_df = task1a_df.head(5)

master_df = task1a_df.copy()
master_df['article_temp_link'] = 'a'
master_df['article_temp_link'] = master_df['article_temp_link'].astype('object')

running_article_count = 0
for index, issue in task1a_df.iterrows():
    issue_link = issue.link
    issue_desc = issue.issue_date

    issue_response = requests.get(
        url = issue_link
    )
    issue_page_html = issue_response.content.decode('utf-8')

    article_block_pattern = r'<article (.+?)</article>'
    article_block_list = re.findall(
        article_block_pattern,
        issue_page_html,
        re.DOTALL
    )

    articles_for_issue = len(article_block_list)
    running_article_count += articles_for_issue
    print("Articles for issue ({}): {}".format(issue_desc, articles_for_issue))

    article_link_pattern = r'<a href=\"(.+)\"'

    article_temp_link_list = []
    for article_block in article_block_list:
        link = re.search(article_link_pattern, article_block)[1]
        pretty_temp_link = 'https://www.aeaweb.org{}'.format(link)
        article_temp_link_list.append(pretty_temp_link)

    master_df.at[index, 'article_temp_link'] = article_temp_link_list

print("MAX number of expected article-observations: {}".format(running_article_count))

master_df = master_df.explode('article_temp_link')
master_df.reset_index(drop=True, inplace=True)
master_df


master_df['article_title'] = 'xxx'
master_df['page_numbers'] = 'xxx'
master_df['article_link'] = 'xxx'
master_df['jel_code'] = 'xxx'
master_df['jel_desc'] = 'xxx'

master_df['jel_code'] = master_df['jel_code'].astype('object')
master_df['jel_desc'] = master_df['jel_desc'].astype('object')

#### PART 2: Collecting article level-data
def title_gen(match_text: str):
    title_pattern = r'<h1 class=\"title\">(.+?)</h1>'
    title = re.search(title_pattern, match_text)[1]
    return title

def authors_gen(match_text: str):

    return


for index, article in master_df.iterrows():
    article_page_link = article.article_temp_link

    article_response = requests.get(
        url = article_page_link,
    )
    article_page_html = article_response.content.decode('utf-8')

    title_gen(article_page_html)





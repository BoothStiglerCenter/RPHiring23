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
master_df['authors'] = 'xxx'
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
    author_pattern = r'<li class=\'author\'(.+?)>(.+?)\s+(.+?)(\s+?)</li>'
    author_element_match_list = re.findall(
        author_pattern,
        match_text,
        re.DOTALL
    )
    author_list = [element[2] for element in author_element_match_list]
    author_pretty_string = '; '.join(author_list)
    print(author_pretty_string)
    return author_pretty_string

def pages_gen(match_text: str):
    pages_pattern = r'\((pp\. .+?)\)'
    pages_string = re.search(pages_pattern, match_text)[1]
    print(pages_string)
    return pages_string

def doi_link_gen(match_text: str):
    doi_pattern = r'<span class=\"doi\">DOI: (.+?)</span>'
    doi = re.search(doi_pattern, match_text)[1]
    pretty_doi_link = 'https://doi.org/{}'.format(doi)
    print(pretty_doi_link)
    return pretty_doi_link

def jel_generator(match_text: str):
    jel_section_pattern = r'<ul class=\'jel-codes\'>(.+?)</ul>'
    jel_section_string = re.search(jel_section_pattern,
        match_text,
        re.DOTALL
    )

    if jel_section_string is None:
        print("NO JEL CODES")
        return None, None

    code_desc_pattern = r'<strong class=\'code\'>(.+?)</strong>\n\s+(.+?)\n'
    code_desc_element_match_list = re.findall(
        code_desc_pattern,
        jel_section_string[1],
        re.DOTALL
    )

    jel_codes_list = []
    jel_descs_list = []
    for element in code_desc_element_match_list:
        jel_code = element[0]
        jel_desc = element[1]
        jel_codes_list.append(jel_code)
        jel_descs_list.append(jel_desc)

    if len(jel_codes_list) != len(jel_descs_list):
        raise ValueError("JEL Codes and Descriptions aren't properly matching")

    print(jel_codes_list)
    print(jel_descs_list)
    return jel_codes_list, jel_descs_list


for index, article in master_df.iterrows():
    article_page_link = article.article_temp_link

    article_response = requests.get(
        url = article_page_link,
    )
    article_page_html = article_response.content.decode('utf-8')

    master_df.loc[index, 'article_title'] = title_gen(article_page_html)

    master_df.loc[index, 'authors'] = authors_gen(article_page_html)

    master_df.loc[index, 'page_numbers'] = pages_gen(article_page_html)   

    master_df.loc[index, 'article_link'] = doi_link_gen(article_page_html)

    master_df.at[index, 'jel_code'], master_df.at[index, 'jel_desc'] = jel_generator(article_page_html)
    time.sleep(0.1)





#### PART 3: REFORMAT MASTER_DF ####
### Prepare the master_df to conform to requirements/task specifications
out_df = master_df.explode(['jel_code', 'jel_desc'])
out_df = out_df[['volume', 'issue_date', 'article_title', 'authors', 'page_numbers', 'article_link', 'jel_code', 'jel_description']]


#### PART 4: REMOVING NON-OBSERVATIONS ####




out_df.to_csv('task1b_joshua_levy.csv', index=False, encoding='utf-8')

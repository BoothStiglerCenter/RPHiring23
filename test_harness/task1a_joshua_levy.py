import pandas as pd
import requests
import time
import re


aer_issues_url = 'https://www.aeaweb.org/journals/aer/issues'

response = requests.get(
    url = aer_issues_url
)

page_html = response.content.decode('utf-8')

link_pattern = r'(<a href=\'/issues/\d+\'.+</a>)'
link_text_list = re.findall(
    link_pattern,
    page_html
)

####
def issue_link_gen(match_text: str):
    link_extension = re.search(r'/issues/\d+', match_text)[0]
    pretty_link = 'https://www.aeaweb.org{}'.format(link_extension)
    return pretty_link


def volume_gen(match_text: str):
    volume_number = re.search(r'Vol\. (\d+),', match_text)[1]
    pretty_volume_str = "Volume {}".format(volume_number)
    return pretty_volume_str


def issue_date_gen(match_text: str): 
    pretty_issue_date_str = re.search(r'>(.+)<', match_text)[1]
    return pretty_issue_date_str


processed_dict_list = []
for match in link_text_list:
    obs_dict = {}
    obs_dict['volume'] = volume_gen(match)
    obs_dict['link'] = issue_link_gen(match)
    obs_dict['issue_date'] = issue_date_gen(match)
    processed_dict_list.append(obs_dict)
    

out_df = pd.DataFrame.from_dict(processed_dict_list)
out_df.to_csv('task1a_joshua_levy.csv', index=False, encoding='utf-8')
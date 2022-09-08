import pandas as pd
import requests
import time
import re



#### PART 1: Get the issues-page ####
### This page contains all the information of interest so we
### shouldn't have to go elsewhere, even if we have to do a
### little processing on that information

aer_issues_url = 'https://www.aeaweb.org/journals/aer/issues'
response = requests.get(
    url = aer_issues_url
)

# Convert response to a string
page_html = response.content.decode('utf-8')


# This regex pattern should extract all of the necessary info
# which can be processed. All such observations are stored as 
# strings inside a list
# Example match observation: 
# "<a href='/issues/685'>July 2022 (Vol. 112, No.7 )</a>"

link_pattern = r'(<a href=\'/issues/\d+\'.+</a>)'
link_text_list = re.findall(
    link_pattern,
    page_html
)

#### PART 2: Process that information ####
def issue_link_gen(match_text: str):
    ''' 
    Converts the html match element to a pretty AEA link:
    '''
    link_extension = re.search(r'/issues/\d+', match_text)[0]
    pretty_link = 'https://www.aeaweb.org{}'.format(link_extension)
    return pretty_link

def volume_gen(match_text: str):
    '''
    Converts the html match element to a required-format Volume number
    '''
    volume_number = re.search(r'Vol\. (\d+),', match_text)[1]
    pretty_volume_str = "Volume {}".format(volume_number)
    return pretty_volume_str

def issue_date_gen(match_text: str): 
    '''
    Just extracts the issue data from the match text because it already exists
    '''
    pretty_issue_date_str = re.search(r'>(.+)<', match_text)[1]
    return pretty_issue_date_str

# For each matched html element in the list, process it for the required information.
# Store processed information in a list of dictionaries
processed_dict_list = []
for match in link_text_list:
    obs_dict = {}
    obs_dict['volume'] = volume_gen(match)
    obs_dict['link'] = issue_link_gen(match)
    obs_dict['issue_date'] = issue_date_gen(match)
    processed_dict_list.append(obs_dict)
    

#### PART 3: DataFrame time ####
# Convert the list of dictionaries to a DataFrame
# Output that DataFrame as required.
out_df = pd.DataFrame.from_dict(processed_dict_list)
out_df.to_csv('test_harness/task1a_joshua_levy.csv', index=False, encoding='utf-8')
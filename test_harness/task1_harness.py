import os
import pandas as pd


task_status_df = pd.read_csv('asdf')
task_scores_df = pd.read_csv('qwer')

task1a_answer_key_df = pd.read_csv('1243')
task1b_answer_key_df = pd.read_csv('5678')

### First, identify if there are any new tasks to be scored.
def candidates_to_score(status_df: pd.DataFrame) -> pd.DataFrame:
    to_score_df = status_df.copy()
    to_score_df = to_score_df[to_score_df.task1a == 2 | to_score_df.task1b == 2]

    return to_score_df

def col_check(taskname: str, answer_cols: set, submission_cols: set) -> float:
    """
    This function ensure that all of the columns are present and that they are properly named. It checks for the number of columns, the column names, and the casing of those columns.

    :param taskname: A string: one of 'task1a' or 'task1b'
    :param answer_cols: A set of column names (strings) that is, in effect, the answer key. There is a strong preference for this do be a globally defined, fixed variable.
    :param submission_cols: A set of column names (strings). This set is compared against `answer_key`
    :return: A float that is the columns sub-score.
    """

    answer_cols_count = 




def score_task1a(firstname: str, lastname: str) -> dict:
    """"
    This function identifies a submitted .csv based on the the passed first and last names, and returns a dictionary of sub-scores for Task 1a

    :param firstname: A lowercase string
    :param lastname: A lowercase string
    :return: A dictionary of sub-scores 
    """

    task1a_sub_scores = {
        'task1a_cols': 0,
        'task1a_obs_count': 0,
        'task1a_sample_check': 0,
    }

    ### Identify the submission (create_path)
    task1a_csv_path = 'FOLDERX/FOLDERY/{firstname}_{lastname}/task1a/task1a_{firstname}_{lastname}.csv'.format(
        firstname = firstname,
        lastname = lastname
    )
    task1a_submitted_df = pd.read_csv(task1a_csv_path)

    ###
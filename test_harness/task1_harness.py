import os
import pandas as pd

random_state_seed = 987654321
task_status_df = pd.read_csv('asdf')
task_scores_df = pd.read_csv('qwer')

task1a_answer_key_df = pd.read_csv('1243')
task1b_answer_key_df = pd.read_csv('5678')
task1b_misc_df = pd.read_csv('9012')

### First, identify if there are any new tasks to be scored.
def candidates_to_score(status_df: pd.DataFrame) -> pd.DataFrame:
    to_score_df = status_df.copy()
    to_score_df = to_score_df[to_score_df.task1a == 2 | to_score_df.task1b == 2]

    return to_score_df.iterrows()

def update_score_status(status_df: pd.DataFrame, candidate_name: str):
    updated_status_df = status_df.copy()

    updated_status_df.loc[updated_status_df.candidate_name == candidate_name, 'task1a'] = 3
    updated_status_df.loc[updated_status_df.candidate_name == candidate_name, 'task1b'] = 3

    updated_status_df.to_csv('asdf', index=False, encoding='utf-8')

    return


### Scoring functions
def col_check(taskname: str, answer_cols: set, submission_cols: set) -> float:
    """
    This function ensures that all of the columns are present and that they are properly named. It checks for the number of columns, the column names, and the casing of those columns. Tha maximum column sub-score is 5.

    :param taskname: A string: one of 'task1a' or 'task1b'
    :param answer_cols: A set of column names (strings) that is, in effect, the answer key. There is a strong preference for this do be a globally defined, fixed variable.
    :param submission_cols: A set of column names (strings). This set is compared against `answer_key`
    :return: A float that is the columns sub-score.
    """
    score = 0


    # The sets are identical. Perfect score
    if answer_cols == submission_cols:
        score = 5
        print('\t{} column check score: {}/5'.format(taskname, score))
        return score

    # Otherwise we check each of the components and apply penalties accordingly
    answer_cols_count = len(answer_cols)
    submission_cols_count = len(submission_cols)

    lowercase_submission_cols_list = [col.lower() for col in submission_cols]
    lowercase_submission_cols_set = set(lowercase_submission_cols_list)

    # There was only a casing issue on the columns (-10%)
    if answer_cols == lowercase_submission_cols_set:
        score = 5 * 0.9
        print('\t{} column check score: {}/5'.format(taskname, score))
        return score

    # This is the count of perfectly correct columns (full points for these)
    correct_cols = answer_cols.intersection(submission_cols)
    correct_cols_count = len(correct_cols)

    # This is the count of correct columns once lowered (-10% for these)
    lowered_correct_cols = answer_cols.intersection(lowercase_submission_cols_list)
    lowered_correct_cols_count = answer_cols.intersection(lowered_correct_cols)


    # Maximum score is reduced to (base * n/answer_cols_count) where n is the number of case-insensitive columns submitted. Note that to get to this point, by definition n < answer_cols_count 
    new_max_score = 5 * (lowered_correct_cols_count / answer_cols_count)
    
    incorrect_case_count = lowered_correct_cols_count - correct_cols_count
    incorrect_case_count_penalty = (new_max_score / lowered_correct_cols_count) * (incorrect_case_count * 0.1) 


    score = new_max_score - incorrect_case_count_penalty

    print('\t{} column check score: {}/5'.format(taskname, score))
    return score

def df_length_check(taskname: str, answer_df: pd.DataFrame, submission_df: pd.DataFrame) -> float:
    """
    This function identifies the lengths of the submitted .csv to check if all observations have been collected or if there has been duplicate/excess collection. The maximum length-check score is 5. 

    :param taskname: A string: one of 'task1a' or 'task1b'
    :param answer_df: A data frame. In effect we are just checking for a number.
    :param submission_df: A datafarme. In effect we are just checking for a number.
    :return: A float that is the columns sub-score.
    """
    
    answer_df_obs = len(answer_df)
    submission_df_obs = len(submission_df)

    # The length of the two data frames is identical (at this point we assume that they are, by definition identical data frames. More tests to come)
    if answer_df_obs == submission_df_obs:
        score = 5
        print('\t{} DF-length check score: {}/5'.format(taskname, score))
        return score

    # Some observations are missing: If n% of observations are missing then the score is 5 * (1-n)
    if answer_df_obs > submission_df_obs:
        score = 5 * (submission_df_obs / answer_df_obs)
        print('\t{} DF-length check score: {}/5'.format(taskname, score))
        return score

    # There has been some amount of inclusion or duplication. If the absolute difference in the count of observations is n% then the maximum score is 5 * (1-n). If the difference is greater than 100% of the true number of observations (ie 1-n < 0 ) return a score of 0.
    if answer_df_obs < submission_df_obs:
        score = 5 * (1 - (submission_df_obs / answer_df_obs))
        print('\t{} DF-length check score: {}/5'.format(taskname, score))
        return score
        
    return

def df_sample_check(taskname: str, answer_sample: pd.DataFrame, submission_df: pd.DataFrame) -> float:
    """
    This function compares a random sample of the answer key data and checks to see if all of those observations are in the submitted df. The maximum sample-check score is 5.

    :param taskname: A string: one of 'task1a' or 'task1b'
    :param answer_sample: A data frame. This is a random sample of the answer sheet. Note that this dataframe should be constant for every run so a there should be a globally defined "seed" that is used to identically identify this random sample for every submission.
    :param submission_df: A data frame. This is a complete submission data frame. 
    :return: A float that is the sample sub-score.
    """

    # We need to drop any duplicates to ensure that the set logic we use works properly 
    submission_unique_df = submission_df.drop_duplicates()

    sample_size = len(answer_sample)
    matches = 0
    for index, obs in answer_sample.iterrows():
        
        # We check if there exists a row for which all of the columns are "True" (i.e. there is a match for every value contained in `obs`)
        # Tests every cell to see if it matches *something* in list(obs) and returns a df filled with values "True" and "False".
        # df.all(axis='columns') checks to make sure that every column in a row contains "True"
        # search_result is a pd.Series that is as long as submission_df (same number of rows) containing values "True" or "False" depending on the result of df.all() for that row. 
        search_result = submission_df.isin(list(obs)).all(axis='columns')     
        
        if True in search_result.unique():
            matches += 1
        else: 
            continue
    
    score = 5 * (matches / sample_size) 

    print('\t{} sample check score: {}/5'.format(taskname, score))
    return score

def df_misc_check(misc_sample: dict, submission_df: pd.DataFrame) -> float:
    """
    This function checks to see if 5 different kinds of miscellaneous (non-scholarly) observations are in the data frame. The maximum score is 5.

    :param misc_sample: A dictionary. This should contain column names and types of miscellaneous observations that should *not* appear in those columns.
    :param submission_df: A data frame. This is a complete submission data frame. 
    :return: A float that is the miscellaneous sub-score.
    """

    penalty = 0
    for column in misc_sample.keys():
        misc_value = misc_sample.get(column)
        test_df = submission_df[submission_df[column]== misc_value]
        if len(test_df) > 0:
            penalty += 1

    score = 5 - penalty
    return score

# Score structuring functions
def score_task1a(firstname: str, lastname: str) -> dict:
    """"
    This function identifies a submitted .csv based on the the passed first and last names, and returns a dictionary of sub-scores for Task 1a

    :param firstname: A lowercase string
    :param lastname: A lowercase string
    :return: A dictionary of sub-scores 
    """

    task1a_sub_scores = {
        'task1a_cols' : 0,
        'task1a_obs_count' : 0,
        'task1a_sample_check' : 0,
        'task1a_TOTAL' : 0
    }

    ### Identify the submission (create_path)
    task1a_csv_path = 'FOLDERX/FOLDERY/{firstname}_{lastname}/task1a/task1a_{firstname}_{lastname}.csv'.format(
        firstname = firstname,
        lastname = lastname
    )
    task1a_submitted_df = pd.read_csv(task1a_csv_path)


    # SCORING FUNCTIONS CALLED
    task1a_sub_scores['task1a_cols'] = col_check(
        taskname = 'Task 1a',
        answer_cols = set(list(task1a_answer_key_df.columns)),
        submission_cols = set(list(task1a_submitted_df.columns))
    )

    task1a_sub_scores['task1a_obs_count'] = df_length_check(
        taskname = 'Task 1a',
        answer_df = task1a_answer_key_df,
        submission_df = task1a_submitted_df,
    )

    task1a_sub_scores['task1a_sample_check'] = df_length_check(
        taskname = 'Task 1a',
        answer_sample = task1a_answer_key_df.sample(n=100, random_state=random_state_seed),
        submission_df = task1a_submitted_df
    )

    task1a_sub_scores['task1a_TOTAL'] = sum([task1a_sub_scores.get(sub_score) for sub_score in task1a_sub_scores.keys()])


    return task1a_sub_scores

def score_task1b(firstname: str, lastname: str) -> dict:
    """
    This function identifies a submitted .csv based on the the passed first and last names, and returns a dictionary of sub-scores for Task 1b

    :param firstname: A lowercase string
    :param lastname: A lowercase string
    :return: A dictionary of sub-scores 
    """
    
    task1b_sub_scores = {
        'task1b_cols' : 0,
        'task1b_obs_count' : 0,
        'task1b_sample_check' : 0,
        'task1b_misc_check' : 0,
        'task1b_TOTAL' : 0
    }

    task1b_csv_path = 'FODLERX/FOLDERY/{firstname}_{lastname}/task1b/task1b_{firstname}_{lastname}.csv'.format(
        firstname = firstname,
        lastname = lastname
    )
    task1b_submitted_df = pd.read_csv(task1b_csv_path)
    
    # SCORING FUNCTIONS CALLED
    task1b_sub_scores['task1b_cols'] = col_check(
        taskname = 'Task 1b',
        answer_cols = set(list(task1b_answer_key_df.columns)),
        submission_cols = set(list(task1b_submitted_df.columns))
    )

    task1b_sub_scores['task1b_obs_count'] = df_length_check(
        taskname = 'Task 1b',
        answer_df = task1b_answer_key_df,
        submission_df = task1b_submitted_df,
    )

    task1b_sub_scores['task1b_sample_check'] = df_length_check(
        taskname = 'Task 1b',
        answer_sample = task1b_answer_key_df.sample(n=100, random_state=random_state_seed),
        submission_df = task1b_submitted_df
    )
    task1b_sub_scores['task1b_misc_check'] = df_misc_check(
        misc_sample = task1b_misc_df.sample(n=100, random_state=random_state_seed),
        submission_df = task1b_submitted_df
    )

    task1b_sub_scores['task1b_TOTAL'] = sum([task1b_sub_scores.get(sub_score) for sub_score in task1b_sub_scores.keys()])

    return task1b_sub_scores



for index, candidate in candidates_to_score(task_status_df):

    candidate_firstname = candidate.firstname
    candidate_lastname = candidate.lastname
    candidate_name = '_'.join([candidate_firstname, candidate_lastname])

    task1a_scores_dict = score_task1a(candidate_firstname, candidate_lastname)
    task1b_scores_dict = score_task1b(candidate_firstname, candidate_lastname)

    print('SCORING {}:'.format(candidate_name.upper()))
    for sub_score in task1a_scores_dict.keys():
        task_scores_df.loc[candidate_name, sub_score] = task1a_scores_dict.get(sub_score)
    
    for sub_score in task1b_scores_dict.keys():
        task_scores_df.loc[candidate_name, sub_score] = task1b_scores_dict.get(sub_score)
    


    task_scores_df.to_csv('qwer', index=True, encoding='utf-8')
    update_score_status()
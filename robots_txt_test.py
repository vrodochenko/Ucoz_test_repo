import requests
import os
import re

'''
Works with Python 3.5 or Anaconda.

This is a test task for ucoz project. The formulation and more comments in Russian could be found in the ipython
notebook at https://github.com/vrodochenko/Ucoz_test_repo/blob/master/Ucoz%20test%20task.ipynb
This document contains a code only.
'''


def is_string_a_valid_url(string):
    """
    This function add some validation for our user input. This one is for the case when we expect a url to be entered.
    The idea of the regular expression is from here: https://web.izjum.com/regexp-email-url-phone (in Russian)
    :param string: a string we want to check
    :return: True or False
    """
    url_regexp = '^((https?|ftp)\:\/\/)?([a-z0-9]{1})((\.[a-z0-9-])|([a-z0-9-]))*\.([a-z]{2,6})(\/?)$'
    if re.match(url_regexp, string):
        return True
    else:
        return False


def ask_for_url():
    """
    The first requirement for this was to read a user's input.
    Using previously defined functions, namely: is_string_a_valid_url() and is_string_a_valid_ip()
    we are going to make a simple sanity check.

    It also seems convenient to automatically add an 'https://' prefix if there is no protocol specified.
    and add '/robots.txt'

    :return: a url if everything went well. Returns 1 in case of errors.
    """
    url_entered = input("Enter the url you wich to retrieve 'robots.txt' from: ")

    if not url_entered.startswith('http') and not url_entered[0].isdigit():
        url_entered = "https://" + url_entered

    if is_string_a_valid_url(url_entered) and not url_entered.endswith('/robots.txt'):
        url_entered += '/robots.txt'
        return url_entered
    else:
        print("You're probably entering not a valid url. Please make sure the input is correct.")
        return 1


def download_robots_txt(path_to_robots_txt, my_user_agent='*'):
    """
    This method uses the 'request' package to retrieve a file from the url specified.
    An optional parameter is for the (unlikely) case where we need a specific user-agent to be able to download
    a file we want.

    It uses a procedure that iterates over a file we download (for almost impossible case of robots.txt
    being exceptionally large).

    Prints out the logstring and the filename, just for convenience

    :param path_to_robots_txt: a full path to robots.txt.
    :param my_user_agent: in case we need to specify one
    :return:
    """
    local_filename = "robots_local_temp.txt"
    my_headers = requests.utils.default_headers()
    my_headers.update({'User-Agent': my_user_agent})
    try:
        r = requests.get(path_to_robots_txt, headers=my_headers)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        logstring = 'download finished, temporary file ./' + local_filename + ' created'
        print(logstring)
        return 0
    except requests.exceptions.RequestException as e:
        print(e)


def parse_robots_txt():
    """
    Parses a local copy of the file 'robots.txt' we probably have.

    To pass a file only once, we needed a logic that allows to store the very first user-agent name as a key,
    and associate the collected data with it only after we have met the next one (or the end of file).

    :return: a resulting data structure which is essentially a dictionary of dictionaries. The external keys are
    User-Agents, the internal ones are 'Allowed' and 'Disallowed'. The internal values are lists of domains
    """
    if os.path.exists("robots_local_temp.txt"):
        local_file = open('robots_local_temp.txt', 'r')
        resulting_data_set = {}
        agent_name_current = 'NoAgent'
        agent_name_next = 'NoAgent'
        for line in local_file:
            line = line.split('\n')[0]
            if line.startswith('User-agent'):
                agent_name_next = line.split(': ')[1].split(' ')[0]
                if not agent_name_current == 'NoAgent':
                    resulting_data_set[agent_name_current] = data_set_for_current_user_agent
                agent_name_current = agent_name_next
                data_set_for_current_user_agent = {"Disallowed": [], "Allowed": []}
            else:
                if line.startswith('Allow'):
                    # filter some possibly useless info and comments
                    data_set_for_current_user_agent["Allowed"].append(line.split(': ')[1].split(' ')[0])
                elif line.startswith('Disallow'):
                    # same thing here
                    data_set_for_current_user_agent["Disallowed"].append(line.split(': ')[1].split(' ')[0])
        # we now have the info of the last (and probably the unique one) agent. So it is time to write them to a
        # data structure we have and stop.
        agent_name_current = agent_name_next
        resulting_data_set[agent_name_current] = data_set_for_current_user_agent
        return resulting_data_set
    else:
        print('A local copy of robots.txt is missing for some reason.')
        return 1


def print_out_the_result(result):
    """
    This function is to generate a bit more human-readable form of the output.
    Makes a bit easier to track which 'Allows' and 'Disallows' suits a User-Agent we are interested in.
    :param: a data structure returned by parse_robots_txt() method
    :return: 0 - for and ideal case. 1 - if we have no output but somehow reached this point and launched a function
    """
    if result == 1:
        print("No output created")
        return 1
    else:
        for key in result.keys():
            print(key, ':')
            for inner_key in result[key]:
                print(inner_key, ':')
                print(result[key][inner_key])
            print()
        return 0


def dispose_of_temp_file():
    """
    One way to parse a file is to download it and store its local version.
    However, it is quite awkward to leave a user with a file he didn't want to create.
    Or use a file with the same name someone occasionally left there for some reason.
    So, before and after we run our code, we need to clean up.

    :return: 0 - if we can remove a file. Raises a warning otherwise.
    """
    if os.path.exists("robots_local_temp.txt"):
        try:
            os.remove("robots_local_temp.txt")
            print('cleaning up...')
        except OSError:
            raise UserWarning("Cannot remove 'robots_local_temp.txt'. Is it opened somewhere?")
    return 0

if __name__ == '__main__':
    dispose_of_temp_file()
    url = ask_for_url()
    download_robots_txt(url)
    result_obtained = parse_robots_txt()
    print_out_the_result(result_obtained)
    dispose_of_temp_file()

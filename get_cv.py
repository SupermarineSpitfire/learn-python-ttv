"""
    Get CV's by keywords from SuperJob using API.
    Save CV list into JSON file.
    The format of CV list is:
    [
        {
            'title': 'Программист Python',
            'gender': 'female',
            'age': 25,
            'has_degree': True,
            'city': 'Москва',
            'keywords': ['python' ,'mysql', 'xml', 'ios', 'windows phone',],
            'url': 'https://www.superjob.ru/resume/programmist-python-20379183.html',
        }
    ]
    There is a restriction: max number of CV's returned is 500: 100 for 1 page. 
"""


import requests
import json
import analyze_cv


def read_client_info():
    with open('client_info.json') as json_data:
        client_info = json.load(json_data)
        json_data.close()
    return client_info


def get_access_token(client_info):
    url = client_info["url_to_get_token"]
    params ={
             "client_id": client_info["client_id"],
             "client_secret": client_info["client_secret"],
             "login": client_info["login"],
             "password": client_info["password"]
            }
    result = requests.get(url, params=params)
    access_token = result.json()["access_token"]
    #print(access_token)
    return access_token


def get_keywords():
    keywords = []
    entered_keywords = input("Please enter keywords to search CV: ")
    keywords = entered_keywords.strip().split()
    for keyword in keywords:
        keyword.strip()
    #print(keywords)
    return keywords


def get_cv_data_by_keyword(client_info, token, keywords, page=0):
    url = client_info["url_to_get_cv_list"]
    params = {}

    params["keyword"] = keywords
    params["count"] = 100
    params["page"] = page

    access_token = "Bearer" + " " + token
    headers = {"Authorization": access_token, "X-Api-App-Id": client_info["client_secret"]}
    result = requests.get(url, headers=headers, params=params)
    #print(result)
    return result.json()["objects"]


def save_cv_into_file(cv_list, keywords, file_open_mode="w"):
    cv_list_to_save = []

    for cv in cv_list: 
        cv_list_to_save.append(produce_dictionary(cv, keywords))

    with open("cv_list.json", file_open_mode) as cv_json_file:     
        json.dump(cv_list_to_save, cv_json_file, ensure_ascii=False,  indent=4, sort_keys=True)
    return cv_list_to_save, len(cv_list)


def produce_dictionary(cv, keywords):
    cv_dict = {}
    cv_dict["title"] = cv["profession"]
    cv_dict["gender"] = cv["gender"]["title"]
    cv_dict["age"] = cv["age"]
    cv_dict["city"] = cv["town"]["title"]
    cv_dict["keywords"] = keywords
    cv_dict["url"] = cv["link"]
    if cv["education"]["title"] == "Высшее":
        cv_dict["has_degree"] = True
    else:
        cv_dict["has_degree"] = False
    return cv_dict


if __name__ == '__main__':

    client_info = read_client_info()
    keywords = get_keywords()
    token = get_access_token(client_info)
    file_open_mode = "w"
    complete_cv_list = []
    number_of_cvs = 0

    for page in range(5):
        cv_list = get_cv_data_by_keyword(client_info, token, keywords, page)
        if cv_list:
            saved_cv, number_of_cvs_per_page = save_cv_into_file(cv_list, keywords, file_open_mode)
        else:
            #print("No CV for page %s" % page)
            break
        file_open_mode = "a"
        complete_cv_list.extend(saved_cv)
        number_of_cvs += number_of_cvs_per_page
    print("Number of CV's returned: %d" % number_of_cvs)
    
    grouping_values_list = ["city", "title", "gender", "has_degree"]
    grouping_value = ""
    
    if saved_cv:

        while grouping_value == "":
            grouping_value = input("\nPlease specify grouping value\
                                   \nGrouping is available by: age, city, title, gender, has_degree\
                                   \nIf you want to exit please enter 'q' or 'Q': ")
            grouping_value = grouping_value.strip()

            if grouping_value.lower() == "q":
                exit(0)

            elif grouping_value == "age":
                analyze_cv.group_by_age(complete_cv_list)
                grouping_value = ""
                continue

            elif grouping_value not in grouping_values_list:
                print("Grouping value is unavailable in the current list")
                grouping_value = ""
                continue

            else:
                analyze_cv.group_by_value(complete_cv_list, grouping_value)
                grouping_value = ""
                continue
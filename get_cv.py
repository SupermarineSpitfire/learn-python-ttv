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
    print(access_token)
    return access_token


def get_keywords():
    keywords = []
    entered_keywords = input("Please enter keywords to search CV:\n>>")
    keywords = entered_keywords.strip().split()
    for keyword in keywords:
        keyword.strip()
    print(keywords)
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
    print(result)
    return result.json()["objects"]


def save_cv_list(cv_list, keywords):
    cv_list_to_save = []
    cv_dict = {}

    for cv in cv_list:
        try:
            cv_dict = produce_dictionary(cv, keywords)
        except:
            print("Something went wrong when parsing CV: %s" % (str(cv)))
            continue
        cv_list_to_save.append(cv_dict)

    return cv_list_to_save


def save_cv_list_into_file(cv_list_to_save):
    with open("cv_list.json", "w") as cv_json_file:     
        json.dump(cv_list_to_save, cv_json_file, ensure_ascii=False,  indent=4, sort_keys=True)


def produce_dictionary(cv, keywords):
    cv_dict = {}
    cv_dict["title"] = cv["profession"]
    cv_dict["gender"] = cv["gender"]["title"]
    cv_dict["age"] = cv["age"]
    cv_dict["city"] = cv["town"]["title"]
    cv_dict["keywords"] = keywords
    cv_dict["url"] = cv["link"]

    try:
        has_degree = cv["education"]["title"]
    except:
        has_degree = False  

    if has_degree == "Высшее":
        cv_dict["has_degree"] = True
    else:
        cv_dict["has_degree"] = False

    return cv_dict


if __name__ == '__main__':

    client_info = read_client_info()
    keywords = get_keywords()
    token = get_access_token(client_info)

    saved_cv_list = []
    complete_cv_list = []
    number_of_cv_list = 0

    for page in range(5):
        cv_list = get_cv_data_by_keyword(client_info, token, keywords, page)
        if cv_list:
            saved_cv_list = save_cv_list(cv_list, keywords)
            number_of_cv_list += len(saved_cv_list)
            complete_cv_list.extend(saved_cv_list)
            if len(saved_cv_list) < 100:
                print("Total number of CV's returned: %d" % number_of_cv_list)
                break

    try:
        save_cv_list_into_file(complete_cv_list)
    except:
        print("Something goes wrong with saving CV list into file.")

    values_list = ["age", "city", "title", "gender", "has_degree"]
    input_value = ""
    filter_or_count_input_value = ""

    while input_value == "":
        input_value = input("\nPlease specify value to count or filter by.\
                                \nGroup/filter is available for:\
                                \n\tage, city, title, gender, has_degree.\
                                \nTo exit please enter 'q' or 'Q'.\n>>")
        input_value = input_value.strip()

        if input_value.lower() == "q":
            exit(0)

        elif input_value not in values_list:
            print("Specified value is unavailable in the current list.")
            input_value = ""
            continue

        else:
            json_file_object = analyze_cv.parse_json("cv_list.json")
            if not json_file_object:
                exit(0)

            filter_or_count_input_value = input("\nWould you like to filter or count by? (C/F)\n>>")
            filter_or_count_input_value.strip()

            if filter_or_count_input_value.lower() == "c":
                if input_value == "age":
                    analyze_cv.print_result(analyze_cv.count_by_age_group(json_file_object))
                else:
                    analyze_cv.print_result(analyze_cv.count_by_value(json_file_object, input_value))

            elif filter_or_count_input_value.strip().lower() == "f":
                analyze_cv.print_result(analyze_cv.filter_links(json_file_object, input_value))
            
            input_value = ""
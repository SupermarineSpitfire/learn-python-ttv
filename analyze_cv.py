"""
    This module is intended to get some statistics
    about CV list which is returned  by particular query:
    1) group by age: age<18, 18<=age<50, age>=50
    2) group by city
    3) group by job title
    4) group by gender
    5) group by degree
"""


import json


def parse_json(json_file):
    try:
        with open("cv_list.json", "r") as json_file_object:
            return json.load(json_file_object)
    except:
        print("Not able to parse JSON file for some reason")
        return False


def filter_links(json_file_object, filtering_parameter):
    list_of_values_to_filter = []
    filterd_links_by_parameter = {}

    if json_file_object is False or filtering_parameter is False:
        print("No content or parameter to parse")
        return

    for cv in json_file_object:
        if filtering_parameter not in list_of_values_to_filter:
            list_of_values_to_filter.append(cv[filtering_parameter])
        else:
            continue

    for value in list_of_values_to_filter:
        filterd_links_by_parameter[value] = []

    for value in list_of_values_to_filter:
        for cv in json_file_object:
            if cv[filtering_parameter] == value:
                filterd_links_by_parameter[value].append(cv["url"])
            else:
                continue

    return filterd_links_by_parameter


def print_result(filtered_links={}):
    if filtered_links == {}:
        print("No links available for specified parameter")
    else:
        for item in filtered_links.items():
            print("\n%s:" % item[0])
            if isinstance(item[1], int):
                print("\t%d" % item[1])
            else:
                for link in item[1]:
                    print("\n\t%s" % link)


def get_parameter_to_filter_or_count_by():
    existent_list_of_parameters = ["city", "age", "has_degree", "gender", "title"]
    filtering_parameter = input("\nPlease specify parameter to filter by:\
                                \nAvailable parameters are:\
                                \n\tcity, age, has_degree, gender, title.\n>>")
    if filtering_parameter not in existent_list_of_parameters:
        print("No such parameter in the list")
        return False
    return filtering_parameter


def count_by_age_group(cv_list):
    age_groups = ["age<18", "18<=age<=25", "25<age<=35", "35<age<=45", "45<age<=55", "age>55"]
    count_by_age = {}
    age_list = []

    for age_group in age_groups:
        count_by_age[age_group] = 0
    
    for cv in cv_list:
        age_list.append(cv["age"])

    for age in age_list:
        if age < 18:
            count_by_age["age<18"] += 1
        if 18 <= age <= 25:
            count_by_age["18<=age<=25"] += 1
        if 25 < age <= 35:
            count_by_age["25<age<=35"] += 1
        if 35 < age <= 45:
            count_by_age["35<age<=45"] += 1
        if 45 < age <= 55:
            count_by_age["45<age<=55"] += 1
        if age > 55:
            count_by_age["age>55"] += 1

    return count_by_age


def count_by_value(cv_list, grouping_by_value):
    group_dict = {}
    group_list = []
    grouping_values_list = ["city", "title", "gender", "has_degree"]

    for cv in cv_list:
        if cv[grouping_by_value] not in group_list:
            group_list.append(cv[grouping_by_value])

    for city in group_list:
        group_dict[city] = 0

    for city in group_dict:
        for cv in cv_list:
            if cv[grouping_by_value] == city:
                group_dict[city] += 1

    return group_dict


if __name__ == '__main__':
    json_file_object = parse_json("cv_list.json")
    
    if not json_file_object:
        exit(0)

    filtering_parameter = get_parameter_to_filter_or_count_by()
    if filtering_parameter is False:
        exit(0)
    count_or_filter_parameter = input("Whould you like to filter or count by? (C/F)\n>>")
    count_or_filter_parameter = count_or_filter_parameter.strip().lower()
    if count_or_filter_parameter == "c":
        if filtering_parameter == "age":
            print_result(count_by_age_group(json_file_object))
        else:
            print_result(count_by_value(json_file_object, filtering_parameter))
    elif count_or_filter_parameter == "f":
        print_result(filter_links(json_file_object, filtering_parameter))
    else:
        exit(0)
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


def group_by_age(cv_list):
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

    print("\nGrpouping by age:")
    for item in count_by_age.items():
        print("\t", item)

    return count_by_age


def group_by_value(cv_list, grouping_by_value):
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

    print("CV count by %s:" % grouping_by_value)
    for city in group_dict.items():
        print("\t%s" % str(city))

    return group_dict


def sort_links_by_city(cv_list):
    city_list = []
    cv_links_by_city = {}
    links_list =[]

    for cv in cv_list:
        if cv["city"] not in city_list:
            city_list.append(cv["city"])
        else:
            continue

    for city in city_list:
        cv_links_by_city[city] = []

    for city in city_list:
        for cv in cv_list:
            if cv["city"] == city:
                links_list.append(cv["url"])
            else:
                continue
            cv_links_by_city[city] = links_list

    return cv_links_by_city


if __name__ == '__main__':
    pass
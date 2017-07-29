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

    age_younger_than_18 = []
    age_between_18_and_50 = []
    age_older_than_50 = []
    
    for cv in cv_list:
        if cv["age"] < 18:
            age_younger_than_18.append(cv)
        elif 18 <= cv["age"] < 50:
            age_between_18_and_50.append(cv)
        else:
            age_older_than_50.append(cv)

    age_dict = {
        "before_18": len(age_younger_than_18),
        "between_18_and_50": len(age_between_18_and_50),
        "after_50": len(age_older_than_50)
    }
    print("Grpouping by age: \n\tBefore 18 - %d,\n\tBetween 18 and 50: %d,\n\tAfter 50: %d" % \
          (age_dict["before_18"], age_dict["between_18_and_50"], age_dict["after_50"]))
    return age_dict["before_18"], age_dict["between_18_and_50"], age_dict["after_50"]


def group_by_value(cv_list, group_by_value):
    group_dict = {}
    group_list = []
    grouping_values_list = ["city", "title", "gender", "has_degree"]

    for cv in cv_list:
        if cv[group_by_value] not in group_list:
            group_list.append(cv[group_by_value])

    for city in group_list:
        group_dict[city] = 0

    for city in group_dict:
        for cv in cv_list:
            if cv[group_by_value] == city:
                group_dict[city] += 1

    print("CV count by %s:" % group_by_value)
    for city in group_dict.items():
        print("\t%s" % str(city))

    return group_dict


if __name__ == '__main__':
    pass
#test3
if __name__ == '__main__':
    user_info = {"first_name": "Tatiana", "last_name": "Trofimova"}
    name = input("Please enter 'first' to see first name and 'last' to see last name: ")
    if name in ('first', 'last'):
        user_info_name = name + '_name'
        print(user_info.get(user_info_name))
    else:
        print("Incorrect input")
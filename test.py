#test1
if __name__ == '__main__':
    weather_list = [
        {"city": "Moscow", "temperature": 24, "date": "25-05-2017"},
        {"city": "Moscow", "temperature": 20, "date": "26-05-2017"}]
    date = input("Введите дату в формате дд-мм-гггг: ")
    i=0
    while (i<len(weather_list)):
        if date == weather_list[i].get("date", "Извините, произошла ошибка"):
            print('Температура в Москве:', weather_list[i].get("temperature"))
            break
        else:
            i+=1
    if i==len(weather_list):
        print("На заданную дату нет информации")
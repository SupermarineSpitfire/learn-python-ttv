#test5
from get_summ import get_summ

def get_answer(question):
    answers = {
        "привет": "И тебе привет!",
        "как дела": "Лучше всех",
        "пока": "Увидимся"}
    
    return answers.get(question.lower(), "Такого слова в словаре нет")

if __name__ == '__main__':
    answer = input("Введите 'привет' или 'как дела' или 'пока': ")
    print(get_answer(answer))
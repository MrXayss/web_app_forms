import requests

def send_request(message,data):
    response = requests.post('http://localhost:8000/get_form/', data=data)
    print(message, response.text)


send_request(
    'Запрос с полным несовпадениям по полям:',
    {'user_mail12': 'admin@gmail.com', 'user_yes': '+79134323546', 'user_descri+ption': 'i am admin1'}
)

send_request(
    'Запрос с полным совпадением:',
    {'user_mail': 'test@ya.ru', 'reg_date': '21.09.2021', 'user_phone': '+79134321563', 'user_description': 'i am admin'}
)

send_request(
    'Запрос где есть поля, которые не существуют и одно поле которое есть в двух формах:',
    {'user_ma': 'admin@gmail.com', 'test': 'test', 'user_description': 'i am admin'}
)

send_request(
    'Запрос со всеми полями одной формы но дата другого формата:',
    {'user_mail': 'user1@ya.ru', 'user_phone': '+79134323546', 'reg_date': '2020-10-10', 'user_description': 'test333'}
)

send_request(
    'Запросы где только одно поле (правильное):',
    {'user_phone': '+79134323546'}
)

send_request(
    'Запросы где только одно поле (неправильное):',
    {'test': '+79134323546'}
)

send_request(
    'Запрос если поля совпали а значения нет:',
    {'user_mail': 'user1@gmail.ru', 'user_phone': '+79134323545'}
)
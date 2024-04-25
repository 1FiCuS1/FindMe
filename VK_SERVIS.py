import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.exceptions import ApiError
import json

from search_criteria import create_search_criteria
token = "vk1.a.BIz9EanDLhQLtuSTT5mVGSTvU7mIycKbGSzDDIVisPwVFO7VwFuglk4c8Z87XC1M0dS_fkkVsCll42WTCH5toPeEabcYTxCz6C7gqoLgTEKd6DrSD9uU0tofY8S3AhXZp_1Ln18-CKTWtrRn81IG18MBY2KAMrAIE3L_DuKKkNiW3sKzPQkdScH722rzshSP5asvFd_daoETjY_-2CzvSg"
authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)
criteria = open('criteria1.json', 'r')
class Vk_servis:
    def __init__(self, user_id, vk_session):
       pass

    def people_search(user_id, vk_session, criteria):
        sex = criteria.get('sex', 0)
        age_from = criteria.get('age_from', 0)
        age_to = criteria.get('age_to', 0)
        city = criteria.get('city', 0)
        relation = criteria.get('relation', 0)

        try:
            users = vk_session.method('users.search', {
                'sex': sex,
                'age_from': age_from,
                'age_to': age_to,
                'city': city,
                'relation': relation,
                'count': 10,
                'has_photo': 1,
                'fields': 'photo_id'
            })
        except vk_api.exceptions.ApiError as e:
            vk_session.method('messages.send', {
                'user_id': user_id,
                'message': f'Произошла ошибка при поиске пользователей: {e}',
                'random_id': get_random_id()
            })
            return

        if users['items']:
            result_message = 'Найденные пользователи:\n'
            for user in users['items']:
                result_message += f"{user['first_name']} {user['last_name']} (id{user['id']} ({user['city']['title']}) ({user['age']})\n"
                # Добавляем ссылку на фотографию пользователя
                result_message += f"https://vk.com/id{user['id']}\n\n"
            vk_session.method('messages.send', {
                'user_id': user_id,
                'message': result_message,
                'random_id': get_random_id()
            })
        else:
            vk_session.method('messages.send', {
                'user_id': user_id,
                'message': 'К сожалению, ничего не найдено по заданным критериям.',
                'random_id': get_random_id()
            })

        criteria = create_search_criteria(user_id, vk_session)

if __name__ == '__main__':
    criteria
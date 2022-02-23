import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
# from datetime import datetime, timedelta
# from apscheduler.schedulers.background import BackgroundScheduler
import config
import files

session = vk_api.VkApi(token = config.api_token)
longpoll = VkBotLongPoll(session, config.group_id)
chat_id = -1


def get_name(uid: int) -> str:
    data = session.method("users.get", {"user_ids": uid})[0]
    return "{}".format(data["first_name"])


def sendMessage(id, text):
    session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})


def sendMessageWithAttachment(id, text, attachment):
    session.method('messages.send', {'chat_id': id, 'message': text, 'attachment': attachment, "random_id": 0})


def listenForEvents():
    global chat_id
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.from_chat:
                        chat_id = event.chat_id
                        user = event.object.message['from_id']
                        msg = event.object.message['text'].lower()

                        if 'алим' in msg:
                            sendMessage(chat_id, 'Алим - хороший человек.')
                        # elif 'аркадий' in msg or 'аркаша' in msg:
                        #     sendMessage(chat_id, 'Аркадий - нехороший человек. То ли дело Алим!')
                        elif 'окуму' in msg:
                            okumu = random.randint(0, 1)
                            sendMessageWithAttachment(chat_id, 'Black Watermelons Matter 🍉', files.special_watermelons[okumu])
                        elif 'бебра' in msg or 'беброчка' in msg:
                            sendMessageWithAttachment(chat_id, 'BEBRE', files.special_watermelons[2])
                        elif 'артур' in msg:
                            sendMessageWithAttachment(chat_id, '🦄 🍉', files.special_watermelons[3])
                        elif 'хочу арбуз' in msg or 'хачу арбуз' in msg or 'хачю арбуз' in msg:
                            watermelon = random.randint(0, len(files.watermelons) - 1)
                            sendMessageWithAttachment(chat_id, f'Держи арбуз, [id{user}|{get_name(user)}] 🍉', files.watermelons[watermelon])
        except Exception as e:
            pass


def main():
    listenForEvents()


if __name__ == '__main__':
    main()

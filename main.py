import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from config import api_token, group_id
from files import arkadiy, special_watermelons, watermelons

session = vk_api.VkApi(token = api_token)
longpoll = VkBotLongPoll(session, group_id)
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
                        elif 'аркадий' in msg or 'аркаша' in msg:
                            sendMessage(chat_id, 'Аркадий - нехороший человек. То ли дело Алим!')
                        elif 'окуму' in msg:
                            okumu = random.randint(0, 1)
                            sendMessageWithAttachment(chat_id, 'Black Watermelons Matter 🍉', special_watermelons[okumu])
                        elif 'бебра' in msg or 'беброчка' in msg:
                            sendMessageWithAttachment(chat_id, 'BEBRE', special_watermelons[2])
                        elif 'артур' in msg:
                            sendMessageWithAttachment(chat_id, '🦄 🍉', special_watermelons[3])
                        elif 'хочу арбуз' in msg or 'хачу арбуз' in msg or 'хачю арбуз' in msg:
                            watermelon = random.randint(0, len(watermelons) - 1)
                            sendMessageWithAttachment(chat_id, f'Держи арбуз, [id{user}|{get_name(user)}] 🍉', watermelons[watermelon])
        except Exception as e:
            pass


def job():
    global chat_id
    arbuz = random.randint(0, len(watermelons) - 1)
    if chat_id != -1:
        sendMessageWithAttachment(chat_id, 'Привет! Держи арбуз 🍉', watermelons[arbuz])


def main():
    today = datetime.today()
    newTime = today.replace(day = today.day, hour = 10, minute = 0, second = 0, microsecond = 0) + timedelta(days = 1)
    delta = newTime - today
    secs = delta.total_seconds()
    scheduler1 = BackgroundScheduler()
    scheduler1.add_job(job, 'interval', seconds = secs)
    scheduler1.start()
    newTime = today.replace(day = today.day, hour = 14, minute = 0, second = 0, microsecond = 0) + timedelta(days = 1)
    delta = newTime - today
    secs = delta.total_seconds()
    scheduler2 = BackgroundScheduler()
    scheduler2.add_job(job, 'interval', seconds = secs)
    scheduler2.start()
    newTime = today.replace(day = today.day, hour = 18, minute = 0, second = 0, microsecond = 0) + timedelta(days = 1)
    delta = newTime - today
    secs = delta.total_seconds()
    scheduler3 = BackgroundScheduler()
    scheduler3.add_job(job, 'interval', seconds = secs)
    scheduler3.start()

    listenForEvents()


if __name__ == '__main__':
    main()

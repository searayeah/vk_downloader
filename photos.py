import vk_api
import requests
import os


def get_chats():
    offset = 0
    return_length = 200
    while return_length == 200:
        chats = vk.messages.getConversations(
            count=200, offset=offset, extended=1
        )
        for item in chats["items"]:
            if item["conversation"]["peer"]["type"] == "chat":
                print(
                    f'{item["conversation"]["peer"]["id"]}'
                    + " : "
                    + f'{item["conversation"]["chat_settings"]["title"]}'
                )
            else:
                for profile in chats["profiles"]:
                    if profile["id"] == item["conversation"]["peer"]["id"]:
                        print(
                            f'{item["conversation"]["peer"]["id"]}'
                            + " : "
                            + f'{profile["first_name"]}'
                            + " "
                            + f'{profile["last_name"]}'
                        )
        offset += 200
        return_length = len(chats["items"])


def get_photos(chat_id):
    print(f"Скачиваю все фотографии из чата {chat_id}")
    i = 0
    from_msg = 0
    attach_length = 200
    amount = 0
    os.makedirs(f"data/{chat_id}/photos", exist_ok=True)
    while attach_length == 200:

        attachments = vk.messages.getHistoryAttachments(
            peer_id=chat_id,
            media_type="photo",
            count=200,
            start_from=from_msg,
        )
        for item in attachments["items"]:
            url = item["attachment"]["photo"]["sizes"][-1]["url"]
            r = requests.get(url)
            open(f"data/{chat_id}/photos/{i}.jpg", "wb").write(r.content)
            i += 1
            from_msg = attachments["next_from"]
        attach_length = len(attachments["items"])
        amount += attach_length
        print(amount, end="\r")
    print(f"Скачано {amount} картинок")


def get_messages(chat_id):
    offset = 0
    return_length = 200
    amount = 0
    os.makedirs(f"data/{chat_id}", exist_ok=True)
    with open(f"data/{chat_id}/messages.txt", "w") as file:
        while return_length == 200:
            messages = vk.messages.getHistory(
                peer_id=chat_id, count=200, offset=offset, extended=1
            )
            for message in messages["items"]:
                for profile in messages["profiles"]:
                    if profile["id"] == message["from_id"]:
                        file.write(
                            f'{profile["first_name"]}'
                            + " "
                            + f'{profile["last_name"]}'
                            + f' : {message["text"]}\n'
                        )
            offset += 200
            return_length = len(messages["items"])
        amount += return_length
        print(amount, end="\r")
    print(f"Скачано {amount} сообщений")


TOKEN = input("Введите токен: ")
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
os.makedirs("data", exist_ok=True)
get_chats()
while True:

    chat_id = int(input("Введите id чата/беседы (цифры слева): "))
    action = input("Что хотите скачать photos/messages? ")

    if action == "photos":
        get_photos(chat_id)
    elif action == "messages":
        get_messages(chat_id)
    else:
        exit()

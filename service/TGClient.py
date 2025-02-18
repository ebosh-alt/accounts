import logging

from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest
from telethon.tl.types import Chat, Updates, InputUser

logger = logging.getLogger(__name__)


class TG_Acc:
    '''
    session_name: str
    api_id: int
    api_hash: str
    phone_number: str
    '''

    def __init__(self, session_name: str, api_id: int, api_hash: str, phone_number: str) -> None:
        self.session_name: str = session_name
        self.api_id: int = api_id
        self.api_hash: str = api_hash
        self.phone_number: str = phone_number


class TGClient_S:
    '''
    client: TelegramClient
    account: TG_Acc
    code: str|int
    '''

    def __init__(self, account: TG_Acc) -> None:
        self.client: TelegramClient = TelegramClient(session=account.session_name, api_id=account.api_id,
                                                     api_hash=account.api_hash, system_version='4.16.30-vxCUSTOM')
        self.account: TG_Acc = account
        self.code: str | int = None
        self.client.parse_mode = "md"

    def __call__(self):
        pass

    async def is_code_needed(self) -> int:
        # 0 - Аккаунт авторизован
        # 1 - Нужно авторизовать аккаунт
        # 2 - Аккаунт не подключается
        result = 1

        try:
            # Установление соединения clinet
            await self.client.connect()
            # Проверка: авторизован ли аккаунт
            if await self.client.is_user_authorized():
                result = 0
        except Exception as er:
            logger.info(er)
            result = 2

        # Завершение соединения с клиентом
        await self.disconnect_client()
        return result

    async def get_authorization_code(self) -> bool | str:
        result = False
        # Установление соединения clinet
        await self.connect_client()
        # try:
        #     await self.client.connect()
        # except Exception as er:
        #     print(er)

        # Отправка запроса на получения кода авторизации
        try:
            result_sending_auth_code = await self.client.send_code_request(self.account.phone_number)
            result = result_sending_auth_code.phone_code_hash
        except Exception as er:
            logger.info(er)

        # Завершение соединения с клиентом 
        await self.disconnect_client()
        return result

    async def enter_authorization_code(self, phone_code_hash) -> bool:
        result = False
        # Установление соединения clinet
        await self.connect_client()

        # Ввод кода авторизации
        try:
            await self.client.sign_in(phone=self.account.phone_number, code=self.code, phone_code_hash=phone_code_hash)
            result = True
        except Exception as er:
            logger.info(er)

        # Завершение соединения с клиентом 
        await self.disconnect_client()
        return result

    async def connect_client(self):
        try:
            await self.client.connect()
        except Exception as er:
            logger.info(er)

    async def disconnect_client(self):
        try:
            await self.client.disconnect()
        except Exception as er:
            logger.info(er)

    async def createChat(self, users: list[int | str], username_bot: str, title: str) -> tuple[int, bool]:
        chat_id = 0
        err = False
        try:
            await self.client.connect()
        except Exception as er:
            logger.info(er)
            err = True
        try:
            users_entity = []
            bot_entity = await self.client.get_entity(username_bot)
            for user in users:
                user = await self.client.get_entity(user)
                users_entity.append(InputUser(user_id=user.id, access_hash=user.access_hash))
            users_entity.append(InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash))
            data: Updates = await self.client(CreateChatRequest(users=users_entity, title=title))
            chat: Chat = data.chats[0]
            chat_id = chat.id
            try:
                await self.client.edit_admin(
                    chat,
                    bot_entity.id,
                    is_admin=True,
                )
            except Exception as er:
                logger.info(er)
                err = True
        except Exception as er:
            err = True
            logger.info(er)
        return chat_id, err


async def startTGClient(client_s: TGClient_S):
    if await client_s.is_code_needed() == 1:
        result_getting_auth_code = await client_s.get_authorization_code()
        if result_getting_auth_code.__class__.__name__ == "str":
            client_s.code = input("Введи код: ")
            result_auth = await client_s.enter_authorization_code(result_getting_auth_code)
            if result_auth:
                return logger.info("Аккаунт авторизован после отправки кода")
        else:
            return logger.info("1: Что-то пошло не так")
    elif await client_s.is_code_needed() == 2:
        return logger.info("Аккаунт не подключился во время проверки на необходимость кода для авторизации")
    elif await client_s.is_code_needed() == 0:
        return logger.info("Аккаунт авторизован раннее")

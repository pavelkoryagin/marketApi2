import datetime

class Podpiska:
    def __init__(self, user_id: int, podpiska: bool, data_podpiska: datetime ):
        self.user_id = user_id,
        self.podpiska = podpiska,
        self.data_podpiska =data_podpiska

    async def get_podpiska(self):
        return Podpiska(self.user_id, self.podpiska, self.data_podpiska)

    async def is_podpiska(self):
        #ЗАпрос в базу данных о наличии подписки у данного пользователя
        pass
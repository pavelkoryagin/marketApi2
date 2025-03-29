class Magazin:
    def __init__(self, name, url):
        self.name = name,
        self.url = url

    #Возвращаем обхект магазина
    def get_magazin(self):
        return Magazin(self.name, self.url)


    #Провекрям, что такой магазин существует
    def is_magazin(self):
        magazin = self.get_magazin()
        print(repr(magazin))


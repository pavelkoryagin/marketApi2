import io
f = open('ozon.txt', 'r', encoding='utf-8')
listBody = f.readlines()
f.close()

# for st in stroka:
#     if st == 'c Ozon Картой\n':
#         print(st)
print(listBody)
try:
    n = listBody.index("с Ozon Картой\n")
    zena = listBody[n - 1]
    print(zena)
except ValueError as valEr:
    print(repr(valEr))

try:
    n = listBody.index('Добавить в корзину')
except ValueError as er:
    print(repr(er))

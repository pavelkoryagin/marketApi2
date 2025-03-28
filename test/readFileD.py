import asyncio
import aiofiles
import os
import time


def files_load():
    files = list()
    for i in range(1, 1000000):
        files.append(f"index{i}.html")
    return files

async def read_file(name):
    async with aiofiles.open(f'D:/1TESTFILE/{name}', 'r') as f:
        if os.path.exists(f'D:/1TESTFILE/{name}'):
            await f.read()
            print(name)

async def main():
    files = files_load()
    names = []
    for name in files:
        if len(names) == 100000:
            tasks = []
            for i in names:
                task = asyncio.create_task(read_file(i))
                tasks.append(task)

            try:
                await asyncio.gather(*tasks)
            except Exception as ex:
                repr(ex)

            names.clear()
        else:
            names.append(name)

if __name__ == '__main__':
    start = time.process_time()
    asyncio.run(main())
    res = time.process_time() - start
    print(res)



# async def load_file(name):
#     async with aiofiles.open(f'D:/1TESTFILE/{name}', 'r') as file:
#         try:
#             if os.path.exists(f'D:/1TESTFILE/{name}'):
#                 await file.read()
#                 print(name)
#         except FileExistsError as ex:
#             repr(ex)
#
#
# async def main():
#     files = files_load()
#     for name in files:
#         fil = []
#         fil.append(name)
#
#         if len(fil) == 1000:
#             # tasks = []
#             # for name in fil:
#             #     task = asyncio.create_task(load_file(name))
#             #     tasks.append(task)
#             #
#             # try:
#             #     await asyncio.gather(*tasks)
#             # except Exception as ex:
#             #     print(repr(ex))
#             print('POLON')
#             fil.clear()
#         else:
#             continue
#
#
#
# if __name__ == "__main__":
#     asyncio.run(main())

# def load_file(files):
#     for name in files:
#         with open(f'D:/1TESTFILE/{name}', 'r') as file:
#             if os.path.exists(f"D:/1TESTFILE/{name}"):
#                 text = file.read()
#                 print(name)
#
#
# def main():
#     files = files_load()
#     files = files[1:100]
#     load_file(files)
#
#
# if __name__ == "__main__":
#     main()

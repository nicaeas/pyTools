import time
from typing import List
from tqdm import tqdm
from itertools import chain
from rarfile import RarFile
# from zipfile import ZipFile  解压zip文件用到

start = time.time()

dictionaries = [
    chr(i) for i in chain(
        range(97, 123), #a-z
        range(65, 91),  #A-Z   
        range(48, 58)   #0-9
        )
        ] 
#   密码包含的字符集
#   dictionaries.extend(['.com', 'www.']) 
#   拓展字符集


def all_passwd(dictionaries: List[str], maxlen: int):
#   返回由 dictionaries 中字符组成的所有长度为 maxlen 的字符串
    def helper(temp: list, start: int, n: int):
        if start == n:                                  # 达到递归出口
            yield ''.join(temp)
            return
        for t in dictionaries:
            temp[start] = t                             # 在每个位置
            yield from helper(temp, start + 1, n)

    yield from helper([0] * maxlen, 0, maxlen)

rfile = RarFile('1.rar' , 'r')

def extract(rfile: RarFile, pwd: str) -> bool:                 # extract函数返回的是bool类型
    try:
        rfile.extractall(path='.', pwd=pwd.encode('utf-8'))    # 密码输入错误的时候会报错
        now = time.time()                                      # 故使用 try - except 语句
        print(f"Password is: {pwd}")                           # 将正确的密码输出到控制台
        return True
    except:
        return False

lengths = [5, 6, 7, 8]                                  # 密码长度范围
total = sum(len(dictionaries) ** k for k in lengths)    # 密码总数


for pwd in tqdm(chain.from_iterable(all_passwd(dictionaries, maxlen) for maxlen in lengths), total=total):
    if extract(rfile, pwd):    
        break

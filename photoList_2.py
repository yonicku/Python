import os
import pandas as pd
import re

photo_list = []

def search(dirname):
    try:
        filenames = os.listdir(dirname) #dirname으로 받은 파일 리스트를 filenames 함수에 저장한다.
        for filename in filenames: #filenames를 filename으로 넣어는다.
            full_filename = os.path.join(dirname, filename) #두개를 합쳐 풀네임을 만든다.
            if os.path.isdir(full_filename): #만약 경로가? 디렉토리일 경우
                search(full_filename) #재귀 호출
            else:
                ext = os.path.splitext(full_filename)[1] #1을 넣는건 os.path.splitext로 배열이 반환되는데 그중 확장자만 사용하기 위함
                if ext == '.jpg': 
                    photo_list.append(full_filename)
                if ext == '.jpeg': 
                    photo_list.append(full_filename)
    except PermissionError:
        pass

    print(photo_list)

searchdir = input("경로 입력")

search(searchdir)


import os
import pandas as pd
import re

photo_list = []
path ="./"
same_name_diff_size = bool
dif_name_same_size = bool
same_name_same_size = bool

#경로의 file_list 중 png와 jpeg를 photo_list로 정리한다.
file_list = os.listdir(path)
for f in os.listdir(path):
    if 'png' in f:
        photo_list.append(f)
    if 'jpeg' in f:
        photo_list.append(f)

#photo_list의 파일명을 토대로 경로의 리스트를 람다식을 사용하여 크기를 정렬한다.
photo_size = list(map(lambda x: os.path.getsize(x), photo_list))
#데이터 프레임을 만들든다. 이름 = name_raw / 크기 =size 컬럼에 추가한다.
find_same_photo = pd.DataFrame({'name_raw' : photo_list, 'size' : photo_size})
print('사진의 갯수 :', len(find_same_photo))

#name_raw의 파일명 숫자 제거하기 정규 표현식으로 name에 추가한다. 
#빈칸+숫자 이후의 값을 선정한다.
com = re.compile(' \d') 
 #photo_list의 빈칸+숫자 이후의 값을 지운다.
find_same_photo['name'] = list(map(lambda x: com.sub('', x), photo_list))

#정규화 이름 중 같은 이름을 카운트한다. 같은 이름은 same_photo_name_count에 저장
same_photo_name_count = pd.DataFrame({'name':find_same_photo['name'].value_counts().index, 'same_name_counts':find_same_photo['name'].value_counts().values})#
#정규화 이름 중 같은 사이즈를 카운트한다. 같은 사이즈는 same_photo_size_count에 저장
same_photo_size_count = pd.DataFrame({'size':find_same_photo['size'].value_counts().index, 'same_size_counts':find_same_photo['size'].value_counts().values})#같은 사이즈를 카운트 한다.

#그 값을 find_same_photo에 same_photo_name_count로 Left 조인으로 머지한다.
find_same_photo = pd.merge(find_same_photo, same_photo_name_count, how = 'left', on = 'name')
#그 값을 find_same_photo에 same_photo_size_count로 Left 조인으로 머지한다.
find_same_photo = pd.merge(find_same_photo, same_photo_size_count, how = 'left', on = 'size')

#파일 검사
for i in range(len(find_same_photo)):
    #이름 같고 크기 다른 파일
    if (find_same_photo['same_name_counts'][i] > 1) & (find_same_photo['same_size_counts'][i] == 1):
        print('이름 같고 크기 다른 파일', find_same_photo['name_raw'][i])
        same_name_diff_size = True
    #이름 다르고 크기 같은 파일
    if (find_same_photo['same_size_counts'][i]>1) & (find_same_photo['same_name_counts'][i]==1):
        print('이름 다르고 크기 같은 파일', find_same_photo['name_raw'][i])
        diff_name_same_size = True
    #이름 같고 크기 같은 파일
    if (find_same_photo['same_size_counts'][i]>1) & (find_same_photo['same_name_counts'][i]>1):
        print('이름 같고 크기 같은 파일', find_same_photo['name_raw'][i])
        same_name_same_size = True
    #그 외 파일   
    else:
        same_name_diff_size = False
        diff_name_same_size = False


if (same_name_diff_size == False) & (diff_name_same_size == False) :
    #겹치는 파일명 제거 후 새 데이터 프레임에 정렬
    find_same_photo_new = find_same_photo.sort_values(['name_raw'], ascending = False).drop_duplicates(['name'], keep = 'first')
    print('남은 사진의 갯수 : {}\n지워진 사진의 갯수 : {}'.format(len(find_same_photo_new), len(find_same_photo)-len(find_same_photo_new)))

    #겹치는 이름 및 사이즈 제거 후 정렬
    pvc_nsn = pd.DataFrame({'name':find_same_photo_new['name'].value_counts().index, 'same_n_count_new':find_same_photo_new['name'].value_counts().values})   
    psvc_nsn = pd.DataFrame({'size':find_same_photo_new['size'].value_counts().index, 'same_s_count_new':find_same_photo_new['size'].value_counts().values})   
    find_same_photo_new = pd.merge(find_same_photo_new, pvc_nsn, how = 'left', on = 'name')
    find_same_photo_new = pd.merge(find_same_photo_new, psvc_nsn, how = 'left', on = 'size')
    
    print('사이즈 같은 사진의 갯수 :', len(find_same_photo_new[find_same_photo_new['same_s_count_new']!=1]))
    print('중복 사이즈의 갯수 :', len(psvc_nsn[psvc_nsn['same_s_count_new']>1]))
    


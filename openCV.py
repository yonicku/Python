import cv2
import photoList
from skimage.metrics import structural_similarity as compare_ssim


delete = []

for i in range(len(photoList.psvc_nsn)):
    if photoList.psvc_nsn['same_s_count_new'][i] >=2:#왜 2이상인지?
        
        # 그 크기에 해당하는 사진을 불러온다. 
        temp = photoList.find_same_photo_new[photoList.find_same_photo_new['size']==photoList.psvc_nsn['size'][i]].reset_index(drop = True).sort_values(['name_raw'])
        
        # 사진 읽기
        imageA = cv2.imread(temp['name_raw'][0])
        imageB = cv2.imread(temp['name_raw'][1])
        
        # 이미지를 grayscale로 변환
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        if len(grayA)==len(grayB):
            (score, diff) = compare_ssim(grayA, grayB, full=True)
            if score == 1:
                delete.append(temp['name_raw'][1])
            else:
                print('확인해보시오! : ', temp['name_raw'][0], '/', temp['name_raw'][1], f'(score : {score})')

delete = delete + list(photoList.find_same_photo[~photoList.find_same_photo['name_raw'].isin(photoList.find_same_photo['name_raw'])]['name_raw'])
print('삭제할 목록 :', len(delete))

result=list(photoList.find_same_photo[~photoList.find_same_photo['name_raw'].isin(delete)]['name_raw'])
print('남길 목록 :', len(result))

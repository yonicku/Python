import shutil
import openCV

for i in openCV.result:
    shutil.move(i, './Result')

for i in openCV.delete:
    shutil.move(i, './Delete')
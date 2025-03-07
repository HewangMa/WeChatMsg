import pytesseract
import re
import os
import cv2
from PIL import Image


# from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
# from docx import *


# 剪裁图像
def cut(file_name) -> str:
    # 读取图像
    file_path = 'origin/' + file_name
    # print(file)
    image = cv2.imread(file_path)
    # 删除图像左侧的头像
    image = image[:, 130:]
    image = image[260:, :]
    new_file_path = 'cut/' + file_name
    cv2.imwrite(new_file_path, image)
    return new_file_path


# 剪裁所有图像
def cut_all():
    # 打开文件夹里的所有文件
    folder = "origin"
    files = os.listdir(folder)
    for file in files:
        cut(file)


# 剪裁图像参考代码
def ref_cut(file):
    image = cv2.imread(file)

    # 假设你已经剪裁了图像（这里仅作示例，实际情况可能不同）
    cropped_image = image[100:300, 100:300]  # 假设你已经剪裁了图像

    # 保存剪裁后的图像
    output_path = 'path_to_output_cropped_image.jpg'
    cv2.imwrite(output_path, cropped_image)

    print("Cropped image saved successfully.")


# 增强图像
def enhance(file_name):
    # 进行直方图均衡化
    # equalized_image = cv2.equalizeHist(image)
    file_path = 'cut/' + file_name
    image = cv2.imread(file_path)
    # print(type(image))
    # cv2.imshow('Original Image', image)

    # 对比度拉伸
    # enhanced_image = cv2.convertScaleAbs(image, alpha=1.3, beta=-30)

    # 将图像转换为灰度
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 定义阈值，将灰色区域变成黑色
    threshold = 230  # 调整阈值以达到想要的效果
    # enhanced_image = np.where(gray_image > threshold, [0, 0, 0], image)

    # 将灰色区域变成黑色
    image[gray_image <= threshold] = [0, 0, 0]

    new_file_path = 'enhanced/' + file_name
    cv2.imwrite(new_file_path, image)
    return new_file_path


# 增强所有图像
def enhance_all():
    # 打开文件夹里的所有文件
    folder_path = "cut"
    files = os.listdir(folder_path)
    for file in files:
        enhance(file)


dr = '多肉:'
cz = '橙子:'


# 将图像内容识别成strs
def img_to_strs(file_name) -> list[str]:
    # 将识别语言设置为中文
    # tessdata_dir_config = '--tessdata-dir "D:/softwares/tesseract/tessdata" -l chi_sim'
    # language = 'chi_sim'

    ret = []
    # 打开图像文件 并打印日期
    file_path = 'enhanced/' + file_name
    image = Image.open(file_path)
    date = '2023-' + file_name[:-4]
    ret.append('\n')
    ret.append(date)
    ret.append('\n')
    # print()
    # print(date)
    # print()

    # 使用Tesseract进行文字识别,并使用lang识别中文简体
    text = pytesseract.image_to_string(image, lang='chi_sim')
    pars = text.split('\n')

    # 设置模式串和替换串
    speaker = 1
    first_sen = True

    dr_origin1 = r'.*幸\)'
    dr_origin2 = r'^多肉.*$'

    cz_origin = r'.*信'

    # year = r'[0-9]{1,4}年'
    date = r'[0-9]{1,2}月[0-9]{1,2}日'
    time = r'[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}'

    endl = r'^\n*$'
    dele = r'[(= 用)]'
    for sen in pars:
        # print(sen)
        # continue
        sen = re.sub(cz_origin, cz, sen)
        sen = re.sub(dr_origin1, dr, sen)
        sen = re.sub(dr_origin2, dr, sen)
        sen = re.sub(dele, '', sen)
        sen = re.sub(date, '', sen)
        sen = re.sub(time, '', sen)
        # sen = re.sub(year, '', sen)
        if re.match(endl, sen):
            continue
        # print(i)
        # # print('!!!!!')
        if re.match(dr, sen) and speaker == 1 or re.match(cz, sen) and speaker == 2:
            continue
        if re.match(dr, sen) and speaker == 2:
            first_sen = True
            speaker = 1
            # ret.append('\n')
            ret.append(sen)
            # print()
            # print(sen)
            continue
        if re.match(cz, sen) and speaker == 1:
            first_sen = True
            speaker = 2
            # ret.append('\n')
            ret.append(sen)
            # print()
            # print(sen)
            continue
        if not first_sen:
            sen = '    ' + sen
        ret.append(sen)
        first_sen = False
        # print(sen)
    return ret


# 将图像写进txt
def imgs_to_docx():
    # 打开文件夹里的所有文件
    date = r'[0-9]{1,4}\-[0-9]{1,2}\-[0-9]{1,2}'
    folder_path = "enhanced"
    files = os.listdir(folder_path)
    # doc = Document()
    txtfile = open('waken.txt', 'a')
    for file in files:
        # if not file.count('7'): continue
        # print('!!')
        day_talks = img_to_strs(file)
        for sen in day_talks:
            txtfile.write(sen)
            # 如果sen是提示语 则不换行
            if sen != dr and sen != cz:
                txtfile.write('\n')
            # if re.search(date, sen):
            # right
            # else:
            # left
        # doc.add_paragraph(sen)
    # doc.save('waken.docx')
    txtfile.close()


if __name__ == '__main__':
    # file = '11-14.jpg'
    # new_file = cut(file)
    # print_img(new_file)
    # cut_all()
    # enhance_all()
    # imgs_to_docx()
    print('end of programming')

from fontTools.ttLib import TTFont
from os import path, makedirs, getcwd, remove
import re, requests, time
import numpy as np

#已知字典
maoyan_dict = {
    'uniE101': '0',
    'uniE687': '1',
    'uniEA2A': '2',
    'uniEB4C': '3',
    'uniE69A': '4',
    'uniF339': '5',
    'uniF252': '6',
    'uniF18E': '7',
    'uniF6A6': '8',
    'uniE5DD': '9'
}
write_path = 'cache'
cur_path = ''

# 获取字体坐标
# get font axis
def getAxis(font):
    uni_list = font.getGlyphOrder()[2:]
    font_axis = []
    for uni in uni_list:
        axis = []
        for i in font['glyf'][uni].coordinates:
            axis.append(i)
        font_axis.append(axis)
    return font_axis

# 获取对比字体文件
base_font = TTFont('test.woff')
uni_base_list = base_font.getGlyphOrder()[2:]
base_axis = getAxis(base_font)
base_font = None

# 使用该函数获取当前页面动态字体
# get current font by use this function
def getFont(response):
    font_url = 'http:' + re.search(r"url\('(.*\.woff)'\)", response).group(1)
    font_file = requests.get(font_url).content
    writeFont(font_file)
    return parseFont()

# save .woff
def writeFont(font_file):
    global cur_path
    if not path.exists(write_path):
        makedirs(write_path)
    cur_path = path.join(write_path, str(time.time()) + '.woff')
    with open(cur_path, 'wb') as f:
        f.write(font_file)

# 获取当前页面动态字体的字典
def parseFont():
    print('open:\t' + cur_path)
    cur_font = TTFont(cur_path)
    uni_list = cur_font.getGlyphOrder()[2:]
    cur_axis = getAxis(cur_font)
    font_dict = {}
    for i in range(len(uni_list)):
        min_avg, uni = 99999, None
        for j in range(len(uni_base_list)):
            avg = compare_axis(cur_axis[i], base_axis[j])
            if avg < min_avg:
                min_avg = avg
                uni = uni_base_list[j]
        font_dict['&#x' + uni_list[i][3:].lower() +';'] = maoyan_dict[uni]
    remove(cur_path)
    return font_dict

# 使用欧式距离计算
# axis1 与 axis2 分别代表着两个字体的坐标
def compare_axis(axis1, axis2):
    # 以坐标（0，0）补填空缺
    if len(axis1) < len(axis2):
        axis1.extend([0,0] for _ in range(len(axis2) - len(axis1)))
    elif len(axis2) < len(axis1):
        axis2.extend([0,0] for _ in range(len(axis1) - len(axis2)))
    # 将列表转换为 Numpy 中的数组
    axis1 = np.array(axis1)
    axis2 = np.array(axis2)
    # 计算并返回欧式距离
    return np.sqrt(np.sum(np.square(axis1-axis2)))

def test():
    global cur_path
    cur_path = 'cache\\1579398826.1402967.woff'
    parseFont()

if __name__ == "__main__":
    test()

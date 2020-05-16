# -*-coding：utf-8 -*-
# BY WANGCC

from requests_html import HTMLSession, Element

session = HTMLSession()
r = session.get(url='http://www.goubanjia.com/')

tbody = r.html.find("tbody")[0]
trs = tbody.find("tr")


def f(el):
    return not any(el.find("[style='display: none;']")) and not any(el.find("[style='display:none;']"))


# 根据class的value解析出正确的port，几行代码搞定相比java灵活不少，python万岁
def parse_port(port_element):
    port_list = []
    # 循环value值
    for letter in port_element:
        # 直接确定到value的该字母在val的第几个下标，转成str添加到port list
        port_list.append(str(val.find(letter)))
    # python标准list转str方法
    port = "".join(port_list)
    # 右移3位
    return int(port) >> 0x3


# 通过js得知port的加密是span的class的值相对应一下val的位置再进行右移0x3得出正确端口
# 比如span<class='GEA'>相对应的port为 G=6 E=4 A=0 得出640 右移0x3得出 80(640>>0x3)
val = 'ABCDEFGHIZ'
ip_list = []
# 循环所有列
for tr in trs:
    # 找到列的所有格
    tds = tr.find("td")
    # 对第一格的内容进行display none 过滤
    ips = filter(f, tds[0].find())
    # 转换成list
    ips = list(ips)
    real_ip = ""
    # 循环每个tr的第一个td的值，最后一个除外
    for ip in ips[:-1]:
        # 直接将text拼凑起来
        real_ip += ip.text.replace("\n", "")
    # 最后一个element为port element，里面的attrs的class的第二个元素就是我们需要的class='value'的value
    port_class = ips[-1].attrs.get('class')[1]
    # 解析port
    real_port = str(parse_port(port_class))
    # 添加到ip上
    real_ip = real_ip+':'+real_port
    # 添加到ip list,第三个td的text就是协议 如http
    ip_list.append(f"{real_ip}")
print(ip_list)
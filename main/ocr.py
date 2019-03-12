import urllib.request
import urllib.parse
import json
import time
import base64
import re


def posturl(headers, url, data={}):
  try:
    params=json.dumps(data).encode(encoding='UTF8')
    req = urllib.request.Request(url, params, headers)
    r = urllib.request.urlopen(req)
    html =r.read()
    r.close()
    return html.decode("utf8")
  except urllib.error.HTTPError as e:
      print(e.code)
      print(e.read().decode("utf8"))
  time.sleep(1)


def read_lists_from_single_picture(file_name):
    with open(file_name, 'rb') as f:  # 以二进制读取本地图片
        data = f.read()
        encodestr = str(base64.b64encode(data), 'utf-8')

    # 请求头
    headers = {
        'Authorization': 'APPCODE ed25f43002f94b2a934186542eaacc51',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    url_request = "https://ocrapi-advanced.taobao.com/ocrservice/advanced"
    dict = {'img': encodestr, "charInfo": False}

    html = str(posturl(headers, url_request, data=dict))
    pattern = re.compile(r'"word":"([^"]*)"')
    tt = pattern.findall(html)
    return tt


def get_number_and_time_from_single_picture(file_name):
    tt = read_lists_from_single_picture(file_name)
    i = -1
    for each in tt:
        i = i + 1
        if '公里' in each:
            break
    return tt[i-1].strip(), tt[i-2].strip()


def get_number_and_name_from_single_picture(file_name):
    tt = read_lists_from_single_picture(file_name)
    number = ''
    name = ''
    for each in tt:
        if '欢迎您回来' in each:
            pattern = re.compile(r'欢迎您回来，([^，]*)，')
            name = pattern.findall(each)[0]
        if '小时' in each:
            pattern = re.compile(r'(.*)小时')
            number = pattern.findall(each)[0]
    return number.strip(), name.strip()


if __name__ == '__main__':
    # print(str(read_lists_from_single_picture('/home/loheagn/Desktop/深度截图_选择区域_20190311213209.png')))
    print(str(get_number_and_time_from_single_picture('/home/loheagn/Desktop/微信图片_20190311195526.png')))
    # print(str(get_number_and_name_from_single_picture('/home/loheagn/Desktop/深度截图_选择区域_20190311213209.png')))

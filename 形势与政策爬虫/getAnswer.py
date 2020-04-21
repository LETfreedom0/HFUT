import requests
import random
import json

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    # Firefox
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        # Safari
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        # chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        # 淘宝浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        # 猎豹浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        # QQ浏览器
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        # sogou浏览器
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        # maxthon浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
        # UC浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
]

def to_requests(url,cookie,host,referer,data):
    headers = {
        'User-agent': random.choice(USER_AGENTS),
        'Cookie': cookie,
        'Connection': 'close',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Host': host,
        'Referer': referer
    }
    req = requests.post(url, data=data, headers=headers)
    
    return req

def get_question():

    # 设置cookie用于登录获取题目 
    cookie = ""
    url = 'https://hfut.xuetangx.com/inner_api/homework/paper/subject/'
    host = 'hfut.xuetangx.com'
    referer = 'https://hfut.xuetangx.com/lms'

    # 需要F12后在network中查看headers下的data信息
    data = {
        "product_id":"",
        "homework_id":"",
        "class_id":""
    }

    req = to_requests(url,cookie,host,referer,data)

    # 将返回信息保存到本地，以便网络出问题分离操作
    file = open("11.txt", mode='w')
    file.write(req.text)
    file.close()

    question_tmp = json.loads(req.text)
    question=question_tmp['data']['question_data']
    return question

def get_question_from_txt(addr):
    f=open(addr,"r", encoding='gbk')
    question_tmp=f.read()
    f.close()
    question_tmp = json.loads(question_tmp)
    question=question_tmp['data']['question_data']
    return question
    
def get_answer(question):
    url = 'http://shuakeya.top/api/web.php'
    cookie = ''
    host = 'shuakeya.top'
    referer = 'http://shuakeya.top/'
    file = open("22.txt", mode='w')
    cnt=1
    for i in question:
        print("----第 %d 题----" %cnt)
        print("question: "+i['stem'])
        data = {
            "q":i['stem']
        }
        req = to_requests(url,cookie,host,referer,data)
        if req.status_code == 200:
            tmp0 = req.text.encode('ascii').decode('gbk')
            tmp1 = json.loads(tmp0)
            print("answer: "+tmp1['data']['answer'].strip('<br>'))
            print('\n')
            file.write("第"+str(cnt)+"题 :")
            file.write(str(tmp1['data']['answer']).strip('<br>')+'\n')
            file.flush()
            cnt = cnt + 1
        else:
            print("ERROR:"+str(req.status_code))
            break

if __name__ == '__main__':
    #question = get_question()
    question = get_question_from_txt("11.txt")
    #print(question)
    get_answer(question)

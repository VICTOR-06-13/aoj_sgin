import hashlib
import re
import requests

url = 'https://acm.webturing.com/login.php'
logout_url = 'https://acm.webturing.com/logout.php'
sign_url = 'https://acm.webturing.com/postFunction.php?action=sign'
wallet_url = 'https://acm.webturing.com/wallet.php'


def server_push(push_information, push_url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"}
    requests.get(push_url + '?text=' + push_information + '&desp=服务器正常', headers=headers)


def sign(user_id, password, sckey):
    md5_password = hashlib.md5(password.encode()).hexdigest()
    username_url = 'https://acm.webturing.com/userinfo.php?user=' + user_id
    push_url = 'https://sc.ftqq.com/' + sckey + '.send'
    data = {
        "user_id": user_id,
        "password": md5_password,
        "submit": ""
    }
    cookies = 'lastlang=13; ' + str(requests.Session().post(url, data=data).cookies)[27:63]
    headers_sign = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": cookies,
        "DNT": "1",
        "Host": "acm.webturing.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"
    }

    # 签到
    response = requests.get(sign_url, headers=headers_sign).text
    wallet_response = requests.get(wallet_url, headers=headers_sign).text
    wallet = str(re.search(r'<strong>(\d+)枚', wallet_response).group())[8:]
    username = requests.get(username_url, headers_sign).text
    name = re.search(r'<span class=\'\'>.*?</span>', username).group()[15:-7]
    if response == '今天已经签到过啦，赶紧去A题吧~\n\n':
        push_information = name + '已经签到过了,' + '钱包里有' + wallet + '图灵币'
        server_push(push_information, push_url)
    else:
        sign_end = re.search(r'(\d+)', response).group()
        push_information = name + '签到成功，已获得' + sign_end + '枚图灵币，钱包里有' + wallet + '图灵币'
        server_push(push_information, push_url)

    # 退出登录
    requests.get(logout_url, data=data, headers=headers_sign)

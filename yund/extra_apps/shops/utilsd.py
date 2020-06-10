from django.db.models import Q
from yund.settings import *
from .models import *
import random
import time
from .views import *
import jwt
import datetime
import urllib
import urllib.request

def dfilter(*args):
    """搜索多条件构建"""
    q=Q()
    args=args[0]
    for i in args:
        if i == 'city':
            continue
        q.add(Q(**{i: args[i]}), Q.AND)
    q.add(Q(**{'is_del': 0}), Q.AND)
    return q

def send_sms(*args):
    """链接短信
    text: 内容
    mobile: 电话
    """
    text,mobile = args
    params=urllib.parse.urlencode(
        {'account': settings.APIID, 'password': settings.APIKEY, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers={"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn=http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response=conn.getresponse()
    response_str=response.read()
    conn.close()
    return response_str

def send_sms1(*args):
    """链接短信
    text: 内容
    mobile: 电话
    """

    statusStr = {
        '0': '短信发送成功',
        '-1': '参数不全',
        '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
        '30': '密码错误',
        '40': '账号不存在',
        '41': '余额不足',
        '42': '账户已过期',
        '43': 'IP地址限制',
        '50': '内容含有敏感词'
    }

    smsapi = "http://api.smsbao.com/"
    
    # 短信平台账号
    user = settings.APIUSER
    # 短信平台密码
    password = settings.APIPASSWOED

    content,phone = args

    data = urllib.parse.urlencode({'u': user, 'p': password, 'm': phone, 'c': content})

    send_url = smsapi + 'sms?' + data

    response = urllib.request.urlopen(send_url)

    the_page = response.read().decode('utf-8')

    print (statusStr[the_page])

def sends(tep):
    """发短信"""
    str=sixnum(4)

    text="您的验证码是："+str+"。请不要把验证码泄露给其他人。"
    ret=send_sms1(text, tep)
    return str

def sixnum(num):
    """六位随机"""
    str=""
    for i in range(num):
        ch=chr(random.randrange(ord('0'), ord('9') + 1))
        str += ch
    return str

def upload_allimg(img):
    """上传图片"""
    print(img)
    f = open(os.path.join(UPLOAD_ROOT,'',img.name),'wb')
    for chunk in img.chunks():
        f.write(chunk)
    f.close()

def ninthnum():
    """mm号生成"""
    num=sixnum(9)
    try:
        user_tep=Users.objects.filter(mmh=num).first()
        if user_tep:
            return ninthnum()
    except:
        pass
    return num

def get_order_code():
    """订单号生成"""
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
    order_no='XH'+order_no
    return order_no


def get_token(payload,timeout):
    headers = {
            "typ": "jwt_",
            "alg": "HS256",
        }
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    token = jwt.encode(payload=payload, key=settings.SECRET_KEY, headers=headers).decode("utf-8")
    return token


def tags(request_data):
    """商品标签"""
    for i in range(len(request_data)):
        taglist=[]
        taglist.append('公司')
        taglist.append(request_data[i]['city'])
        if request_data[i]['brand'] == '1':
            taglist.append('品牌')
        if request_data[i]['old_new'] == 0:
            taglist.append('二手')
        if request_data[i]['old_new'] == 1:
            taglist.append('全新')
        request_data[i]['tags'] = taglist
    return request_data


def splits(data):
    if len(data) != 1:
        data=data.split(',')
    else:
        data = [data]
    return data

def cached(*args):
    tep,time,str=args
    userdics={
        tep:{
            'str':str,
            'time':time
        }
    }
    return userdics

def str2sec(x):
    '''
    字符串时分秒转换成秒
    '''
    h, m, s = x.strip().split(':') #.split()函数将其通过':'分隔开，.strip()函数用来除去空格
    return int(h)*3600 + int(m)*60 + int(s) #int()函数转换成整数运算

def isstr(*args):
    mes={}
    strs,tep,str1=args
    strs=eval(strs)
    times=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    times=datetime.datetime.strptime(times,'%Y-%m-%d %H:%M:%S')
    time=datetime.datetime.strptime(strs[tep]['time'],'%Y-%m-%d %H:%M:%S')
    a =str(times-time)
    nums = str2sec(a)
    if nums > 60:
        mes={
            'code':0,
            'msg':'验证码失效'
        }
    elif str1 != strs[tep]['str']:
        mes={
            'code':0,
            'msg':'验证码错误'
        }
    else:
        mes={
            'code':'200',
            'msg':'正确'
        }
    return mes
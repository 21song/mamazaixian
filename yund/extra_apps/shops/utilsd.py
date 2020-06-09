from django.db.models import Q
from yund.settings import *
from .models import *
import random
import time
from .views import *
import jwt
import datetime

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

def sends(tep):
    """发短信"""
    str=sixnum(4)
    text="您的验证码是："+str+"。请不要把验证码泄露给其他人。"
    ret=send_sms(text, tep).decode('utf-8')
    ret=json.loads(ret)
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

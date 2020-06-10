from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data,BucketManager
import uuid
from PIL import Image
import io


def upload(img):   # img是文件
    _img = img.read()
    size = len(_img) / (1024 * 1024)#上传图片的大小 M单位
    print('size:',size)
    image = Image.open(io.BytesIO(_img))
    key = str(uuid.uuid1().hex) + '.' + image.format
    print('key:',key)
    access_key = 'Ka5DV-q4fp9V-kV31vb7KekwD3A6WjV_sWuJGB7W'
    secret_key = 'Ta-n9rWOf6-trUe7iX4WouOY4Gmb0h6M1BTciBbf'
    q = Auth(access_key, secret_key)
    bucket_name = 'banluyuan'
    token = q.upload_token(bucket_name, key, 3600, )  #生成上传 Token，可以指定过期时间等
    name = 'upfile.{0}'.format(image.format) #获取图片后缀（图片格式）
    if size > 1:
        x, y = image.size
        im = image.resize((int(x / 1.73), int(y / 1.73)), Image.ANTIALIAS) #等比例压缩 1.73 倍；抗锯齿
        print('压缩')
    else:
        print('不压缩')
        im = image
    im.save('service/media/' + name) #在service目录下有个media文件夹，先保存在本地，再上传
    path = 'service/media/' + name

    ret, info = put_file(token, key, path)
    # print(info)
    url = 'http://qiniu.banluyuan.com/{}'.format(key)
    return url

# 测试upload,成功
# with open("4971.jpg", "rb") as imageFile:
#     url = upload(imageFile)
#     print(url)

def delete_img(img_url):  # img_url形如：http://qiniu.banluyuan.com/beb4fd86a56011eab5536014b35d1592.JPEG
    access_key = 'Ka5DV-q4fp9V-kV31vb7KekwD3A6WjV_sWuJGB7W'
    secret_key = 'Ta-n9rWOf6-trUe7iX4WouOY4Gmb0h6M1BTciBbf'
    # 初始化Auth状态
    q = Auth(access_key, secret_key)
    # 初始化BucketManager
    bucket = BucketManager(q)
    # 你要测试的空间， 并且这个key在你空间中存在
    bucket_name = 'banluyuan'
    key = img_url.split('/')[-1]
    # 删除bucket_name 中的文件 key
    ret, info = bucket.delete(bucket_name, key)
    # print(info)
    return str(info)
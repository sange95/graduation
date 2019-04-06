import logging
import sys
sys.path.append('/root/.virtualenvs/py3_flask1/lib/python3.5/site-packages')
from qiniu import Auth, put_data


# 需要填写自己的Access Key 和 Secret Key
access_key = 'qZbOjg3C4Af1UMEu-Zr2Ro4ylW58CoSVJ12gkpiT'
secret_key = 'n4m6h04KPAYPT3_jY6vZsU494GSwjO3c8pNSYgUX'

# 要上传的空间
bucket_name = 'data2'




def storage(data):
    """七牛云存储上传文件接口"""
    if not data:
        return None
    try:
        # 构建鉴权对象
        q = Auth(access_key, secret_key)

        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name)

        # 上传文件
        ret, info = put_data(token, None, data)

    except Exception as e:
        logging.error(e)
        raise e

    if info and info.status_code != 200:
        raise Exception("上传文件到七牛失败")



    # 返回七牛中保存的图片名，这个图片名也是访问七牛获取图片的路径
    return ret["key"]


if __name__ == '__main__':
    file_name = input("输入上传的文件")
    with open(file_name, "rb") as f:
        print(storage(f.read()))
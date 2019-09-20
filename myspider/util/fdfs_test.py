# coding=utf8
from fdfs_client.client import Fdfs_client
import requests

def main():
    client = Fdfs_client('client.conf')
    pic_url = 'http://pic25.nipic.com/20121112/9252150_150552938000_2.jpg'
    pic_res = requests.get(url=pic_url)
    res = client.upload_appender_by_buffer(pic_res.content,file_ext_name='jpg')
    print(res)


if __name__ == '__main__':
    main()


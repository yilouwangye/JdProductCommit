# !usr/bin/env python
# -*-coding:utf-8 -*-

# @FileName: crawl.py
# @Author:tian
# @Time:06/06/2020

from mitmproxy import ctx
import json
from pymongo import MongoClient

def response(flow):
    client = MongoClient(host='127.0.0.1',port=27017)
    db = client['country']
    col = db['jd_product']
    url = 'https://120.52.83.22/client.action?functionId=getCommentListWithCard&clientVersion'
    if url in flow.request.url:
        text = flow.response.text
        data = json.loads(text)
        '''d.get(key,value),key不存在时，可以设置对应值'''
        image = [{'picURL':'该用户暂未提交评论图片'}]
        items = data.get('commentInfoList')
        for item in items:
            item = item.get('commentInfo')
            data = {
                'user_name': item.get('userNickName'),
                'user_image':item.get('userImgURL'),
                'model': item.get('wareAttribute')[1].get('型号') + '，' + item.get('wareAttribute')[0].get('颜色'),
                # 'model': item.get('wareAttribute'),   # 京东通用属性值
                'date': item.get('commentDate'),
                'content': item.get('commentData').replace('\n',''),
                'image':[i.get('picURL') for i in item.get('pictureInfoList',image)]
            }
            ctx.log.info(str(data))
            col.update({'user_name':item.get('userNickName')},{'$set':data},True)
    else:
        ctx.log.info(str('----------筛选数据中----------'))


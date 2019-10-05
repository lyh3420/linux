#!/usr/bin/python3
# _*_ coding:utf-8 _*_
'''
 'corpid': '**************' 企业ID
 'corpsecret': '**********************************************' TOKEN hash
 'agentid': ********,     application ID
'''
import os
import sys
import time
import json
import pickle
import requests
basedir = os.path.abspath(os.path.dirname(__file__))
class WeChatMsg(object):
    def __init__(self,username,content):
        self.get_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        self.send_msg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
        self.access_token_cache = os.path.join(basedir,'access_token_cache')
        self.get_token_content = {
                            'corpid': '**************',
                            'corpsecret': '**********************************************'
                            }
        self.main_text_content = {
                           'touser': username,
#                           'toparty': username,
                           'msgtype': 'text',
                           'agentid': ********,
                           'text': {
                                'content': content,
                                }
                            }

    def _get_new_token(self):
        req = requests.get(url=self.get_token_url,params=self.get_token_content)
        access_token = json.loads(req.content)['access_token']
        current_time = int(time.time())
        return access_token,current_time

    def _dump_token(self):
        with open(self.access_token_cache,'wb') as f:
            access_token,current_time = self._get_new_token()
            data = {'access_token':access_token,
                'token_time':current_time}
            pickle.dump(data,f)

    def _get_old_token(self):
        if os.path.isfile(self.access_token_cache):
            with open(self.access_token_cache,'rb') as f:
                data = pickle.load(f)
                access_token = data.get('access_token')
                token_time = data.get('token_time')
        else:
            access_token,token_time = self._get_new_token()
            self._dump_token()
        return access_token,token_time

    def get_token(self):
        old_access_token,old_token_time = self._get_old_token()
        current_time = int(time.time())
        if current_time - old_token_time >= 7200:
            access_token,token_time = self._get_new_token()
            self._dump_token()
            return access_token
        else:
            return old_access_token

    def send_msg(self):
        url = '{0}?access_token={1}'.format(self.send_msg_url,self.get_token())
        data = self.main_text_content
        print(data)
        req = requests.post(url=url, data=json.dumps(data,ensure_ascii=False))
        return req.status_code, req.content

if __name__ == '__main__':
    if len(sys.argv) == 4:
        username, subject, text = sys.argv[1:]
        content = '{0}\n{1}'.format(subject, text)
        wesener = WeChatMsg(username, content.encode('utf-8').decode('latin-1'))
        status_code, text = wesener.send_msg()
    else:
        msg = 'Usage:\n     {0}  "username" "subject" "text"'.format(sys.argv[0])
        print(msg)
        sys.exit()


#!/usr/bin/env python
# coding: utf-8

from wxbot import *#导入类函数
import ConfigParser
import json
import datetime

class TulingWXBot(WXBot):#图灵key的读入
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = ""
        self.robot_switch = True

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')#对配置文件写入
        except Exception:
            pass
        print 'tuling_key:', self.tuling_key



    def tuling_auto_reply(self, uid, msg):
        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api"
            user_id = uid.replace('@', '')[:30]
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = ''
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
            elif respond['code'] == 200000:
                result = respond['url']
            else:
                result = respond['text'].replace('<br>', '  ')

            print '    ROBOT:', result
            return result
        else:
            return u"有点忙，回聊哦。"

    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        start_cmd = [u'出来', u'启动', u'工作']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])

    def handle_group_message(self, msg, group):
        import pdb
        pdb.set_trace()
        message_list = []
        content = msg['content']['data'].replace("\n", "")
        # self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
        self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], content), msg['user']['id'])
        if msg['content']['data'].replace("\n", "") != u'DONE':
            message_list.append(msg)
            pass
        if message_list != []:
            with open(os.path.join(self.temp_pwd, group['PYInitial']+'.txt'), 'a') as f:
                # f.write(msg['content']['data'].encode("utf-8"))
                f.write(json.dumps(message_list))
                f.write('\n\n*************************separator*************************\n\n')
            pass
            pass

        if msg['content']['data'].replace("\n", "") == u'DONE':
            with open(os.path.join(self.temp_pwd, group['PYInitial']+'.txt'), 'r') as f:
                text = f.read()
                with open(os.path.join(self.temp_pwd, group['PYInitial']+'_tmp.txt'), 'w') as f:
                    # f.write(msg['content']['data'].encode("utf-8"))
                    f.write(text)
                print "---------- 删除上次，存下本次 ----------"
                text = text.replace("\n", "")
                text_list = text.split("*************************separator*************************")
                if text_list:
                    if text_list[-1] == '':
                        text_list.pop()
                        self.parse_group_message(text_list, group)
                        pass
                    pass
            pass

    def parse_group_message(self, text_list, group):
        group_id = group['UserName']
        group_members = self.group_members[group_id]
        member_dict = {}
        for member in group_members:
            member_id = member['UserName']
            member_dict[member_id] = member
            pass
        new_text_list = {}
        for text in text_list:
            text_info = json.loads(text)[0]
            # user_id = json.dumps(text_info['content']['user']['id'])
            # msg_id = json.dumps(text_info['msg_id'])
            # user_id = user_id.replace("\"","")
            # msg_id = msg_id.replace("\"","")
            user_id = text_info['content']['user']['id'].encode('utf8')
            msg_id = text_info['msg_id'].encode('utf8')
            user = member_dict[user_id]
            # new_text = {'content': json.dumps(text_info['content']['data']).replace("\"", "")}
            new_text = {'user': user, 'content': text_info['content']['data']}
            new_text_list[msg_id] = new_text
            pass
        time_stramp = datetime.datetime.now().strftime('%Y%m%d')
        message_dict = {}
        message_dict[time_stramp] = new_text_list
        message_dict['group_nickname'] = group['NickName'].encode('utf8')
        messages = json.dumps(message_dict)
        import pdb
        pdb.set_trace()
        with open(os.path.join(self.temp_pwd, 'messages.txt'), 'a') as f:
            f.write(messages)
            f.write('\n\n=========================separator=========================\n\n')
        print "---------- 已存 ----------"
        with open(os.path.join(self.temp_pwd, group['PYInitial']+'.txt'), 'w') as f:
            # f.write(msg['content']['data'].encode("utf-8"))
            f.write('')
        print "---------- 已删 "+group['PYInitial'].encode('utf8')+".txt ----------"
        self.display_reports()
        
    def display_reports(self):
        with open(os.path.join(self.temp_pwd, 'messages.txt'), 'r') as f:
            text = f.read()
            text = text.replace("\n", "")
            text_list = text.split("=========================separator=========================")
            if text_list:
                if text_list[-1] == '':
                    text_list.pop()
                    print text_list
                    pass
                pass

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            # reply = u'我就是我'
            # for group in self.group_list:
            #     if group['NickName'] == u'我要吃好吃的':
            #         group_id = group['UserName']
            #         group_title = group['PYInitial']
            #         pass
            # if msg['to_user_id'] == group_id:
            #     self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['to_user_id'])
            #     message_list.append(msg)
            #     with open(os.path.join(self.temp_pwd,group_title+'.txt'), 'a') as f:
            #         # f.write(msg['content']['data'].encode("utf-8"))
            #         f.write(json.dumps(message_list))
            #         f.write(',\n\n')
            #     pass
            # if msg['to_user_id'] != group_id:
            #     self.send_msg_by_uid(reply, msg['user']['id'])
            #     pass
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            # self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
            print "========================= 什么都没有 ========================="
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            with open(os.path.join(self.temp_pwd, 'group_name.txt'), 'r') as f:
                groups = f.read()
                groups = groups.decode('utf8')
                group_array = groups.split("\n")
            pass
            for group in self.group_list:
                if group['NickName'] in group_array:
                    print "group name ---- "+group['NickName']
                # if group['NickName'] == u'我要吃好吃的':
                    if msg['user']['id'] == group['UserName']:
                        self.handle_group_message(msg, group)
                    pass
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(self.my_account['UserName'], msg['user']['id'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break
                if is_at_me:
                    src_name = msg['content']['user']['name']
                    reply = 'to ' + src_name + ': '
                    if msg['content']['type'] == 0:  # text message
                        reply += self.tuling_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                    else:
                        reply += u"对不起，读的书少，不认识你发的乱七八糟的东西。"
                    self.send_msg_by_uid(reply, msg['user']['id'])


def main():
    bot = TulingWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
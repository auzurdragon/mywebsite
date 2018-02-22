#! coding:utf8
"""
    微信处理, itchat
"""

def login():
    """
        初始化
    """
    import itchat
    itchat.auto_login(hotReload=True, picDir='mynote/templates/')
    self.msglog = []   # 保存接到的消息记录
    self.friends = []

@itchat.msg_register([TEXT, ATTACHMENT, CARD, FRIENDS, MAP, NOTE, PICTURE, RECORDING, SHARING, SYSTEM, VIDEO])
def get_text(msg):
    from itchat.content import *
    print(msg)
    self.msglog.append(dict({"msg_type":"text"} ** msg))


if __name__ == '__main__':
    import itchat
    from itchat.content import *
    msglog = []

    @itchat.msg_register([TEXT, ATTACHMENT, CARD, FRIENDS, MAP, NOTE, PICTURE, RECORDING, SHARING, SYSTEM, VIDEO])
    def get_msg(msg):
        msglog.append(msg)
        print(msg)

    @itchat.msg_register([TEXT, ATTACHMENT, CARD, FRIENDS, MAP, NOTE, PICTURE, RECORDING, SHARING, SYSTEM, VIDEO], isGroupChat=True)
    def get_group(msg):
        msglog.append(msg)
        print(msg)

    itchat.auto_login(hotReload=True)
    itchat.run()

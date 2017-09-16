# coding:utf-8
"""友盟消息推送接口"""

class PushAPI(object):
    def __init__(self):
        self.url = "http://msg.umeng.com/api/send?sign=mysign"
        self.requ_para = {
            "appkey":"59b7cbdcb27b0a10f8000013",
            "timestamp":"",
            "type":"listcast",
            "device_tokens":""
            "payload":{
                "display_type":"notification",
                "body":{
                    "ticker":"test",    # 通知栏提示
                    "title":"title",    # 通知标题
                    "text":"text",      # 通知文字描述
                    "play_vibrate":"true",  # 收到通知震动
                    "play_lights":"true",   # 收到通知闪灯
                    "play_sound":"true",    # 收到通知发出声音
                    "after_open":"go_url",  # 跳转url
                    "url":"http://112.74.161.9",
                },
            },
        }

    def get_sign(self):
        """获得sign签名"""
        

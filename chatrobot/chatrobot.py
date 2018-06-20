#! coding:utf8
"""
微信和QQ批量操作和自动查找优惠券
"""
import itchat
from time import strftime, localtime, time, sleep

def output_info(level, msg):
    print('%s, [%s], %s' % (strftime('%Y-%m-%d %H:%M:%S', localtime(time())), level, msg))

# def login():
def qr_print(uuid, status, qrcode):
    """
    处理QR图片
    """
    print(uuid)
    print(status)
    print(qrcode)

uuid = itchat.get_QRuuid()  # 生成uuid
itchat.get_QR(uuid=uuid, qrCallback=qr_print)   # 生成二维码图片
check = itchat.check_login(uuid)
if check == '200':   # 登录成功
    itchat.web_init()   # 初始化
    itchat.get_contact()   # 更新相关信息，获得联系人列表
    itchat.show_mobile_login()  # 在手机微信上显示登录状态
    itchat.start_receiving()    # 开始循环扫描新消息
    itchat.run(debug=True)    # 开始后台运行
else:
    output_info('E', f'check_login failed : {check}')





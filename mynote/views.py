from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.files.storage import FileSystemStorage as fs

# Create your views here.



def weixin_login(request):
    import itchat, qrcode, time, threading
    def save_qr(uuid, status, qrcode):
        with open('./mynote/static/%s' % fname, 'wb') as w:
            w.write(qrcode)
    uuid = itchat.get_QRuuid()
    fname = '%s.png' % uuid
    print(fname)
    itchat.get_QR(uuid=uuid, qrCallback=save_qr)
    while True:
        status = itchat.check_login(uuid)
        if status == '200':
            print("OK")
            break
        else:
            print(status)
    # uuid = itchat.get_QRuuid()
    # try:
    #     itchat.get_QR(uuid=uuid, picDir='./mynote/static/%s' % fname)
    # except Exception as e:
    #     print(e)
    # # qrimg = qrcode.make('https://login.weixin.qq.com/l/%s' % uuid)
    # # qrimg.save('./mynote/static/%s' % fname)
    # finally:
    #     lock = threading.Lock()
    #     def weixin_check(uuid):
    #         import itchat
    #         try:
    #             while True:
    #                 status = itchat.check_login(uuid)
    #                 if status == '200':
    #                     print(status)
    #                     lock.release()
    #                     break
    #                 else:
    #                     print(status)
    #         except Exception as e:
    #             print(e)
    #         finally:
    #             return status
    #     t = threading.Thread(target=weixin_check, args=(uuid,))
    #     t.start()
    #     userinfo = itchat.web_init()
        # itchat.get_contact()
        # itchat.start_receiving()
    # print(itchat.get_friends())
    return render(request, 'img_temp/weixin_login.html', {'fname':fname, 'uuid':uuid})

def weixin_check(request):
    import itchat
    print(request.GET)
    uuid = request.GET.get('uuid')
    status = itchat.check_login(uuid)
    return HttpResponse(status)

def weixin(request):
    """微信功能"""
    import itchat, time, pickle, qrcode
    # from itchat.content import *
    qrurl = 'https://login.weixin.qq.com/l/'
    picQR = '%d.png' % int(time.time())
    # 模拟itchat登录流程
    uuid = itchat.get_QRuuid()
    qrimg = qrcode.make('https://login.weixin.qq.com/l/%s' % uuid)
    qrdir = 'tt.png'
    qrimg.save(qrdir)
    return render(request, 'weixin.html', {'qrdir':qrdir} )
    # itchat.auto_login(hotReload=True, picDir=picQR)
    # flist = itchat.get_friends()
    # with open('flist.pkl', 'wb') as w:
    #     pickle.dump(flist, w)
    # clist = [{'username':i['UserName'], 'nickname':i['NickName'], 'sign':i['Signature'], 'sex':i['Sex'], 'province':i['Province'], 'city':i['City']} for i in flist[1:-2]]
    # return render(request, 'weixin.html', {'picqr':picQR, 'clist':clist})
    

    

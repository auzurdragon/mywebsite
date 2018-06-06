from django.shortcuts import render, render_to_response
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage as fs

# Create your views here.

def weixin_login(request):
    """
        微信登录，判断是否带有UUID，不带则加载登录模板。带UUID则用UUID检查登录是否成功。使用JS脚本发送带UUID的请求
    """
    import itchat, time, base64, json
    def save_qr(uuid, status, qrcode):
        # with open('%s%s' % (qrpath,fname), 'wb') as w:
        #     w.write(qrcode)
        pass
    eventid = request.GET.get('eventid')
    result = {
        'check':False,
        'uuid':'',
        'status':'0',
        'errMsg':'',
        'result':'',
    }
    if eventid == "start":
        try:
            uuid = itchat.get_QRuuid()
            qrcode = itchat.get_QR(uuid = uuid, qrCallback=save_qr)
            qrcode = base64.b64encode(qrcode.getvalue())
            result['uuid'] = uuid
            response = HttpResponse(qrcode)
            response.set_cookie('uuid', uuid)
            return response
        except Exception as e:
            result['errMsg'] = e
            response = HttpResponse()
        finally:
            print(result)
            return response
    elif eventid == "login":
        print(request.COOKIES)
        try:
            uuid = request.COOKIES['uuid']
            result['status'] = itchat.check_login(uuid)
            print(result['status'])
            tmp = itchat.web_init()
            result['result'] = {'user':tmp['User'],}
            itchat.show_mobile_login()
            itchat.start_receiving()
            result['result']['flist'] = itchat.get_friends()
            result['check'] = True
            result['uuid'] = uuid
            print(result)
        except Exception as e:
            print(e)
        finally:
            response = HttpResponse(json.dumps(result), content_type='application/json')
            return response
    else:
        response = render_to_response('weixin_login.html',{})
        response.delete_cookie('uuid')
        return response

    # if eventid == "start":
    #     try:
    #         qrid = itchat.get_QRuuid()
    #         qrcode = itchat.get_QR(uuid=qrid, qrCallback=save_qr)
    #         qrcode = base64.b64encode(qrcode.getvalue())
    #         response = HttpResponse(qrcode)
    #         response.set_cookie(key='uuid',value=qrid)
    #     except Exception as e:
    #         result['result'] = e
    #     return response
    # elif eventid == 'login':
    #     if 'uuid' in request.COOKIES.keys():
    #         uuid = request.COOKIES['uuid']
    #         print(uuid)
    #         try:
    #             status = itchat.check_login(uuid)
    #             print(status)
    #         except Exception as e:
    #             result['result'] = e
    #             status = '0'
    #             return HttpResponse(json.dumps(e), content_type="application/json")
    #         finally:
    #             if status == '200':
    #                 try:
    #                     initinfo = itchat.web_init()
    #                     # print(initinfo)
    #                     userinfo = initinfo['User']
    #                     print(userinfo)
    #                     itchat.show_mobile_login()
    #                     itchat.start_receiving()
    #                     result['check'] = True
    #                     result['status'] = status
    #                     result['result'] = {
    #                         'userinfo':userinfo,
    #                         'result':itchat.get_friends(),
    #                     }
    #                 except Exception as e:
    #                     result['result'] = e
    #                 finally:
    #                     pass
    #             else:
    #                 result['status'] = status
    #             return HttpResponse(json.dumps(result), content_type="application/json")
    #     else:
    #         return HttpResponse(json.dumps(result), content_type="application/json")
    # else:
    #     response = render_to_response('weixin_login.html', {})
    #     response.delete_cookie('uuid')
    #     return response

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
    

    

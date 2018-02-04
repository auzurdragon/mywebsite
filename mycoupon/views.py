from django.shortcuts import render

# Create your views here.

def tb_coupon(request):
    """女装选品库"""
    from mycoupon.models import tb_coupon
    from json import loads
    clist = loads(tb_coupon.objects.to_json())
    print(clist)
    return render(request,'tb_coupon.html', {'clist':clist})

def get_tbsign(body):
    """
        生成签名字符串
        body, 传入的参数字典
        [签名方法说明](http://open.taobao.com/docs/doc.htm?spm=a219a.7395905.0.0.QW7JO2&articleId=101617&docType=1&treeId=1)
        [API说明](http://open.taobao.com/docs/api.htm?spm=a219a.7386797.0.0.p2OcOK&source=search&apiId=29821)
    """
    from hashlib import md5
    app_secret = '8f8a525b7396fbd40c6c4aa9d7f37151'
    keys = body.keys()
    keys = [i.encode('ascii') for i in body]
    keys.sort()
    signstr = '%s%s%s' % (
        app_secret,
        str().join(
            ["%s%s" % (i.decode("utf_8"), body[i.decode("utf_8")]) for i in keys]
        ),
        app_secret
    )
    signstr = md5(signstr.encode("utf_8")).hexdigest().upper()
    print(signstr)
    return signstr
def tbk_dg_item_coupon_get(q='女装', page_no=1):
    """
        tbk.dg.item.coupon.get , (好券清单API【导购】)
        [API说明](http://open.taobao.com/docs/api.htm?spm=a219a.7386797.0.0.p2OcOK&source=search&apiId=29821)
    """
    import requests
    from time import strftime, localtime, time
    api_url = 'http://gw.api.taobao.com/router/rest'
    body = {
        'method':'',
        'app_key':'24598079',
        'sign_method':'md5',
        'format':'json',
        'v':'2.0',
    }
    print(body)
    body = dict(body, ** {
        'method':'taobao.tbk.dg.item.coupon.get',
        'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
        'adzone_id':'159428618',
        'platform':1,
        'q':q,
        'page_no':page_no,
    })
    print(body)
    body['sign'] = get_tbsign(body)
    tmp = requests.post(data=body, url=api_url)
    tmp = tmp.json()
    print(tmp)

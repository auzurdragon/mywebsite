#！coding:utf-8

class coupon(object):
    """
        获得优惠券
    """
    def __init__(self):
        self.TB_app_key = '24795664'
        self.TB_app_secret = '1cc8d454b613aa6f833e36fdf246bde8'
        self.TB_adzone_id = '248444921'
    def tb_getsign(self, body):
        """
            生成签名字符串
            body, 传入的参数字典
            [签名方法说明](http://open.taobao.com/docs/doc.htm?spm=a219a.7395905.0.0.QW7JO2&articleId=101617&docType=1&treeId=1)
            [API说明](http://open.taobao.com/docs/api.htm?spm=a219a.7386797.0.0.p2OcOK&source=search&apiId=29821)
        """
        from time import time, localtime, strftime
        from hashlib import md5
        # 添加公共请求参数
        body = dict({
            'app_key':self.TB_app_key,
            'sign_method':'md5',
            'format':'json',
            'v':'2.0',
            'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
        }, ** body)
        keys = body.keys()
        keys = [i.encode('ascii') for i in body]
        keys.sort()
        signstr = '%s%s%s' % (
            self.TB_app_secret,
            str().join(
                ["%s%s" % (i.decode("utf_8"), body[i.decode("utf_8")]) for i in keys]
            ),
            self.TB_app_secret
        )
        signstr = md5(signstr.encode("utf_8")).hexdigest().upper()
        body['sign'] = signstr
        return body
    def tb_getcoupon(self, q, page_no):
        """
            tbk.dg.item.coupon.get , (好券清单API【导购】)
            [API说明](http://open.taobao.com/docs/api.htm?spm=a219a.7386797.0.0.p2OcOK&source=search&apiId=29821)
        """
        import requests
        api_url = 'http://gw.api.taobao.com/router/rest'
        body = {
            'method':'taobao.tbk.dg.item.coupon.get',
            'adzone_id':self.TB_adzone_id,    # 阿里妈妈推广位
            'q': q if q else '吉他',
            'page_no':page_no if page_no else 1,
        }
        body = self.tb_getsign(body)
        try:
            tmp = requests.post(data=body, url=api_url)
            tmp = tmp.json()
            results = tmp['tbk_dg_item_coupon_get_response']['results']['tbk_coupon']
            result_num = tmp['tbk_dg_item_coupon_get_response']['total_results']
            return (result_num, results)
        except Exception as e:
            print(e)
            return e
        

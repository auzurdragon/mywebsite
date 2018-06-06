#！coding:utf-8

import requests
from time import time, localtime, strftime
from hashlib import md5

api_url = 'http://gw.api.taobao.com/router/rest'
app_key = '24795664'
app_secret = '1cc8d454b613aa6f833e36fdf246bde8'
adzone_id  = '248444921'

def get_coupon(key='', by='keyword', page_no=1, page_size=30, sort='total_sales_desc'):
    """
    查找优惠券，使用淘宝通用物料搜索接口 [taobao.tbk.dg.material.optional](http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.7feRJP&apiId=35896)
    :param key , 按查询方法传值
    :param by , 指定查询方法， keyword-按关键字查询, cat-按类目id查询
    :param page_no , 指定查询页数, 默认1页20条
    :param page_size , 指定每页记录数量
    :param sort , 指定排序方法
    return (bool, int, [list]) , 查询是否成功, 查询记录数量, 查询结果
    """
    body = {
        'method':'taobao.tbk.dg.material.optional',
        'adzone_id':adzone_id ,    # 阿里妈妈推广位
        'page_no':page_no,
        'page_size':page_size,
        'sort': sort,
        'has_coupon':'true',
    }
    if by == 'keyword':
        if key != '':
            body.update({'q': key})
    elif by == 'cat':
        body.update({'cat': key})
    else:
        return (False, 0, [])
    body = get_sign(body)  # 进行签名
    try:
        tmp = requests.post(data=body, url=api_url)
        tmp = tmp.json()
        coupon_num = tmp['tbk_dg_material_optional_response']['total_results'] # 记录总数
        coupon = tmp['tbk_dg_material_optional_response']['result_list']['map_data'] # 当前页的记录
        # 计算券后价格
        for i in coupon:
            if i['coupon_info'] != '':
                i['coupon_price'] = float(i['zk_final_price']) - float(i['coupon_info'][i['coupon_info'].rfind('减')+1:-1])
                i['url'] = i['coupon_share_url']  # 替换淘客链接为二合一链接
            else:
                i['coupon_price'] = float(i['zk_final_price'])
        return (True, coupon_num, coupon)
    except KeyError:
        return(False, 0, tmp)
    except Exception as E:
        return (False, 0, E)
def get_tpwd(url, text='', logo=''):
    """
    taobao.tbk.tpwd.create( 淘宝客淘口令 )
    [参考文档](http://open.taobao.com/api.htm?docId=31127&docType=2&source=search)
    :param url , 淘宝链接, 必须以 https 开头，否则报错 口令跳转url不支持口令转换
    :param text , 宣传文案，复制会在手机顶部显示提示文字。
    :param logo , 弹窗logo的图片url
    """
    text = '打开手机淘宝, 马上抢券!' if text == '' else text
    body = {
        'method': 'taobao.tbk.tpwd.create',
        'text': text,  # 口令弹框内容
        'url': url,  # 口令跳转目标页面
        'logo': logo,  # 弹窗logo
    }
    body = get_sign(body)
    try:
        tmp = requests.post(url=api_url, data=body)
        tmp = tmp.json()
        return (True, tmp['tbk_tpwd_create_response']['data']['model'])
    except KeyError:
        return (False, tmp)
    except Exception as E:
        return (False, E)
def get_sign(body):
    """
        生成签名字符串
        body, 传入的参数字典
        [签名方法说明](http://open.taobao.com/docs/doc.htm?spm=a219a.7395905.0.0.QW7JO2&articleId=101617&docType=1&treeId=1)
        [API说明](http://open.taobao.com/docs/api.htm?spm=a219a.7386797.0.0.p2OcOK&source=search&apiId=29821)
    """
    # 添加公共请求参数
    body.update({
        'app_key':app_key,
        'sign_method':'md5',
        'format':'json',
        'v':'2.0',
        'timestamp':strftime('%Y-%m-%d %H:%M:%S', localtime(time())),
    })
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
    body['sign'] = signstr
    return body
def get_itemurl(short_url):
    """
    将商品短链接通过模拟请求，转换为商品原链接
    """
    tmp = requests.get(short_url)
    link = tmp.text[tmp.text.find('https://'):]
    link = link[:link.find('?')]
    link = requests.get(link).url
    return link

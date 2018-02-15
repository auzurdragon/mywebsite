from django.shortcuts import render

# Create your views here.

def tb_coupon(request):
    """优惠券搜索"""
    # from mycoupon.models import tb_coupon
    # from json import loads
    import re
    from math import ceil
    from mycoupon.coupon import coupon
    from django.core.paginator import Paginator
    q = request.GET.get('q') if request.GET.get('q') else '吉他'
    page_no = int(request.GET.get('page')) if request.GET.get('page') else 1
    s = coupon()
    cnum, clist = s.tb_getcoupon(q=q, page_no=page_no)    
    # 提取折扣价和优惠券信息，计算券后价格
    for i in clist:
        i['zk_final_price'] = round(float(i['zk_final_price']) - float(re.findall('\d{1,3}', i['coupon_info'])[1]), 2)
    page_max = ceil(cnum/20)
    plist = list(range(1, ceil(cnum/20)+1)) # 每页20个，转换查询结果数量为页数
    print(page_no)
    page_no = page_no if page_no in plist else 1 # 检查页码是否在总页数范围内
    print(cnum, q, page_no, plist,  sep="\n")
    return render(request,'tb_coupon.html', {'clist':clist, 'q':q, 'page_no':page_no, 'plist':plist, 'page_max':page_max})

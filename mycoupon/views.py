
from django.shortcuts import render
from django.http import HttpResponse
from mycoupon import taobao_api

# Create your views here.

def tb_coupon(request):
    """
    优惠券搜索
    """
    # 初始化参数
    content = []
    page_size = 30
    key = request.GET.get('key') if request.GET.get('key') else '吉它'
    page_no = int(request.GET.get('page')) if request.GET.get('page') else int(1)
    page_list = []
    page_num = 0
    # 查找优惠券
    result = taobao_api.get_coupon(key=key, page_size=page_size, page_no=page_no)
    if result[0] == True:
        content = result[2]
        # 计算页数
        page_num = int(result[1]/page_size) + 1
        # 计算页码序列
        if page_no < 7:
            A = 1
            B = 11 if page_num > 11 else page_num
        elif page_no > page_num -6:
            A = page_num - 10
            B = page_num
        else:
            A = page_no - 5
            B = page_no + 5
        page_list = list(range(A, B+1))
    return render(request,'coupon.html', {'content':content, 'key':key, 'page_no':page_no, 'page_list':page_list, 'page_num':page_num})

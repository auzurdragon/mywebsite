
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from mycoupon import coupon
from django.http import JsonResponse
# Create your views here.

def coupon_rest(request):
    """
    优惠券搜索接口
    """
    try:
        if request.method == 'POST':
            status, coupon_num, coupon_list = coupon.get_coupon(
                q = request.POST.get('q') if request.POST.get('q') else '吉它',
                cat = request.POST.get('cat') if request.POST.get('cat') else '',
                page_no = request.POST.get('page_no') if request.POST.get('page_no') else 1,
                is_tmall = request.POST.get('is_tmall') if request.POST.get('is_tmall') else 'false',
                need_free_shipment = request.POST.get('need_free_shipment') if request.POST.get('need_free_shipment') else 'false',
                need_prepay = request.POST.get('need_prepay') if request.POST.get('need_prepay') else 'false',
                start_price = int(request.POST.get('start_price')) if request.POST.get('start_price') else 0,
                end_price = int(request.POST.get('end_price')) if request.POST.get('end_price') else 0,
                sort = request.POST.get('sort') if request.POST.get('sort') else '',
                )
            result = {
                'status': status,
                'msg': 'request success',
                'coupon_num': coupon_num,
                'coupon_list': coupon_list,
            }
        else:
            result = {
                'status': False,
                'msg': 'request get',
                'coupon_num': 0,
                'coupon_list': [],
            }
    except:
        result = {
            'status': False,
            'msg': 'request failed',
            'coupon_num': 0,
            'coupon_list': [],
        }
    finally:
        return HttpResponse(json.dumps(result), content_type='application/json')

def tb_coupon(request):
    """
    优惠券搜索
    """
    # 初始化参数
    content = []
    page_size = 30
    q = request.GET.get('q') if request.GET.get('q') else '吉它'
    page_no = int(request.GET.get('page')) if request.GET.get('page') else int(1)
    page_list = []
    page_num = 0
    # 查找优惠券
    result = coupon.get_coupon(q=q, page_size=page_size, page_no=page_no)
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
    return render(request,'coupon.html', {'content':content, 'q':q, 'page_no':page_no, 'page_list':page_list, 'page_num':page_num})

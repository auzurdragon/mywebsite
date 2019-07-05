from django.shortcuts import render

# Create your views here.

def myapps(request):
    """
        我的应用首页
    """
    AppPanel = [
        {'title':'企业数据查询', 'url':'qydata', 'content':'按关键字抓取企查查的免费数据。'},
        {'title':'中文分词', 'url':'#', 'content':'对输入的文本进行分词, 统计词频。'}
    ]
    return render(request, 'panellist.html', {'PanelList':AppPanel})

def qydata(request):
    """
        企业数据查询
    """
    description = "按关键字抓取企查查免费数据，默认条件为 抓取长沙+存续+有限责任公司，返回结果按成立时间逆序排列。"
    api = '/myapps/qydata'
    TableTitle, TableRow, RowNum = [],[], 0
    keywords = request.GET.get('q')
    pagenum = 1
    if keywords:
        from myapps.qydata import GetQyDataQichacha
        qicc = GetQyDataQichacha(keywords.split())
        qicc.get_list_all(pagenum)
        RowNum = len(qicc.QyList)
        if RowNum:
            TableTitle = ['名称','状态','注册资本','成立时间','联系人','电话','邮箱','地址']
            TableRow = [ [i['Name'],i['Status'],i['Capital'],i['estDate'],i['LxName'],i['Tel'],i['Email'],i['Addr']] for i in qicc.QyList]
    print(TableTitle, TableRow, RowNum)
    return render(request, 'search.html',{'Api':api,'TableTitle':TableTitle,'TableRow':TableRow, 'RowNum':RowNum,'description':description})

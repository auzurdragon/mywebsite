# -*-coding=utf-8 -*-
"""高德地图查询接口"""

class SearchAPI(object):
    """查询接口"""
    def __init__(self):
        self.ak = "4abe9ac8ff90a85bc562d4127c7de355"
        self.city = int(4301)
        self.result = []

    def s_library(self, qword="图书馆"):
        """使用百度接口，查询东郡小学周边50km范围的图书馆"""
        from urllib import request
        from json import loads
        requ_para = {
            "location":"28.192726,113.032666",
            "radius":"50000",
            "query":qword,
            "tag":"高等院校,中学,小学,亲子教育,留学中介机构,图书馆,科技馆,美术馆,展览馆,文化宫",
            "output":"json",
            "scope":2,
            "page_size":20,
            "page_num":0,
            "ak":"4abe9ac8ff90a85bc562d4127c7de355"
        }
        requrl = "http://api.map.baidu.com/place/v2/search"
        requrl = ("%s?%s" % (
            requrl, "&".join(
                ["%s=%s" % (i, str(requ_para[i])) for i in requ_para]
                )
            ))
        res = request.urlopen(request.quote(requrl, safe="!*'();:@&=+$,/?%#[]")).read().decode()
        self.result = loads(res)["results"]
        return True

if __name__ == "__main__":
    result = SearchAPI()
    result.s_library()
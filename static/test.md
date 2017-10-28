# 标题1 
## 标题2 

    # 代码块<code></code>
    import markdown
    reader = open("static/test.md", "rb")
    html = reader.read().decode("utf-8")
    reader.close()
    html = markdown.markdown(html)
    print(html)

> 引用  
> 引用  

### 标题3  
1. 列表1 
2. 列表2 
3. 列表3

### 标题3
* 无序列表  
* 无序列表  
    * 二级列表  
    * 二级列表  

### 分隔线  
    ***  
    ---  
***  
---  

### 参考链接  
    [百度](http://www.baidu.com)  
[百度](http://www.baidu.com)
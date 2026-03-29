from django.shortcuts import render # 把一个 HTML 模板和数据结合起来，生成网页，再返回给浏览器。


def index(request):
    return render(request, 'index.html')

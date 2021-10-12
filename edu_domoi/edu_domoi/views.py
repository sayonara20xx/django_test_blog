# здесь описываем возвращаемые ответы (вьюхи)

from django.http import HttpResponse

def hello(request):
    return HttpResponse("<h1>hello</h1>")
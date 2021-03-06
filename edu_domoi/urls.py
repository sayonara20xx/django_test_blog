"""edu_domoi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include 

# path представляет собой следующий метод:
# если мы получаем значение, переданное первым аргументом, то вызываем вторую
# функцию с аргументом

# вообще у path 4 агрумента
# Два из них позиционных, уже указаны, но если логика большая, то будет удачнее
# использовать вторым параметром функцию include, который вместо функции использует
# модуль для обработки запроса

from .views import redirect_blog

urlpatterns = [
    path('', redirect_blog),
    path('admin/', admin.site.urls),
    path('blog/', include("edu1.urls"))
]

"""
    в юрлсах описываются функции-обработчики запросов, который будут
    возвращать ответы

    как вообще джанго машрутизирует:
    например, пришёл запрос
    http://localhost:5000/blog/some-file.txt

    первым делом, джанго отбрасывает домен и остается
    blog/some-file.txt
    
    и затем, в файле urls.py в коллекции urlpatterns
    смотрит, есть ли соответствия у полученных кусков урла
    с этим списком (сначала, этим куском будет blog)

    если обрабатывает запрос приложение, то следующий
    кусок так же, в юрлсах и в юрлпаттернс будет обрабатываться
    уже внутри модуля (здесь следующий кусок - some-file.txt)
    но пути на темплейты внутри каталогов приложений должны оставаться полными
    т.е. в нашем случае, в пути должна быть папка blog

    ------
    Так же имеет очень большой смысл присваивать имена узлам
    Если мы создаем навигацию внутри сайта, то при написании
    внутри вьюшек строгих ссылок при изменении карты сайта
    нам придётся их переписывать

    Джанго может вручную вместо имён подставлять ссылки, если
    ещё в path мы именованным параметром зададим узлу имя,
    которое используем вместо пути, например, в html-атрибуте <a>
    Чтобы джанга нас поняла, достаточно вместо ссылки написать
    такую конструкцию:
    {% url 'posts_list_url' %}
    где в кавычках имя узла

    параметры через пробелы - это сепарированные /-ой узлы
    если мы вводим что-то без кавычек, джанго это воспримет
    как переменную контекста

    эту конструкцию можно облегчить, определив у модели
    метод get_absolute_url

    --------
    Да, есть ещё такая штука: иногда файлы создаются с фигурными
    скобками в urlpatterns вместо квадратных, спасёт тебе время
"""
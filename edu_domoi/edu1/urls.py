from django.urls import path
from django.urls.resolvers import URLPattern

from .views import *

urlpatterns = [
    path("", post_list, name="posts_list_url"),
    path("post/<str:slug>/delete/", PostDelete.as_view(), name="post_delete_url"),
    path("post/create/", PostCreate.as_view(), name="post_create_url"),
    path("post/<str:slug>/", PostDetail.as_view(), name="post_detail_url"),
    path("post/<str:slug>/update", PostUpdate.as_view(), name="post_update_url"),
    path("tags/", tags_list, name="tags_list_url"),
    path("tag/<str:slug>/delete/", TagDelete.as_view(), name="tag_delete_url"),
    path("tag/create/", TagCreate.as_view(), name="tag_create_url"),
    path("tag/<str:slug>/", TagDetail.as_view(), name="tag_detail_url"),
    path("tag/<str:slug>/update/", TagUpdate.as_view(), name="tag_update_url")
]

"""
    Чтобы нам использовать заранее неопределённые
    названия путей, мы будем использовать шаблоны пути

    Угловые скобки, которые идут внутри этой штуки
    /<>/
    означают, что внутри именованная группа символов
    /<тип:имя_группы>/

    Это означает, что во вьюху-обработчик мы передаем
    параметр, описанный именованной группой символов
    имя_группы = имя параметра в функции-вьюхе после реквеста


    -- конфликты урлов --
    урлы надо писать таким образом, чтобы они не конфликтовали,
    а то пользователь попадет не туда, куда надо
    особенно внимательно надо быть с шаблонами, в котором имя
    параметра может быть любым, если предыдущие узлы совпадают

    здесь, например, мы хотим реализовать создание тега
    форма для создания лежит по адрессу:
    tag/create

    у нас уже есть
    tag/<str:string>
    
    которая сработает вместо создания, если мы напишем tag/create ниже
    в связи с этим два момента:
    - обработка пути создания выше
    - нельзя создавать теги с именем create, иначе при поиске по нему
    будем попадать на страницу с созданием
"""
from django.core import paginator
from django.db.models.query import RawQuerySet
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse
from django.urls import reverse

from .models import Post, Tag
from .utils import *
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

def post_list(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        "posts": page, 
        "index": True,
        "is_paginated": is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, "blog/index.html", context=context)


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = "blog/tag_detail.html"


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = "blog/tag_create_form.html"
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    form_model = TagForm
    template = "blog/tag_update_form.html"
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = "blog/tag_delete_form.html"
    redirect_url = "tags_list_url"
    raise_exception = True


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = "blog/post_detail.html"


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = "blog/post_create_form.html"
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    form_model = PostForm
    template = "blog/post_update_form.html"
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = "blog/post_delete_form.html"
    redirect_url = "posts_list_url"
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, "blog/tags_list.html", context={"tags": tags})


"""
    Все htlm распологаем внутри папки templates
    templates - словно корень, папки внутри - узлы,
    которым вьюшки соответствуют
    То есть, если мы здесь обрабатываем страницу для
    адреса /blog, то распологаться она будет в папке:
    edu1/templates/blog

    Такая структура результат соглашения джанго
    При запуске джанго собирает из папок все темплейты
    и смотрит, нет ли по одному адресу одинаковых
    темплейтов, то есть, конфликта имен

    Чтобы привязать шаблон из папки к запросу,
    мы используем метод render(<request>,
    <relative_view_path_without_"templates"_dir>)
    Да, так как джанго собирает все шаблоны,
    нам не нужно указывать в начале пути папку templates

    Если нам нужно показать в шаблоне результат каких-либо
    вычислений, то мы можем с помощью именованного параметра
    context во внутрь html темплейта передать их значения,
    там они разыменовываются с помощью двойных фигурных скобок

    Процесс наполнения шаблона данными - рендеринг
    на что название функции и расчитывает

    -- рендер (наполнение и изменение html-фарша) параметрами и средствами джанги --
    Есть такая ситуация: нам нужно передать список имён в рендер,
    и мы хотим, чтобы каждое имя было в отдельном теге <p>

    в таком случае мы можем воспользоваться средствами джанго
    для изменения содержания темплейтов типа программируя,
    написав питон-лайк код внутри html-докумета, я там
    уже предоставил пример как это сделать

    по факту, мы просто генерируем повторяющиеся куски html-разметки,
    используя средства джанго

    -- "Наследование" вьюшек --
    Если у нас несколько вьюшек, то есть смысл повторяющиеся
    общие элементы, типа футера и хеадера, вынести в отдельный
    шаблон. У джанги есть механизм наследования шаблонов, который
    наполняет дочерние шаблоны своим содержимым, что удобно

    Чтобы реализовать такое, сначала, создадим темплейт с наиболее
    общим содержимым (здесь это base.html), и там, помимо того, что
    нами было описано как общее, мы распологаем отдельные блоки
    {% block имя_блока %}{% endblock %}

    Ими мы размечаем "не общие" места во вьюшке, которые мы будем
    заполнять с помощью других файлов, как это сделано в index.html

    В последнем мы указываем ещё одну директиву(или как это называется)
    {% extend <path_to_file_without_templates_dir> %}
    и соответствие html-фарша самим блокам устанавливаем с помощью
    {% block имя_блока %}{% endblock %}
    заменит тот блок, который был описан в файле, указанном в пути
    в экстенде

    Да, джанго просто подставит index.html в тот html-каркас, который 
    мы опишем в других файлах.
    Польза такого неочевидного подхода очевидна - описание общее,
    меняется и контролируется посредством одного файла

    Чтобы шаблоны можно было юзать откуда угодно, в корне проекта,
    на одном уровне с директориями приложений, создаем папку
    templates, и там храним их

    Чтобы джанго увидела файлы там, необходимо в файле settings.py
    в словаре TEMPLATES, добавляем в DIRS в список путь до папки
    os.path.join(BASE_DIR, "templates")
    сама функция вернёт рабочий для текущей оси путь до папки
    BASE_DIR - переменная среды окружения, которая хранит абсолютный
    путь до проекта, т.е. путь до папки во втором параметре так же
    абсолютный


    -- Фильтры шаблонов --
    Они используются и применяются относительно легко, легче
    делать по документации
    Например, обрезание количества выводимых слов будет происходить
    следующим образом в процессе рендера:
    применение фильтра - пайп, далее - название, после двоеточия - аргументы

    {{ <переменная>|truncatewords:15 }}


    -- Включение шаблонов --
    Как наследование, только наоборот
    По сути, просто включаем весь отдельно написанный html-исходник в другой,
    определив ему место

    в директории blog я создал includes, где включаемые файлы
    будут располагаться, и в ней уже создал html файл

    его включение происходит следующим образом:
    {% include 'blog/includes/postcard_template.html' %}
    путь нужно указывать полный, иначе он не поймёт

    Исходник можно написать прямо с именами используемых в исходном
    файле переменных, содержимое через инклюд просто копипаститься
    во внутрь во время рендера


    -- Class Based Views --
    Вьюха, как обработчик запроса, может быть представлена в
    виде отдельного класса, что в джанго уже было сделано за нас
    Проблему необходимости описания класса начинаешь замечать, когда
    пишешь почти идентичныке запросы, например, как здесь:
    def post_detail(request, slug):
        post = Post.objects.get(slug__iexact=slug)
        eturn render(request, "blog/post_detail.html", context={"post": post})

    def tag_detail(request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        return render(request, "blog/tag_detail.html", context={"tag": tag})

    казалось бы, отличий немного, какую-то логику можно вынести в отдельный
    класс во имя DRY

    Этот класс за нас обработает всё, что связано с запросом, например,
    необязательно проверять какой именно запрос прилетел, GET ли он
    вообще

    Пример описания уже представлен выше, в urls.py теперь надо
    указать метод класса as_view как обработчик

    Проблему похожести логики решим с помощью её описания в отдельном
    классе. Такие приколы называются МИКСИНАМИ, по сути, просто
    промежуточные классы, от которых мы потом наследуемся.

    Я вынес их отдельно в utils.py, там же представлен пример описания
    Да, после описания миксина его нужно так же наследовать и
    самым очевидным образом использовать, переопределив логику
    через определения атрибутов

    Единственный интересный и неочевидный момент завязан на
    формировании списка, передаваемый рендердеру во время
    построения ответа-страницы: 
    там мы используем получение имени класса с приведением его 
    к нижнему регистру как ключ поля, так что это в рендеринге 
    и листинге html надо учитывать

    Ещё, что тоже стоит учитывать, так это MRO при наследовании
    миксинов: будет определено свойство так, как это указано
    у самого левого класса, если есть свойства с одинаковыми
    именами


    -- Получение дефолтной 404 -- 
    Чтобы описать такую логику, импортируем метод get_list_or_404
    Если мы без него описывали получение записей из бд в виде
    экземпляров моделей вот так:
    post = Post.objects.get(slug__iexact=slug)

    то теперь логика такая:
    post = get_list_or_404(Post, slug__iexact=slug)

    за нас вызывает objects, за нас get
    Работает внутри как дефолтный try-except: вытащила - 
    дальше как обычно работает с данными и возвращает их,
    нет - ответом будет джанговская 404


    -- Основы работы с формами --
    Это лежит в основе CRUD - "паттерн" функциональности
    Create - Read - Update - Delete

    Чтение уже было реализовано, осталось остальное

    Мы как пользователи хотели бы создавать посты
    через формы - максимально привычный способ,
    через них же имеет смысл реализовать и
    изменение постов

    Делая это через html формы мы обрекаем себя кучей
    работы: нужно проверять какие данные вводятся,
    в рамках защиты и простой смысловой фильтрации,
    хотя-бы чтобы нельзя было заполнить со <script>

    Идея в том, чтобы собрать данные, сформировать их
    в какую-то сущность, а потом создать экзепляр соответствующей
    модели, плюс ещё поменять зависимые бд, типа тегов

    Действий много, и джанго уже имеет некоторые классы,
    которые облегачают работу

    Работа с формами будет происходить в отдельном файле
    forms.py, туда и перекатываемся


    -- POST запросы в форме --
    Здесь представлен пример, как мы получаем данные из формы
    через пост запрос и используем их для создания записи в бд
    тегов
    
    Впринципе, всё логично, за исключением редиректа в ретурне,
    этот метод вполне универсален, здесь он нас по объекту
    просто перенаправит на страницу с созданным тегом

    Ещё момент: все данные мы получаем из передаваемого автоматически
    аргумента requests

    -- Изменение объектов --
    Цепочка работы такая:
    идентификация и получение объекта
    представить текущие данные в виде формы
    проверить валидность изменённых польхователем данных

    Чтобы подставить в форму все данные, достаточно передать
    в именованный параметр конструктора формы сам экземпляр
    модели (если форма наследуется от класса ModelForm, как
    здесь, именно такая логика там реализована)

    -- Чё за пагинатор такой? --
    Я уже описывал пагинацию в manage.py, что происходит и как работает.
"""
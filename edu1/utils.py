from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin

from .models import *

class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj, "admin_object": obj, "detail": True})

class ObjectCreateMixin(View):
    # здесь реагируем на post-запросы
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={"form": form})

    def post(self, request):
        bound_form = self.form_model(request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={"form": bound_form})


class ObjectDeleteMixin(View):
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj, "admin_object": obj, "delete": True})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))


class ObjectUpdateMixin(View):
    model = None
    form_model = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(instance=obj)
        return render(request, self.template, 
                      context={"form": bound_form, self.model.__name__.lower(): obj, "admin_object": obj, "Update": True})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, 
                      context={"form": bound_form, self.model.__name__.lower(): obj})

'''
    Вроде как всё понятно и уже описано: эти миксины просто объединяют в один
    объект общую реализацию вьюшек-объектов.

    Что стоит ещё упомянуть: работу с кнопками, которые реализуют функционал CRUD.
    Чтобы отображать их как следует, передаем в контекст шаблона объект с ключом
    'admin_object' со значением obj, т.е. передаем объект рендеру.
    У этого обьекта вызываем методы получаения урлов для модификации
    и удаления, т.е. прямо внутри href пишем вызов функции в двойных фигурных скобках

    А, есть ещё переменные, передаваемые в конекст, которые отвечают за прорисовку кнопок,
    они обеспечивают то, что лишние кнопки показываться не будут, например, во время
    просмотра подробностей кнопки "создать" быть не должно.

    Но я сделаю не как автор видоса, я просто запихну в рендер условие {% if имя_свойства %}
    в блоке которого размещу то, что нужно. Например, при detail == true отображаются только
    кнопки модификации или удаления поста.

    Причем пофиг, определены ли эти контекстные переменные во время проверки или нет, если нет,
    то просто вернётся false.
'''
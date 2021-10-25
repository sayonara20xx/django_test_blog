'''
    Здесь буду писать всё о структуре джанги в целом

    Проект состоит из приложений (App), которые представляют
    из себя отдельный кусок функционала, изолированное приложение

    Приложение = папка с исходниками внутри
    По хорошему, приложения должны работать независимо друг от друга
    что логично, ведь мы захотим их переносить из одного проекта в другой

    создать свое приложение можно так:
    python manage.py startapp <название_приложения>
    (выполнять в активной директории с manage.py)

    В джанго реализован паттерн MVC
    Model - View - Controller
    Код для описания данных в бд - модели
    Маршрутизация генерации ответа пользователю - вьюшка
    Код, маршрутизирующий и обрабатывающий запросы - контроллер

    А за обработку запроса отвечает только файл Views, то есть
    весь контроль отображения шаблонов реализован со вьюшками

    Мы будет использовать sqlite
    Данные в базах данных хранятся в таблицах, где в столбцах
    содержаться поля сущностей, а в каждой строке - обособленная
    сущность, ничего нового.

    Общение с базой данных, обычно, происходит с помощью sql
    запросов напрямую, но джанго поднимает и это на один
    уровень вверх и для обмена информацией с данных мы будем
    пользоваться ORM (Object Relational Mapping)

    Перевод на русский (объекто-реляционное отображение)
    Суть слова меппинг - процесс соотнесения "карты и территории"

    вместо карты - объекты python, а вместо территории - базы данных
    бд соответственно реляционная

    Джанго позволяет представить записи и их свойства в виде
    объектов Python, и работу с самой базой средствами абстракции
    ООП - классами и их методами.

    Да, можно было бы вручную закодить вызов запросов и параметров,
    но вот если база данных поменяется, сложные запросы приходится
    переписать

    Суть ORM в том, чтобы не было проблем при смене БД

    Модели описываются в model.py
    Вьюшки в views.py
    Обработку перехода на узел и вызов соответствующей вьюшки осуществялет urls.py
    Всякие вспомогательные приколы типа миксинов есть в utils.py
    Формы, которые используются за получения данных и которые можно соотнести с 
    моделями - в forms.py

    А этот файл (manage.py) представляет собой некий интерфейс, позволяющий контролировать
    и настраивать работу кода.
'''

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edu_domoi.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
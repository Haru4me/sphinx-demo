# Инструкция по созданию документации с использованием `sphinx`

## Первый подход

```bash
$ mkdir doc
$ cd doc
$ sphinx-apidoc -M -e -o . -a ../numeric -V 0.0.0 -A Golov~V.A. -E
$ rm make.bat
$ make html
```

## Улучшим простой вариант

1. Добавим настройки в `setup.py`
2. Добавим иконку и лого в `_static`
2. Отредактируем `index.rst`
3. Добавим статические страницы `install.rst` и `start.rst`

## Что дальше?

1. Замена `sphinx.ext.napoleon` на `numpydoc`
    - Более красивое чтение docstring'ов
    - Нужны отдельные `файлы.rst` под методы классов
2. Шаблоны `_templates`
    - Сами задаем стиль оформления `autodoc` и `autosummary`
    - Можно не хранить нестатические `rst` в репозитории, а сразу генериить все по заданным шаблонам.
    - Нужно разбираться
3. Покрытие документации и тесты на документацию (последнее хз)
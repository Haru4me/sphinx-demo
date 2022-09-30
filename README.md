# Инструкция по созданию документации с использованием `sphinx`

## Полезные ссылки

- [Getting Started](https://www.sphinx-doc.org/en/master/usage/quickstart.html)
- [Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc)
- [Sphinx autosummary](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#module-sphinx.ext.autosummary)
- [Sphinx extensions](https://www.sphinx-doc.org/en/master/usage/extensions/index.html#extensions)

## Можно начать так

```bash
sphinx-quickstart
```

## Создание с готовым autodoc

```bash
$ mkdir doc
$ cd doc
$ sphinx-apidoc -M -e -o . -a ../numeric -V 0.0.0 -A Golov~V.A. -E
$ rm make.bat
$ make html
```

## Улучшим

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

# Инструкция по созданию документации с использованием `sphinx`

## Полезные ссылки

- [Numpydoc style guide](https://numpydoc.readthedocs.io/en/stable/format.html)
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

1. doc2.0
    - Редактированный `setup.py `
    - Добавлены статические файлы
    - Добавлены статические `*.rst`
2. doc3.0
    - Первый подход к автогенерации с autosummary
3. doc4.0
    - Альтернативный подход к автогенерации с autosummary


## Подумать

1. Как улучшить
2. Как исправить проблемы с toctree
3. Подумать как лучше интегрировать `numpydoc extention`
4. Поддержка версий

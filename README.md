# Инструкция по созданию документации с использованием `sphinx`

## Полезные ссылки

- Sphinx start
    - [Numpydoc style guide](https://numpydoc.readthedocs.io/en/stable/format.html)
    - [Sphinx Getting Started](https://www.sphinx-doc.org/en/master/usage/quickstart.html)
    - [Sphinx Config Setup](https://www.sphinx-doc.org/en/master/usage/configuration.html)
    - [Sphinx apidoc](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html)
- Sphinx advanced
    - [Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc)
    - [Sphinx autosummary](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#module-sphinx.ext.autosummary)
    - [Sphinx extensions](https://www.sphinx-doc.org/en/master/usage/extensions/index.html#extensions)
    - [Numpydoc extention](https://numpydoc.readthedocs.io/en/latest/install.html)
    - [Markdown extention](https://www.sphinx-doc.org/en/master/usage/markdown.html)
- Alternatives
    - [Mkdocs](https://www.mkdocs.org/)
    - [Mkdocs Material](https://squidfunk.github.io/mkdocs-material/)

## Создание документации через quickstart

```bash
$ sphinx-quickstart
$ make html
```

## Создание с готовым autodoc через sphinx-apidoc

```bash
$ sphinx-apidoc -f -F -M -e -o . -a ../numeric -V 0.0.0 -A Golov~V.A.
$ rm make.bat
$ make html
```

## Улучшим

1. doc1
    - sphinx-quickstart
    - sphinx-apidoc
2. doc2
    - Редактированный `setup.py `
    - Добавлены статические файлы
    - Добавлены статические `*.rst`
3. doc3
    - Первый подход к автогенерации с autosummary
4. doc4
    - Альтернативный подход к автогенерации с autosummary


## Подумать

1. Как улучшить
2. Как исправить проблемы с toctree
3. Подумать как лучше интегрировать `numpydoc extention`
4. Поддержка версий

## Наблюдение

При генерации с `sphinx-apidoc` можно заметить, что наличие сгенерированного названия влияет на мерархическую структуру `toctree`. Так, при сгенерированном названии глубина равна 3, а при несгенерированном равна 2.
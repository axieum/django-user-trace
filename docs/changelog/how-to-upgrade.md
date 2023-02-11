# How to upgrade

## with pip <small>recommended</small> { #with-pip data-toc-label="with pip" }

`django-user-log` can be upgraded from [PyPI][pypi].

=== ":simple-pypi: pip"

    ```sh
    pip install -U django-user-log
    ```

=== ":simple-poetry: poetry"

    ```sh
    poetry update django-user-log
    ```

??? question "How do I see what version I currently have installed?"

    To see which version of `django-user-log` you currently have installed, use:

    === ":simple-pypi: pip"

        ```sh
        pip show django-user-log
        ```

    === ":simple-poetry: poetry"

        ```sh
        poetry show django-user-log
        ```

!!! tip

    It's always recommended to invoke `pip install` in a Python virtualenv. This
    will ensure that there are no conflicts with your global Python installation.

[pypi]: https://pypi.org/project/django-user-log

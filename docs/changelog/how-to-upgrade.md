# How to upgrade

## with pip <small>recommended</small> { #with-pip data-toc-label="with pip" }

`django-user-trace` can be upgraded from [PyPI][pypi].

=== ":simple-pypi: pip"

    ```sh
    pip install -U django-user-trace
    ```

=== ":simple-poetry: poetry"

    ```sh
    poetry update django-user-trace
    ```

??? question "How do I see what version I currently have installed?"

    To see which version of `django-user-trace` you currently have installed, use:

    === ":simple-pypi: pip"

        ```sh
        pip show django-user-trace
        ```

    === ":simple-poetry: poetry"

        ```sh
        poetry show django-user-trace
        ```

!!! tip

    It's always recommended to invoke `pip install` in a Python virtualenv. This
    will ensure that there are no conflicts with your global Python installation.

[pypi]: https://pypi.org/project/django-user-trace

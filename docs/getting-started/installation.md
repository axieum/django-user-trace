# Installation

## with pip <small>recommended</small> { #with-pip data-toc-label="with pip" }

`django-user-trace` can be installed from [PyPI][pypi].

=== ":simple-pypi: pip"

    ```sh
    pip install django-user-trace
    ```

=== ":simple-poetry: poetry"

    ```sh
    poetry add django-user-trace
    ```

## with git

You can also build and install `django-user-trace` from its source.

```shell
git clone https://github.com/axieum/django-user-trace.git
cd django-user-trace
pip install -e .
```

!!! tip

    It's always recommended to invoke `pip install` in a Python virtualenv. This
    will ensure that there are no conflicts with your global Python installation.

[pypi]: https://pypi.org/project/django-user-trace

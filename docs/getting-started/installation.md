# Installation

## with pip <small>recommended</small> { #with-pip data-toc-label="with pip" }

`django-user-log` can be installed from [PyPI][pypi].

=== ":simple-pypi: pip"

    ```sh
    pip install django-user-log
    ```

=== ":simple-poetry: poetry"

    ```sh
    poetry add django-user-log
    ```

## with git

You can also build and install `django-user-log` from its source.

```shell
git clone https://github.com/axieum/django-user-log.git
cd django-user-log
pip install -e .
```

!!! tip

    It's always recommended to invoke `pip install` in a Python virtualenv. This
    will ensure that there are no conflicts with your global Python installation.

[pypi]: https://pypi.org/project/django-user-log

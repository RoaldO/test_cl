Test Creation Lib 
=================

analyzes your source files and generates test files for them. It will of course not implement the actual test cases, but
the generation process really speeds up development of your application.

Installation
------------
install the library using:

### pip
```shell
$ python -m pip install test_cl
```

### poetry
```shell
$ poetry add --dev test_cl
```

Running
-------
The test_cl commands need to be run from the applications root folder.

```shell
python -m test_cl generate
```

Contributing
------------
In this phase I do not yet accept contributions, but hopefully soon will. If you really need to have certain changes, 
you can of course branch the project.

### Setup
The development of the library uses [poetry](https://python-poetry.org/) to manage the dependencies and virtual 
environment.

### Automated tests
The library uses [pytest](https://docs.pytest.org/) to test its own implementation.

### IDE setup
#### JetBrains IDEs
Mark the _src_ folder as _Sources Root_ and the _tests_ folder as _Test Sources Root_

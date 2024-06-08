# Git-gut
## Description
Application will analyze is there a technical debt in project. By showing various statistics which might indicate presence of "technical debt". </br>

## Prerequisites
Make sure tool Poetry is installed, for instructions use official website https://python-poetry.org/docs/

## Installation
```bash
poetry install
```

## Help (Man page)
Application requires only one argument, path to your repo <br/>
To get full list of possible options, just run:
```bash
poetry run python main.py --help
```

## Few examples to get started
```bash
poetry run python main.py --columns=filename,commitcount,mfauthor,daratio,linecount --sort=daratio-desc --filters="linecount>50" ./
poetry run python main.py --query="SHOW linecount, daratio FROM ./ WHERE linecount > 10 and daratio > 0.1 ORDERBY daratio DESCK and linecount DESC" ./
```

## Word of caution
Right now it's not optimized to be used on big and long running repositories.

## Local development
Project has various tools setup for code styling 
1. Pylint - https://pylint.readthedocs.io/
2. Black - https://black.readthedocs.io/

To check code style you can run
```bash
poetry run pylint $(git ls-files '*.py')
```
To autoformat file you can setup your favourite IDE or run CLI command
```bash
poetry run black ./
```
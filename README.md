# DjangoRecipes

## Description

Web site which contains experiences on synthesis images (perception of noise). 

## Installation

### 1. Manually

#### Requirements

You need to have python, pip

```
pip install -r requirementst.txt
```

#### Run server

And then, run the server :

```
python project/manage.py runserver
```

or if you want to precise a specific port number :

```
python project/manage.py runserver 8080
```

### 2. Using docker (recommended)

You can use make commands:

```
make build
```

```
make run
```

Or simply:

```
make deploy
```

Will run `build` and `run` commands at once.

You also have `stop`, `remove`, `clean` commands:
- `stop`: stop current container instance if exists
- `remove`: stop and remove container instance if exists
- `clean`: remove docker image if exists

## How to contribute ?

This project uses [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/) to improve cooperation during the development.

For each feature, you have to create a new git flow feature branch.

## Licence

[MIT](LICENSE)

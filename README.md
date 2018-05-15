
## Requisitos

- Python 2.7.5 (Normalmente pre-instalados em ambientes linux. https://www.python.org/download/releases/2.7.5/)

- pip (normalmente vem instalado com as versões 2.7 do python. https://pip.pypa.io/en/stable/installing/)

- virtualenv (tutorial para instalação em windows: https://fernandofreitasalves.com/tutorial-virtualenv-para-iniciantes-windows/)



## Criando o ambiente

```shell
    virtualenv ENV
```

## Configurando o shell para ambiente virtual

```shell
    source ENV/bin/activate
```

## Baixando as dependencias

```shell
    pip install -r requirements.txt
```

## Executando o app

```shell
    ./ENV/bin/python src/app.py
```

## Requisitos


# Windows:

- GIT (https://git-scm.com/download/win)

- Python 2.7.9, download para Windows: (https://www.python.org/ftp/python/2.7.9/python-2.7.9.msi)

- Configurar variavel de ambiente PYTHON_HOME para o endereço de instalação, normalmente para windows é usado o caminho c:\Python27

![Alt text](python_home.PNG)

-- PYTHON_HOME=c:\Python27
-- adicionar a variavel PYTHON_HOME na variavel PATH conforme a figura abaixo (texto a ser add na variavel PATH %PYTHON_HOME%\;%PYTHON_HOME%\Scripts\ ):

![Alt text](python_in_path.PNG)




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

## Configuração do ambiente

# Windows

- GIT (https://git-scm.com/download/win)

- Python 2.7.9, download: (https://www.python.org/ftp/python/2.7.9/python-2.7.9.msi)

- Configurar variavel de ambiente PYTHON_HOME para o endereço de instalação, normalmente para windows é usado o caminho c:\Python27 para a instalação (Link sobre configurações de variaveis de ambiente no Windows https://technet.microsoft.com/pt-br/library/cc668471.aspx)

![Alt text](python_home.PNG)

- Adicionar na variavel Path o seguinte texto: ;%PYTHON_HOME%\;%PYTHON_HOME%\Scripts\ :

![Alt text](python_in_path.PNG)

- Para testar a configuração basta abrir um novo terminal e digitar os seguintes comandos abaixos:

Testar comando python:
```shell
    python --version
```
Saida para o comando python deve ser algo parecido com:
```shell
	Python 2.7.9
```
Testar o comando pip:
```shell
    pip --version
```
Saida para o comando pip deve ser algo parecido com:
```shell
	pip 1.5.6 from C:\Python27\lib\site-packages (python 2.7)
```

- Casos os comandos tenham as saidas parecidas, podemos continuar com a instalação do virtualenv

```shell
	pip install virtualenv
```

Testar com o comando abaixo:
```shell
	virtualenv --version
```


# Executando o projeto

- Clonando o projeto

Abra um terminal e digite os seguintes comandos:
```shell
    git clone https://github.com/alessandron3/twitter-data-mining.git
    cd twitter-data-mining/
```

- Criando um ambiente virtual

No mesmo terminal dentro do projeto digite o seguinte comando: 
```shell
	virtualenv ENV/
```

Para ativando o ambiente virtual para esse terminal digite o seguinte comando:
```shell
	ENV\Scripts\activate
```

Depois de ativar o ambiente virtual o curso do terminal deve mudar para algo parecido com o exemplo abaixo:
```shell
	(ENV) C:\Users\alessandro.santos\dev\workspace\twitter-data-mining>
```

Baixando as dependencias
```shell
    pip install -r requirements.txt
```

- Executando a aplicação

Digite o comando abaixo para executar a aplicação:
```shell
	ENV\Scripts\python.exe src\app.py
```

Para acessar abra seu browser e digite o endereço abaixo:
http://localhost:5000/login

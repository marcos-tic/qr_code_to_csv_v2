# Instalar dependências e compilar no Windows 11

Este guia explica como preparar o Python e gerar o executável `CSVExpress.exe`.

## 1. Instalar e conferir o Python

Instale uma versão atual do Python 3 para Windows pelo [site oficial do Python](https://www.python.org/downloads/windows/). Durante a instalação, marque **Add python.exe to PATH**.

Abra um novo Prompt de Comando e confira:

```bat
py --version
```

Se o comando `py` não existir, tente:

```bat
python --version
```

## 2. Abrir a pasta do projeto

Copie a pasta `versao_windows` para o computador Windows. No Explorador de Arquivos, abra essa pasta, clique na barra de endereço, digite `cmd` e pressione Enter. O Prompt de Comando será aberto no local correto.

Confirme que estão presentes `main_windows.py`, `requirements.txt`, `icone.png`, `csv_express_ilustracao.png`, `app_icon.ico` e `compilar_windows.bat`:

```bat
dir
```

## 3. Instalar as dependências

O script de compilação instala as dependências automaticamente. Para instalá-las manualmente, execute:

```bat
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

O arquivo `requirements.txt` inclui PyInstaller, que empacota o programa, além das bibliotecas usadas pelo aplicativo.

## 4. Gerar o executável

Execute o script:

```bat
compilar_windows.bat
```

Ele instala as dependências, compila `main_windows.py` e copia o executável para a pasta atual. Ao final, o arquivo estará em:

```text
versao_windows\CSVExpress.exe
```

O PyInstaller também mantém uma cópia em `versao_windows\dist\CSVExpress.exe`.

## Compilar manualmente

Se preferir não usar o `.bat`, na pasta `versao_windows` execute:

```bat
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m PyInstaller --noconfirm --onefile --windowed --icon=app_icon.ico --add-data "icone.png;." --add-data "csv_express_ilustracao.png;." --name CSVExpress main_windows.py
```

Nesse caso, o executável fica em `dist\CSVExpress.exe`. Para copiá-lo também para a pasta atual:

```bat
copy /Y dist\CSVExpress.exe .\CSVExpress.exe
```

## Problemas comuns

- **`py` ou `python` não é reconhecido:** instale o Python com a opção de adicionar ao PATH e abra um novo Prompt de Comando.
- **Falha ao baixar pacotes:** verifique a conexão com a internet e tente novamente.
- **O Windows bloqueou o arquivo:** use `CSVExpress.exe` gerado localmente e confirme que o Windows Defender não colocou o arquivo em quarentena.
- **O executável não inicia:** recompile pelo Prompt de Comando para ler as mensagens de erro e confirme que a compilação terminou com sucesso.

O executável gerado é para Windows. Para gerar a versão Linux, compile em um ambiente Linux.

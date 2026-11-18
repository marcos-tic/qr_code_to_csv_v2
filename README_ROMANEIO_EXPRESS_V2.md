# Romaneio Express V2

Aplicativo separado do CSV Express para extrair dados de romaneios PDF. O app antigo continua disponível em `main.py` e `main_windows.py`.

Ícone do app: `romaneio_express-v2.png` (PNG) e `romaneio_express-v2.ico` (Windows).

## Executar

No Linux, execute `./executar_romaneio_express-v2.sh` ou rode `python3 romaneio_express_v2.py`. O nome histórico `romaneio_express-v2.py` continua disponível como launcher. É necessário ter as dependências do projeto instaladas (`requirements.txt`). Para processar diretamente pela linha de comando, informe um ou mais PDFs:

```bash
python3 romaneio_express_v2.py arquivo.pdf
```

## Dados extraídos

A interface lista os códigos de pacote associados aos lotes e mantém a coluna de arquivo de origem para referência. A exportação CSV começa com `Minuta` (o número após o hífen no código do pacote) e inclui arquivo de origem, romaneio, data e hora de emissão, origem, destino, motorista, placa, recebedor, observações, totais declarados, lote e código de pacote. O CSV tem uma linha por pacote; datas ausentes ou inválidas ficam vazias.

PDFs sem texto extraível, como documentos digitalizados, e PDFs sem códigos de pacote reconhecidos aparecem no resumo de falhas. O CLI continua processando os outros arquivos e retorna código de erro quando algum falha. A lógica compartilhada fica em `romaneio_core.py`, que deve acompanhar o aplicativo ao executar ou compilar.

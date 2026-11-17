# CSV Express

Aplicativo portátil e moderno para leitura de romaneios em PDF e extração automática de minutas e datas para planilhas CSV.

## 🚀 Características
- **Interface gráfica em PyQt6** com tema claro padrão, opção de tema escuro e suporte a arrastar e soltar (drag & drop).
- **100% Portátil**: Arquivo único executável autônomo sem necessidade de instalar Python ou dependências.
- **Cabeçalho formatado**: Gera o arquivo CSV com a coluna padronizada `Minuta`.
- **Codificação UTF-8 com BOM (`utf-8-sig`)**: Abre perfeitamente no Excel sem erros de caracteres.
- **Suporte a Linha de Comando (CLI)** e processamento em lote.

## 🧭 Layout do aplicativo

A janela principal abre com **950 px de largura fixa** e **800 px de altura inicial**. A altura pode ser ajustada pelo usuário e respeita o mínimo de 560 px. A interface é organizada em duas abas: **Extrator** e **Manual**. O tema claro é aplicado ao iniciar; o controle gráfico no cabeçalho alterna entre claro e escuro.

### Aba Extrator

O conteúdo da aba é disposto verticalmente, de cima para baixo:

1. **Cabeçalho do app:** mostra o nome “CSV Express” e uma descrição curta da extração. À direita ficam **Selecionar PDF** e o interruptor visual de tema claro/escuro. As dicas de ferramenta explicam a função de cada controle ao posicionar o ponteiro sobre ele.
2. **Entrada de PDFs:** área tracejada para arrastar e soltar um ou mais arquivos PDF. Também é possível selecionar PDFs pelo botão do cabeçalho. Após carregar arquivos, essa área se compacta para liberar mais espaço à pré-visualização; continua disponível para adicionar outros documentos.
3. **Cartões de resumo:** três cartões apresentam a quantidade de PDFs carregados, o total de minutas extraídas e a data ou datas dos romaneios. Antes do processamento, os números começam em zero e a data aparece como “-”.
4. **Busca e resultados:** o campo **Filtrar minuta...** filtra a tabela conforme o texto digitado, procurando tanto na minuta como no nome do PDF de origem. A tabela contém as colunas **#**, **Minuta Extraída**, **Arquivo de Origem** e **Data**. Ela é somente leitura: clicar numa linha copia a minuta para a área de transferência e o status confirma a cópia. A altura das linhas é fixa.
5. **Estado sem resultados:** antes de carregar arquivos, a área de resultados orienta a adicionar PDFs. Durante a leitura, mostra que o processamento está em andamento. Após a leitura, informa quando nenhum número de minuta foi encontrado; se os PDFs falharem, orienta a consultar o resumo de falhas.
6. **Status e progresso:** o status mostra o arquivo em processamento, a quantidade de minutas carregadas, a confirmação de cópia ou a conclusão sem resultados. A barra de progresso aparece durante o processamento.
7. **Ações no rodapé:** **Limpar Lista** remove os arquivos e resultados da sessão; **Abrir Pasta Destino** abre a pasta do CSV gerado; **Exportar para CSV** permite escolher o nome e o local para salvar as minutas. Os botões são habilitados quando a ação está disponível e contam com dicas de ferramenta.

Quando um ou mais PDFs não puderem ser lidos, ao final do processamento é exibido um resumo com a quantidade de falhas, o nome de cada arquivo (até oito listados) e a mensagem de erro correspondente. Se houver mais falhas, o resumo informa quantos arquivos adicionais não foram detalhados.

### Aba Manual

A aba Manual usa rolagem vertical para caber em janelas menores. No topo, apresenta o logo LATAM sem um bloco de fundo branco. Abaixo há **um único bloco cinza** que reúne o título “Manual de uso”, uma introdução, as quatro etapas (adicionar PDFs, conferir a extração, exportar CSV e localizar o arquivo ou limpar a lista) e a observação de que PDFs digitalizados como imagem não podem ser extraídos como texto. O conteúdo permanece agrupado em um só painel.

### Comportamento visual

- A paleta da interface usa índigo como cor primária e coral como cor secundária; o tema escuro adapta fundos, textos, cartões, tabela e área de entrada.
- A área de entrada é ampla no estado inicial e compacta depois que PDFs são carregados, mantendo espaço para arrastar mais arquivos.
- Os cartões de resumo, a tabela e as mensagens de estado atualizam conforme os arquivos são processados, limpos ou filtrados.
- A janela mantém a largura de 950 px; o conteúdo pode acompanhar a altura disponível, com altura mínima de 560 px.

## 🎨 Paleta de cores

- **Primária — Índigo:** `#2A0087` (RGB 42, 0, 135). Usada em ações principais, seleção e realces da interface.
- **Secundária — Coral:** `#EE1750` (RGB 238, 23, 80). Usada em ações secundárias, estados de interação e detalhes de destaque.

## 📂 Como Usar
- **Interface Gráfica**: Abra `CSV Express.desktop` para iniciar com o ícone personalizado, ou execute `CSVExpress`.
- **Linha de Comando**:
  ```bash
  ./CSVExpress arquivo.pdf
  ```
Versao Linux e Windows

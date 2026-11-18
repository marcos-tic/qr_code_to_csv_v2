# Qualidade e acessibilidade

## Verificações automatizadas

O workflow `.github/workflows/ci.yml` roda em Ubuntu e Windows. Ele instala as dependências, compila os módulos Python e cria os pacotes PyInstaller dos dois aplicativos. Para repetir a checagem de sintaxe localmente:

```bash
python3 -m compileall -q main.py main_windows.py romaneio_core.py romaneio_express_v2.py
```

Os fluxos de extração e exportação ainda precisam de verificação funcional com PDFs de exemplo mantidos fora do repositório. Esses documentos podem conter dados operacionais; não os adicione ao Git sem confirmar que estão anonimizados.

## Revisão de acessibilidade feita

- Controles principais e tabelas têm nomes acessíveis em português.
- O seletor de tema declara nome acessível, foco por teclado e tratamento de Espaço/Enter.
- A tabela e a busca devem ser verificadas manualmente com teclado e leitor de tela nos sistemas suportados.

Esta inspeção do código não certifica conformidade WCAG. Contraste efetivo, ordem de foco, leitura dos estados dinâmicos e suporte de leitores de tela precisam de validação manual em Windows e Linux.

## Escopo de CI

O CI verifica importação/sintaxe e empacotamento. Não executa testes de comportamento, interface ou leitura de PDFs. A lógica de extração compartilhada está em `romaneio_core.py`, separada da interface para permitir testes unitários focados quando essa cobertura for adicionada.

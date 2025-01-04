# FileWeave: Uma ponte entre sua Codebase e LLMs

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/filipemsilv4/fileweave/blob/master/README.md)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](https://github.com/filipemsilv4/fileweave/blob/master/README.pt-br.md)

Já imaginou poder compartilhar toda a sua codebase com um LLM de forma simples? O FileWeave torna isso possível. Este aplicativo desktop transforma o processo cansativo de copiar múltiplos arquivos em uma operação suave. Desenvolvido com Python e tkinter, o FileWeave ajuda você a criar snapshots perfeitamente formatados do seu código, que os LLMs podem facilmente entender e analisar.

<img width="1391" alt="Screenshot 2024-12-27 at 23 48 56" src="https://github.com/user-attachments/assets/ad26dd50-29b0-45d7-a0ff-ae60dfd7a622" />

## Por que FileWeave?

LLMs modernos como o **Gemini**, com sua enorme janela de contexto de mais de 1M tokens, são excelentes em entender codebases complexas - desde que tenham uma boa visão do todo. Mas preparar essa visão geral tradicionalmente significava copiar e colar tediosamente dezenas de arquivos. O FileWeave transforma esse processo em uma simples operação de apontar e clicar.

Com o FileWeave, você pode:
- Navegar pela estrutura do seu projeto facilmente
- Selecionar exatamente os arquivos que deseja incluir
- Filtrar automaticamente arquivos irrelevantes usando regras do `.gitignore`
- Gerar uma saída perfeitamente formatada pronta para seu LLM
- Copiar tudo para sua área de transferência com um único clique

O resultado? Você passa menos tempo preparando código para análise e mais tempo obtendo insights valiosos do seu LLM.

## Recursos Principais

O FileWeave combina poder com simplicidade:

- **Interface Inteligente**: Uma GUI limpa e intuitiva construída com tkinter
- **Filtragem Inteligente**: Integração perfeita com suas regras do `.gitignore`
- **Controle de Arquivos Ocultos**: Alterne a visibilidade de arquivos ocultos com um clique
- **Saída Otimizada para LLMs**: Gera blocos de código em markdown com identificadores de linguagem e separadores claros de arquivos
- **Compatibilidade Multiplataforma**: Funciona em macOS, Windows e Linux
- **Atalhos de Teclado**: Acesso rápido com ⌘O/Ctrl+O para seleção de diretório e ⌘C/Ctrl+C para copiar

## Como Começar

O FileWeave usa Poetry para gerenciamento de dependências. Veja como começar:

1. **Instale o Poetry** (caso ainda não tenha):
   Visite a [documentação do Poetry](https://python-poetry.org/docs/#installation) para instruções detalhadas.

2. **Configure o FileWeave**:
   ```bash
   git clone https://github.com/filipemsilv4/fileweave.git
   cd fileweave
   poetry install
   ```

3. **Inicie o aplicativo**:
   ```bash
   poetry run python fileweave/main.py
   ```

## Usando o FileWeave

1. Inicie o FileWeave
2. Selecione o diretório raiz do seu projeto
3. Ajuste as configurações de visibilidade se necessário
4. Escolha os arquivos que deseja incluir
5. Gere sua saída combinada
6. Copie para a área de transferência e compartilhe com seu LLM

## Participe da Comunidade

Suas contribuições podem tornar o FileWeave ainda melhor! Seja um bug encontrado, uma sugestão de recurso ou código para contribuir, sua participação é bem-vinda através de issues e pull requests.

## Licença

O FileWeave está disponível sob a Licença MIT. Consulte o arquivo `LICENSE` para detalhes.

## Agradecimentos

Agradecimento especial à biblioteca `pathspec` por fornecer os recursos de análise do `.gitignore`.

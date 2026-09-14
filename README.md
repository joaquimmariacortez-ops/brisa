# joaquimtabuadas
tabuadas 
# Brisa

A **Brisa** é uma linguagem de programação nova, feita para ser escrita em
arquivos. Ela não tem console interativo: você cria um arquivo com a extensão
`.brisa` e o executa.

## Começar

É necessário ter Python 3 instalado. No terminal, dentro desta pasta, execute:

```bash
python3 brisa.py exemplos/boas-vindas.brisa
```

Para criar um programa seu, faça por exemplo o arquivo `meu-programa.brisa`:

```brisa
crie pessoa = "Ana"
diga "Olá, " + pessoa

repita 2:
  diga "Estou em um arquivo!"
```

Depois execute `python3 brisa.py meu-programa.brisa`.

## Palavras da linguagem

| Forma | O que faz |
| --- | --- |
| `crie nome = valor` | guarda um valor com um nome |
| `diga valor` | escreve algo na tela |
| `repita número:` | repete o bloco indentado abaixo |
| `se condição:` | executa o bloco quando a condição é verdadeira |

Use dois espaços para formar um bloco abaixo de `repita` ou `se`. Os valores
podem ser textos, números, contas (`+`, `-`, `*`, `/`, `%`, `**`), comparações
e os nomes criados anteriormente.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

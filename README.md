# 🔓 ZipCracker - Quebrador Avançado de Senhas ZIP

![Screenshot](screenshot.png)

Ferramenta profissional para recuperação de senhas de arquivos ZIP com suporte a AES-256, interface moderna e relatórios detalhados.

## ✨ Recursos Premium

- 🖥️ Interface gráfica intuitiva com tema escuro
- 📊 Estatísticas em tempo real (velocidade, tempo restante)
- 🔍 Suporte a criptografia AES-128 e AES-256
- 📈 Visualização detalhada do progresso
- ⚡ Multiplataforma (Linux, Windows, macOS)
- 📁 Seletor de arquivos integrado
- 🛑 Controle de processo (pausar/continuar)
- 📋 Log de atividades completo

## 🛠️ Pré-requisitos

- Python 3.10 ou superior
- Ubuntu/Debian (recomendado) ou outro Linux
- 100MB de espaço livre para wordlists

## 📦 Instalação Rápida

1. Clone o repositório ou baixe os arquivos
2. Execute o script de instalação:

```bash
chmod +x install.sh
./install.sh
```

🖥️ Como Usar a Versão Gráfica

Execute o comando:

`./zipcracker`

Ou alternativamente:

`python3 zipcracker_gui.py`

Passo a Passo GUI:

    Clique em "Procurar..." para selecionar o arquivo ZIP

    Selecione o arquivo de wordlist (ex: rockyou.txt)

    Clique em "Iniciar Ataque"

    Acompanhe o progresso na tela

⌨️ Como Usar a Versão CLI

Execute o comando:

`./zipcracker_cli.py arquivo.zip wordlist.txt [--verbose]`

Exemplo avançado:

`./zipcracker_cli.py documento.zip /usr/share/wordlists/rockyou.txt -v`

Opções da CLI:

    -v ou --verbose: Ativa modo detalhado

    Sem argumentos: Mostra ajuda

📂 Wordlists Recomendadas

O ZipCracker inclui automaticamente:

    ./wordlists/rockyou.txt (baixada durante instalação)

Outras wordlists populares:

    /usr/share/wordlists/seclists/

    /usr/share/wordlists/rockyou.txt

    Wordlists personalizadas (crie seu próprio arquivo .txt)

⚙️ Tecnologias Utilizadas

    Python 3.10+

    PyQt5/PyQtChart para interface gráfica

    PyZipper para descriptografia AES

    Colorama para cores no terminal

    Bibliotecas padrão para máxima compatibilidade

⚠️ Considerações Éticas e Legais

Este software destina-se exclusivamente para:

    Recuperação de arquivos pessoais

    Testes de segurança autorizados

    Pesquisa acadêmica em criptografia

❌ Nunca utilize para:

    Violar sistemas sem permissão

    Burlar proteções de software

    Qualquer atividade ilegal

💡 Dicas Avançadas

    Para arquivos grandes:
    
```
nohup ./zipcracker_cli.py grande_arquivo.zip wordlist.txt > log.txt &
```

*Criando wordlists personalizadas:*
    
`crunch 6 8 0123456789 -o numeros.txt`

*Monitorando uso de recursos:*

`watch -n 1 'ps aux | grep zipcracker'`


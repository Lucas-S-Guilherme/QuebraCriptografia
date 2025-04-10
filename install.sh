#!/bin/bash

# Cria ambiente virtual
python3 -m venv venv

# Ativa o ambiente
source venv/bin/activate

# Instala dependências
pip install pyzipper pyqt5

# Dá permissão de execução
chmod +x zipcracker_gui.py
chmod +x zipcracker_cli.py

# Cria atalho no sistema
echo '#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 zipcracker_gui.py "$@"' > zipcracker

chmod +x zipcracker

echo ""
echo "Instalação concluída!"
echo "Agora você pode executar a versão gráfica com: ./zipcracker"
echo "Ou para a versão CLI: ./zipcracker_cli.py arquivo.zip wordlist.txt"
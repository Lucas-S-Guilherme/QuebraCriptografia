#!/bin/bash

# Verifica se é Ubuntu/Debian
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [ "$ID" = "ubuntu" ] || [ "$ID" = "debian" ]; then
        echo "Instalando dependências do sistema..."
        sudo apt update
        sudo apt install -y python3-venv python3-pip p7zip-full python3-pyqt5 python3-pyqt5.qtchart
    fi
fi

# Cria ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv

# Ativa o ambiente
source venv/bin/activate

# Instala dependências Python
echo "Instalando dependências Python..."
pip install pyzipper colorama

# Verifica se o QtChart está acessível
python3 -c "from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando PyQtChart via pip..."
    pip install PyQtChart
fi

# Download da wordlist rockyou.txt se não existir
if [ ! -f "wordlists/rockyou.txt" ]; then
    echo "Baixando wordlist rockyou.txt..."
    mkdir -p wordlists
    wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O wordlists/rockyou.txt
fi

# Cria atalho no sistema
echo "Criando atalho 'zipcracker'..."
cat > zipcracker << 'EOL'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 zipcracker_gui.py "$@"
EOL

chmod +x zipcracker
chmod +x zipcracker_cli.py
chmod +x zipcracker_gui.py

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║          INSTALAÇÃO CONCLUÍDA COM SUCESSO!       ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Agora você pode executar:"
echo ""
echo "  Versão gráfica: ./zipcracker"
echo "  Versão CLI:     ./zipcracker_cli.py arquivo.zip wordlist.txt"
echo ""
echo "Dica: Experimente a wordlist incluída: ./wordlists/rockyou.txt"
#!/usr/bin/env python3
import sys
import pyzipper
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QFileDialog,
                            QProgressBar, QMessageBox, QTextEdit)
from PyQt5.QtCore import QThread, pyqtSignal

class ZipCrackerThread(QThread):
    update_signal = pyqtSignal(str, int, int)
    result_signal = pyqtSignal(str, bool)

    def __init__(self, zip_file, wordlist):
        super().__init__()
        self.zip_file = zip_file
        self.wordlist = wordlist
        self.running = True

    def run(self):
        try:
            with pyzipper.AESZipFile(self.zip_file) as zf:
                with open(self.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                    total_words = sum(1 for _ in f)
                    f.seek(0)
                    
                    for i, word in enumerate(f, 1):
                        if not self.running:
                            return
                        
                        password = word.strip()
                        try:
                            zf.extractall(pwd=password.encode())
                            self.result_signal.emit(password, True)
                            return
                        except (RuntimeError, pyzipper.BadZipFile):
                            if i % 100 == 0:
                                self.update_signal.emit(password, i, total_words)
                            continue
                        except Exception as e:
                            self.result_signal.emit(f"Erro: {e}", False)
                            return
            
            self.result_signal.emit("Senha não encontrada na wordlist", False)
        except Exception as e:
            self.result_signal.emit(f"Erro: {e}", False)

    def stop(self):
        self.running = False

class ZipCrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZipCracker - Quebrador de Senhas ZIP")
        self.setGeometry(100, 100, 500, 400)
        
        self.thread = None
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Arquivo ZIP
        self.lbl_zip = QLabel("Arquivo ZIP:")
        self.txt_zip = QLineEdit()
        self.btn_zip = QPushButton("Procurar...")
        self.btn_zip.clicked.connect(self.browse_zip)
        
        # Wordlist
        self.lbl_wordlist = QLabel("Wordlist:")
        self.txt_wordlist = QLineEdit()
        self.btn_wordlist = QPushButton("Procurar...")
        self.btn_wordlist.clicked.connect(self.browse_wordlist)
        
        # Progresso
        self.progress = QProgressBar()
        self.lbl_status = QLabel("Pronto para iniciar")
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        
        # Botões
        self.btn_start = QPushButton("Iniciar")
        self.btn_start.clicked.connect(self.start_cracking)
        self.btn_stop = QPushButton("Parar")
        self.btn_stop.clicked.connect(self.stop_cracking)
        self.btn_stop.setEnabled(False)
        
        # Adicionando widgets ao layout
        layout.addWidget(self.lbl_zip)
        layout.addWidget(self.txt_zip)
        layout.addWidget(self.btn_zip)
        layout.addWidget(self.lbl_wordlist)
        layout.addWidget(self.txt_wordlist)
        layout.addWidget(self.btn_wordlist)
        layout.addWidget(self.progress)
        layout.addWidget(self.lbl_status)
        layout.addWidget(self.txt_log)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_stop)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def browse_zip(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecione o arquivo ZIP", "", "ZIP Files (*.zip)")
        if file:
            self.txt_zip.setText(file)
    
    def browse_wordlist(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecione a wordlist", "", "Text Files (*.txt)")
        if file:
            self.txt_wordlist.setText(file)
    
    def start_cracking(self):
        zip_file = self.txt_zip.text()
        wordlist = self.txt_wordlist.text()
        
        if not zip_file or not wordlist:
            QMessageBox.warning(self, "Aviso", "Selecione o arquivo ZIP e a wordlist!")
            return
        
        self.thread = ZipCrackerThread(zip_file, wordlist)
        self.thread.update_signal.connect(self.update_progress)
        self.thread.result_signal.connect(self.show_result)
        self.thread.start()
        
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.lbl_status.setText("Processando...")
        self.txt_log.append(f"Iniciando ataque ao arquivo: {zip_file}")
        self.txt_log.append(f"Usando wordlist: {wordlist}")
    
    def stop_cracking(self):
        if self.thread:
            self.thread.stop()
            self.thread.wait()
            self.lbl_status.setText("Interrompido pelo usuário")
            self.txt_log.append("Processo interrompido pelo usuário")
            self.btn_start.setEnabled(True)
            self.btn_stop.setEnabled(False)
    
    def update_progress(self, password, current, total):
        percent = int((current / total) * 100)
        self.progress.setValue(percent)
        self.lbl_status.setText(f"Testando... {current}/{total} ({percent}%) - Última tentativa: {password}")
    
    def show_result(self, message, success):
        if success:
            self.txt_log.append(f"\n[+] Senha encontrada: {message}")
            QMessageBox.information(self, "Sucesso", f"Senha encontrada: {message}")
        else:
            self.txt_log.append(f"\n[-] {message}")
            if "Erro" not in message:
                QMessageBox.warning(self, "Resultado", message)
            else:
                QMessageBox.critical(self, "Erro", message)
        
        self.progress.setValue(100)
        self.lbl_status.setText("Concluído" if success else "Falha")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZipCrackerGUI()
    window.show()
    sys.exit(app.exec_())
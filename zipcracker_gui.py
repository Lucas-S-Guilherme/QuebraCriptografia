#!/usr/bin/env python3
import sys
import pyzipper
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QFileDialog,
                            QProgressBar, QMessageBox, QTextEdit, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QColor

class ZipCrackerThread(QThread):
    update_signal = pyqtSignal(str, int, int, float)
    result_signal = pyqtSignal(str, bool)

    def __init__(self, zip_file, wordlist):
        super().__init__()
        self.zip_file = zip_file
        self.wordlist = wordlist
        self.running = True
        self.start_time = None

    def run(self):
        try:
            self.start_time = time.time()
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
                            elapsed = time.time() - self.start_time
                            speed = i / elapsed if elapsed > 0 else 0
                            self.update_signal.emit(password, i, total_words, speed)
                            self.result_signal.emit(password, True)
                            return
                        except (RuntimeError, pyzipper.BadZipFile):
                            if i % 100 == 0:
                                elapsed = time.time() - self.start_time
                                speed = i / elapsed if elapsed > 0 else 0
                                self.update_signal.emit(password, i, total_words, speed)
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
        self.setWindowTitle("ZipCracker Pro - Quebrador de Senhas ZIP")
        self.setGeometry(100, 100, 700, 500)
        self.thread = None
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Configuração do tema
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #e0e0e0;
                font-weight: bold;
            }
            QLineEdit, QTextEdit {
                background-color: #3b3b3b;
                color: #ffffff;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                min-width: 80px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #555;
            }
            QPushButton#stopButton {
                background-color: #f44336;
            }
            QPushButton#stopButton:hover {
                background-color: #d32f2f;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 3px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
        """)

        # Painel de configuração
        config_panel = QWidget()
        config_layout = QHBoxLayout()
        
        # Arquivo ZIP
        zip_group = QWidget()
        zip_layout = QVBoxLayout()
        self.lbl_zip = QLabel("Arquivo ZIP:")
        self.txt_zip = QLineEdit()
        self.btn_zip = QPushButton("Procurar...")
        self.btn_zip.clicked.connect(self.browse_zip)
        zip_layout.addWidget(self.lbl_zip)
        zip_layout.addWidget(self.txt_zip)
        zip_layout.addWidget(self.btn_zip)
        zip_group.setLayout(zip_layout)
        
        # Wordlist
        wordlist_group = QWidget()
        wordlist_layout = QVBoxLayout()
        self.lbl_wordlist = QLabel("Wordlist:")
        self.txt_wordlist = QLineEdit()
        self.btn_wordlist = QPushButton("Procurar...")
        self.btn_wordlist.clicked.connect(self.browse_wordlist)
        wordlist_layout.addWidget(self.lbl_wordlist)
        wordlist_layout.addWidget(self.txt_wordlist)
        wordlist_layout.addWidget(self.btn_wordlist)
        wordlist_group.setLayout(wordlist_layout)
        
        config_layout.addWidget(zip_group)
        config_layout.addWidget(wordlist_group)
        config_panel.setLayout(config_layout)
        main_layout.addWidget(config_panel)
        
        # Barra de progresso
        self.progress = QProgressBar()
        main_layout.addWidget(self.progress)
        
        # Status
        self.lbl_status = QLabel("Pronto para iniciar")
        self.lbl_status.setStyleSheet("font-size: 14px; color: #4CAF50;")
        main_layout.addWidget(self.lbl_status)
        
        # Estatísticas
        self.lbl_stats = QLabel()
        self.lbl_stats.setStyleSheet("font-size: 12px; color: #aaaaaa;")
        main_layout.addWidget(self.lbl_stats)
        
        # Log
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("font-family: monospace;")
        main_layout.addWidget(self.txt_log)
        
        # Botões
        btn_panel = QWidget()
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("Iniciar Ataque")
        self.btn_start.clicked.connect(self.start_cracking)
        self.btn_stop = QPushButton("Parar")
        self.btn_stop.setObjectName("stopButton")
        self.btn_stop.clicked.connect(self.stop_cracking)
        self.btn_stop.setEnabled(False)
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        btn_panel.setLayout(btn_layout)
        main_layout.addWidget(btn_panel)
        
        central_widget.setLayout(main_layout)
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
        
        self.txt_log.clear()
        self.thread = ZipCrackerThread(zip_file, wordlist)
        self.thread.update_signal.connect(self.update_progress)
        self.thread.result_signal.connect(self.show_result)
        self.thread.start()
        
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.lbl_status.setText("Processando...")
        self.txt_log.append(f"[*] Iniciando ataque ao arquivo: {zip_file}")
        self.txt_log.append(f"[*] Usando wordlist: {wordlist}")
    
    def stop_cracking(self):
        if self.thread:
            self.thread.stop()
            self.thread.wait()
            self.lbl_status.setText("Interrompido pelo usuário")
            self.txt_log.append("[!] Processo interrompido pelo usuário")
            self.btn_start.setEnabled(True)
            self.btn_stop.setEnabled(False)
    
    def update_progress(self, password, current, total, speed):
        percent = int((current / total) * 100)
        elapsed = time.time() - self.thread.start_time
        remaining = (elapsed / current) * (total - current) if current > 0 else 0
        
        self.progress.setValue(percent)
        self.lbl_status.setText(
            f"Testando... {current}/{total} ({percent}%) | "
            f"Velocidade: {speed:.0f} p/s | "
            f"Última tentativa: {password[:20]}{'...' if len(password) > 20 else ''}"
        )
        
        self.lbl_stats.setText(
            f"Tempo decorrido: {timedelta(seconds=int(elapsed))} | "
            f"Tempo estimado restante: {timedelta(seconds=int(remaining))}"
        )
    
    def show_result(self, message, success):
        if success:
            elapsed = time.time() - self.thread.start_time
            self.txt_log.append(f"\n[+] SENHA ENCONTRADA: {message}")
            self.txt_log.append(f"[+] Tempo total: {timedelta(seconds=int(elapsed))}")
            QMessageBox.information(
                self, 
                "Sucesso", 
                f"<b>Senha encontrada com sucesso!</b><br><br>"
                f"Senha: <code>{message}</code><br>"
                f"Tempo: {timedelta(seconds=int(elapsed))}",
                QMessageBox.Ok
            )
            self.lbl_status.setText("Senha encontrada!")
            self.lbl_status.setStyleSheet("color: #4CAF50; font-weight: bold;")
        else:
            self.txt_log.append(f"\n[-] {message}")
            if "Erro" not in message:
                QMessageBox.warning(self, "Resultado", message)
            else:
                QMessageBox.critical(self, "Erro", message)
            self.lbl_status.setText("Falha - Senha não encontrada")
            self.lbl_status.setStyleSheet("color: #f44336; font-weight: bold;")
        
        self.progress.setValue(100)
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

if __name__ == "__main__":
    from datetime import timedelta
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = ZipCrackerGUI()
    window.show()
    sys.exit(app.exec_())
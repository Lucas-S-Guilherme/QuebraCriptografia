#!/usr/bin/env python3
import pyzipper
import argparse
import time
from datetime import timedelta
import os
import sys
from colorama import init, Fore, Back, Style

init()  # Inicializa colorama

class ZipCracker:
    def __init__(self, zip_file, wordlist):
        self.zip_file = zip_file
        self.wordlist = wordlist
        self.start_time = None
        self.last_update = 0
        self.total_words = 0
        self.tested = 0
        self.password_found = False

    def print_progress(self, password):
        current_time = time.time()
        if current_time - self.last_update >= 0.1:  # Atualiza a cada 100ms
            elapsed = timedelta(seconds=int(current_time - self.start_time))
            progress = (self.tested / self.total_words) * 100
            speed = self.tested / (current_time - self.start_time) if (current_time - self.start_time) > 0 else 0
            
            sys.stdout.write(
                f"\r{Fore.YELLOW}[*] Progresso: {progress:.2f}% | "
                f"Testadas: {self.tested:,}/{self.total_words:,} | "
                f"Velocidade: {speed:,.0f} p/s | "
                f"Tempo: {elapsed} | "
                f"Última tentativa: {Fore.CYAN}{password[:20]}{'...' if len(password) > 20 else ''}{Style.RESET_ALL}"
            )
            sys.stdout.flush()
            self.last_update = current_time

    def crack(self):
        try:
            self.start_time = time.time()
            print(f"{Fore.GREEN}\n╔══════════════════════════════════════════════════╗")
            print(f"║{Fore.YELLOW}          ZIPCRACKER - QUEBRADOR DE SENHAS          {Fore.GREEN}║")
            print(f"╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[*] Arquivo ZIP: {Fore.WHITE}{self.zip_file}")
            print(f"{Fore.BLUE}[*] Wordlist: {Fore.WHITE}{self.wordlist}")
            
            # Conta o número de palavras na wordlist
            print(f"{Fore.YELLOW}[*] Contando palavras na wordlist...{Style.RESET_ALL}")
            with open(self.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                self.total_words = sum(1 for _ in f)
            
            print(f"\n{Fore.MAGENTA}[*] Iniciando ataque...{Style.RESET_ALL}")
            
            with pyzipper.AESZipFile(self.zip_file) as zf:
                with open(self.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                    for password in f:
                        password = password.strip()
                        self.tested += 1
                        
                        try:
                            zf.extractall(pwd=password.encode())
                            self.password_found = True
                            self.print_progress(password)
                            return password
                        except (RuntimeError, pyzipper.BadZipFile):
                            self.print_progress(password)
                            continue
                        except Exception as e:
                            print(f"\n{Fore.RED}[!] Erro: {e}{Style.RESET_ALL}")
                            return None
            
            return None
        except FileNotFoundError as e:
            print(f"\n{Fore.RED}[!] Arquivo não encontrado: {e}{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"\n{Fore.RED}[!] Erro inesperado: {e}{Style.RESET_ALL}")
            return None

def main():
    parser = argparse.ArgumentParser(description='Quebrador de senhas ZIP avançado')
    parser.add_argument('zip_file', help='Arquivo ZIP protegido por senha')
    parser.add_argument('wordlist', help='Arquivo de wordlist contendo senhas possíveis')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')
    
    args = parser.parse_args()
    
    cracker = ZipCracker(args.zip_file, args.wordlist)
    password = cracker.crack()
    
    if cracker.password_found:
        elapsed = timedelta(seconds=int(time.time() - cracker.start_time))
        print(f"\n\n{Fore.GREEN}╔══════════════════════════════════════════════════╗")
        print(f"║{Back.GREEN}{Fore.BLACK}          SENHA ENCONTRADA COM SUCESSO!          {Style.RESET_ALL}{Fore.GREEN}║")
        print(f"╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Senha encontrada: {Fore.WHITE}{password}")
        print(f"{Fore.GREEN}[+] Tempo total: {Fore.WHITE}{elapsed}")
        print(f"{Fore.GREEN}[+] Tentativas: {Fore.WHITE}{cracker.tested:,}/{cracker.total_words:,}")
        print(f"{Fore.GREEN}[+] Velocidade média: {Fore.WHITE}{cracker.tested/(time.time() - cracker.start_time):,.0f} senhas/segundo{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}[-] Senha não encontrada na wordlist{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import pyzipper
import argparse
from time import time

def crack_zip(zip_file, wordlist):
    try:
        with pyzipper.AESZipFile(zip_file) as zf:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                total_words = sum(1 for _ in f)
                f.seek(0)
                
                start_time = time()
                for i, word in enumerate(f, 1):
                    password = word.strip()
                    try:
                        zf.extractall(pwd=password.encode())
                        end_time = time()
                        print(f"\n[+] Senha encontrada: '{password}'")
                        print(f"[+] Tempo decorrido: {end_time - start_time:.2f} segundos")
                        print(f"[+] Tentativas: {i}/{total_words}")
                        return True
                    except (RuntimeError, pyzipper.BadZipFile):
                        # Exibe progresso a cada 1000 tentativas
                        if i % 1000 == 0:
                            print(f"\rTentativa {i}/{total_words} ({i/total_words*100:.1f}%) - Última tentativa: {password}", end='')
                        continue
                    except Exception as e:
                        print(f"\n[!] Erro: {e}")
                        return False
    except FileNotFoundError:
        print("[!] Arquivo ZIP ou wordlist não encontrado")
        return False
    
    print("\n[-] Senha não encontrada na wordlist")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Quebrador de senhas ZIP')
    parser.add_argument('zip_file', help='Arquivo ZIP protegido por senha')
    parser.add_argument('wordlist', help='Arquivo de wordlist contendo senhas possíveis')
    
    args = parser.parse_args()
    
    print(f"[*] Iniciando ataque ao arquivo: {args.zip_file}")
    print(f"[*] Usando wordlist: {args.wordlist}")
    
    if not crack_zip(args.zip_file, args.wordlist):
        print("[!] Falha ao quebrar a senha")
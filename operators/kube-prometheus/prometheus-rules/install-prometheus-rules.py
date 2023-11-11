import subprocess
import os

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Erro ao executar o comando: {command}\nErro: {err.decode('utf-8')}")
        return False
    return True

def install_prometheus_rules():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    rule_files = [f for f in os.listdir(current_dir) if f.endswith('.yaml') and f.startswith("high-memory-usage-rules") or f.startswith("pods-evicted-rules") or f.startswith("pods-restart-rules")]

    for file in rule_files:
        file_path = os.path.join(current_dir, file)
        if run_command(f"kubectl apply -f {file_path}"):
            print(f"Regra {file} instalada com sucesso.")
        else:
            print(f"Falha ao instalar a regra {file}.")

if __name__ == "__main__":
    install_prometheus_rules()

import subprocess
import os

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Erro ao executar o comando: {command}\nErro: {err.decode('utf-8')}")
        return False
    return True

def install_grafana_dashboards():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_files = [f for f in os.listdir(script_dir) if f.endswith('.yaml')]

    for file in dashboard_files:
        file_path = os.path.join(script_dir, file)
        if run_command(f"kubectl apply -f {file_path}"):
            print(f"Dashboard {file} instalado com sucesso.")
        else:
            print(f"Falha ao instalar o dashboard {file}.")

if __name__ == "__main__":
    install_grafana_dashboards()

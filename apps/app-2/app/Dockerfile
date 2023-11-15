# Usa uma imagem base Python oficial
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos requirements.txt para o contêiner
COPY requirements.txt .

# Instala as dependências
RUN pip install -r requirements.txt

# Copia o restante dos arquivos para o contêiner
COPY . .

# Expõe a porta 5000
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]

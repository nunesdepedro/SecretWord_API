FROM python:3.14-slim

WORKDIR /app

# Instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da API
COPY . .

# Cria uma pasta para salvar o banco SQLite (Garante persistência)
RUN mkdir -p /app/data

EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

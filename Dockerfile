# ベースイメージを指定
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー
COPY . .

# Flaskのポートを開ける
EXPOSE 5000

# Flaskアプリの起動コマンド
CMD ["python", "app.py"]

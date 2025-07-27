FROM hub.docker.mirrors.lucien.ink/library/python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
COPY . .
CMD ["python", "main.py"]

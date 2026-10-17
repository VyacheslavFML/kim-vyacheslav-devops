FROM python:3.13-alpine
WORKDIR /app
COPY app/ ./app/
COPY tests/ ./tests/
RUN python -m unittest discover -s tests -v && adduser -D student
USER student
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')" || exit 1
CMD ["python", "-u", "app/main.py"]

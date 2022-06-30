FROM python:3.10-alpine

WORKDIR /application
COPY ./ .
RUN pip install -r requirements.txt
ENV PYTHONPATH="$PYTHONPATH:/application"
ENV PYTHONUNBUFFERED=0
ENTRYPOINT ["python", "-m", "swissre_test", "--file", "stdin", "--destination", "stdout"]
CMD ["--help"]
FROM python:3.12
WORKDIR /cookplanner
COPY . /cookplanner
EXPOSE 8888
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--reload", "--port 1234"]
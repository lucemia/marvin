FROM prefecthq/prefect:2-python3.10

WORKDIR /app

RUN python -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ARG CACHE_BUST=1

RUN echo "Cache bust: ${CACHE_BUST}" && \
    pip install git+https://github.com/PrefectHQ/marvin.git@slackbot#egg=marvin[chromadb]

RUN pip uninstall uvloop -y

COPY setup.py /app/examples/slackbot/community_bot/setup.py

CMD ["uvicorn", "marvin.server:app", "--host", "0.0.0.0", "--port", "4200"]

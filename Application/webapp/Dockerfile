FROM python:3.9.18-slim-bookworm as builder

# Installing dumb-init for better process handling, usually application like Python or Node shouldnt run as process 1
# Didnt installed gcc because there was no need for it
RUN apt-get update && apt-get install -qq -y --no-install-recommends \
    dumb-init \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

#Used multistage for better caching and light weight image
FROM python:3.9.18-slim-bookworm

#Creating non-root user for security reasons
RUN groupadd --gid 1500 user \
    && useradd --uid 1500 --gid 1500 user --home /home/user

WORKDIR /home/user

COPY --from=builder --chown=user:user /root/.local /home/user/.local
COPY --from=builder --chown=user:user /usr/bin/dumb-init /usr/bin/dumb-init

COPY . .

#Its not that necessary but just in case i added these variables :)
ENV PATH=/home/user/.local/bin:$PATH \
    PYTHONPATH=/home/user/.local/lib/python3.9/site-packages

USER user

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["python3","webapp.py"]

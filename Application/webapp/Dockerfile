FROM python:3.9.18-slim-bookworm as builder

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

#Used multistage for better caching and light weight image
FROM python:3.9.18-slim-bookworm 

#Creating non-root user for security reasons
RUN groupadd --gid 1500 user \
    && useradd --uid 1500 --gid 1500 user --home /home/user

# Installing dumb-init for better process handling, usually application like Python or Node shouldnt run as process 1
# Didnt installed gcc because there was no need for it
RUN apt-get update && apt-get install -qq -y --no-install-recommends \
    dumb-init \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

WORKDIR /home/user

COPY --from=builder --chown=user:user /root/.local /home/user/.local

COPY . .

#Its not that necessary but just in case i added these variables :)
ENV PATH=/home/user/.local/bin:$PATH

USER user

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["python3","webapp.py"]

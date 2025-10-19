FROM python:3.11-slim
WORKDIR /opt/chal

# Install uv and dependencies in one layer for better caching
RUN pip install uv

# Create unprivileged unprivileged user. lol.
RUN groupadd -r unprivileged && \
	useradd -r -g unprivileged \
        -d /home/unprivileged \
        -s /bin/bash \
        unprivileged

# Create directories for uv
RUN mkdir -p /home/unprivileged/.cache/uv /home/unprivileged/.local/share/uv

COPY pyproject.toml /opt/chal/pyproject.toml
COPY .python-version /opt/chal/.python-version
COPY uv.lock /opt/chal/uv.lock
RUN chown -R unprivileged:unprivileged /home/unprivileged
RUN chown root:unprivileged /opt/chal && chmod g+w /opt/chal
USER unprivileged
RUN uv sync --locked
USER root
RUN chown root:root /opt/chal && chmod g-w /opt/chal

# Copy application files
COPY . /opt/chal

USER unprivileged
EXPOSE 8000
ENTRYPOINT ["/opt/chal/docker-entrypoint.sh"]


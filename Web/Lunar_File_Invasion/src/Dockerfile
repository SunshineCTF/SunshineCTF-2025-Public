FROM python:3.11-slim
WORKDIR /lunarCMS/internal/staging/decommed/alimuhammadsecured/opt/chal

# Install uv and dependencies in one layer for better caching
RUN pip install uv

# Create unprivileged unprivileged user. lol.
RUN groupadd -r unprivileged && \
	useradd -r -g unprivileged \
        -d /home/unprivileged \
        -s /bin/bash \
        unprivileged

# Create directories and set permissions for uv
RUN mkdir -p /home/unprivileged/.cache/uv /home/unprivileged/.local/share/uv && chown -R unprivileged:unprivileged /home/unprivileged/.cache /home/unprivileged/.local

COPY pyproject.toml pyproject.toml
COPY .python-version .python-version
COPY uv.lock uv.lock


# Change ownership of the working directory and switch to unprivileged user
RUN chown -R unprivileged:unprivileged .
USER unprivileged
RUN uv sync --locked

# Copy application files
COPY --chown=unprivileged:unprivileged . .


# Run the seeder as the unprivileged user during image build so database.db is created
# and owned by unprivileged user (no permission problems at runtime).
# RUN python3 seeder.py
# Run seeder inside the env managed by uv
RUN uv run python seeder.py

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["/lunarCMS/internal/staging/decommed/alimuhammadsecured/opt/chal/docker-entrypoint.sh"]

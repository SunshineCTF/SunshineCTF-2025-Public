FROM debian:bookworm-slim

# Enable 32-bit architecture
RUN dpkg --add-architecture i386

# Install only what's needed to run 32-bit binaries and socat
RUN apt update && apt install -y \
    libc6:i386 \
    libstdc++6:i386 \
    socat \
    file \
    && rm -rf /var/lib/apt/lists/*

# Create user with no shell access (optional security)
RUN useradd -m -s /usr/sbin/nologin ctf

# Add your challenge binary and flag
COPY hal9000.mov /home/ctf/hal9000.mov
COPY flag.txt /home/ctf/flag.txt

# Set permissions
RUN chown -R root:ctf /home/ctf && \
    chmod 750 /home/ctf/hal9000.mov && \
    chmod 640 /home/ctf/flag.txt

# Switch to non-root user
USER ctf
WORKDIR /home/ctf

EXPOSE 25005/tcp

# Expose on port 25005 via socat
CMD socat TCP-LISTEN:25005,reuseaddr,fork EXEC:"./hal9000.mov",stderr,sigint


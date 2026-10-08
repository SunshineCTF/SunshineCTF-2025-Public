# Deployment Guide
<br>

Note: Source code is not provided for this challenge and this NEEDS to be a per instance challenge (see the writeup for why).
## Building and Running the Challenge
1. Make sure `Docker` and `Docker Compose` are installed on your system & make sure the container runtime process is running. 
2. Clone the repository and `cd` into it:
```bash
git clone https://github.com/SunshineCTF/2025-Web-Forge.git
cd 2025-Web-Forge
```
3. Build and start all services
```bash
chmod +x build_challenge.sh
./build_challenge.sh
```

4. Once started, the challenge will be available at:
```cpp
http://<host-ip>:3000/
```
<br>

## Stopping the Challenge
To stop and remove running containers (without deleting volumes):
```bash
docker compose down
```
<br>

## Maintenance Notes
- In order to monitor activity or debug:
```bash
docker compose logs -f forge
```
- The flag is stored inside the `forge` container at `/flag.txt`, and is created at build time.

See [writeup.md](writeup.md) for the solution.

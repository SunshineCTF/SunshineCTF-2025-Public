# HAL9000.mov

Install the "movcc" compiler from github: https://github.com/xoreaxeaxeax/movfuscator
- Might need to install the 32-bit libc as well, see the installation guide in the repo

Compile as follows: `movcc -s -o hal9000.mov hal9000.c`

Deploy binary through Docker: `docker build -t hal9000 .` and `docker run --rm -d -p 25005:25005 hal9000:latest`. Competitors can simply install the necessary dynamic libraries (libc, etc.) through apt! 


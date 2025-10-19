### NOTE:

> [!CAUTION]
> **Do NOT provide source!**
- This will be a `GLOBAL` instance.
- SQLMAP won't work with this, went through all the scan payloads and blocked the one-shot ones.
- blocked a bunch of query keywords that could be used for DOS-es + blocked suspiciously long queries
- The goal of this challenge is for people to learn the classic manual `ORDER BY` and `UNION SELECT` SQL injection technique.


### Building
```bash

chmod +x build_challenge.sh
./build_challenge.sh

```
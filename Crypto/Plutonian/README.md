# Plutonian Crypto

## Crypto (Easy/Medium)

This challenge is focused on abusing NONCE reuse in AES-CTR mode with a portion of known plaintext. Because the same prefix is used along with an initial counter that is incremented by 1 each time the message is sent, the keystream effectively just shifts to the left by one block in each message.

## Deployment

This challenge has a docker component which can be built and deployed with docker-compose.

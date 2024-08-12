# Usage
1. Install chrome driver https://googlechromelabs.github.io/chrome-for-testing/
2. python -m venv venv
3.  Create a `dogs/config.yaml`
```yaml
proxy:
  key: your_proxy_key
  authorization: your_authorization_token
```
4. source venv/bin/activate
5. python __main__.py --add 1 (to add new account)
6. python __main__.py (to claim on all accounts)

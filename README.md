### Running locally

Requirements:
- python >= 3.6
- [pipenv](https://github.com/pypa/pipenv) (install via `pip install pipenv`)

Run the monitor:
- `pipenv install` - Install requirements
- `scripts/copy-config` - Copy config file (some dummy settings are set by default)
- `scripts/run` - Run the monitor

### Running on server

You can use the following systemd service entry:
```
[Unit]
Description=Bitcoin Arbitrage Monitor
After=network-online.target

[Service]
Type=simple
User=bitcoin
Restart=always
WorkingDirectory=/home/bitcoin/bitcoin-arbitrage
ExecStart=/home/bitcoin/bitcoin-arbitrage/scripts/run

[Install]
WantedBy=multi-user.target
```

### Running the tests
Manually: 
- `scripts/test`

With PyCharm:
![image](https://user-images.githubusercontent.com/3121306/34055600-3bde00ae-e1d0-11e7-87dd-5f67eaddab9b.png)

# Bitcoin Arbitrage Trading Bot

<a href="https://www.buymeacoffee.com/mammuth" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

A python monitoring and trading bot which exploits price-spreads between different cryptocurrency exchanges.

<img width="1235" alt="bitcoin-arbitrage-trading-bot" src="https://user-images.githubusercontent.com/3121306/46918330-4ce52400-cfd1-11e8-8c30-1c6dd0758e04.png">

## Capabilities
- Monitoring of spreads between exchanges (eg. Gdax, Bitfinex, Bitstamp, ...)
- Multiple currency pairs configurable (eg. BTC/EUR, ETH/USD, ...)
- Notifications on spread thresholds (eg. spreads of > 200€) via different notification channels (eg. Pushbullet, Mail, ...)
- Automated trading for configured spread thresholds (partly implemented)
- Storing of historical spreads and making them available via a web UI
- Highly [configurable](https://github.com/mammuth/bitcoin-arbitrage-trading-bot/blob/master/bitcoin_arbitrage/monitor/settings_sample.py) (currency pairs, thresholds for each notification channel or trading, historical data, ...)

## Trading Strategy
The following example explains *spreads* between exchanges:

| Exchange | BTC/EUR price |
|----------|---------------|
| Gdax     | 5000€         |
| Bitfinex | 5**6**00€         |

This results in a spread of 600€ for the price of 1 BTC in EUR between Gdax and Bitfinex (this example is not based on ask and bid prices for simplicity reasons, the bot itself uses those correct prices).

### How to exploit this spread?
(example based on above table)

### Strategy 1 (common "arbitrage trading")  
**Preparation:**    
- Store 5000€ on Gdax

**Spread exploitation:**    
- Buy BTC on Gdax for 5000€
- Send BTC from Gdax to Bitfinex
- Pay fees for transaction and wait until it's confirmed
- Sell BTC on Bitfinex for 5600€

**Postprocessing (steps needed to be able to repeat exploit):**    
- Transfer 5600€ from Bitfinex to Gdax to repeat

| Advantages                                 | Disadvantages                                                                     |
|--------------------------------------------|-----------------------------------------------------------------------------------|
| Capital needed: 5000€         | **Risk of price fluctuation** until transaction is confirmed                      |
|                       | Postprocessing partly done manually (SEPA transfer of the euro amount)            |
|                                            | Postprocessing is time-consuming (couple of days for international SEPA transfer) |


### Strategy 2 (used by this trading bot)  
**Preparation:**    
- Store 5000€ on Gdax account
- Store 1 BTC on Bitfinex account

**Spread exploitation:**    
- Buy 1 BTC on Gdax
- Simultaneously sell 1 BTC on Bitfinex

**Postprocessing (steps needed to be able to repeat exploit):**    
- Transfer 5600€ from Bitfinex to Gdax
- Transfer 1 BTC from Gdax to Bitfinex

| Advantages                                                                                       | Disadvantages                                                          |
|--------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| **No real risk of price fluctuation** (whole spread exploitation only takes a couple of seconds) | Same disadvantages as strategy 1 (except the risk of price fluctation) |
|                                                                              | Capital needed: ~ 2x5000€ (fiat currency: 5000€ + BTC worth ~5000€)    |


The following table demonstrates the amount of BTC and fiat stored on the exchanges during the different phases of the execution of the strategy:

**Preparation**

| Exchange | Amount of BTC | Amount of € |
|----------|---------------|-------------|
| Gdax     | 0             | 5000        |
| Bitfinex | 1             | 0           |

**After Spread exploitation**

| Exchange | Amount of BTC | Amount of € |
|----------|---------------|-------------|
| Gdax     | 1             | 0           |
| Bitfinex | 0             | 5600        |

**Profit: 600€** (excluding fees for simplicity)

## Status of project
The strategy worked during the *crypto boom* at the end of 2017 (with spreads of > 700€ several times a week). As of now, spreads are pretty low (< 100€) which renders using the bot risky and less attractive (change of prices during order executions, fees, ...).

- Monitoring works
- Automated trading is partly implemented, but never tested with real accounts
- Reliability isn't as good as it should be when using the bot with real accounts

# Developer Information

The bot itself is placed at [bitcoin_arbitrage/monitor](https://github.com/mammuth/bitcoin-arbitrage/blob/master/bitcoin_arbitrage/monitor/monitor.py) with its entry point / main class being [bitcoin_arbitrage/monitor/monitor.py](https://github.com/mammuth/bitcoin-arbitrage/blob/master/bitcoin_arbitrage/monitor/monitor.py).

The code within `bitcoin_arbitrage/` is a Flask app which is just a *fancy* wrapper for the monitor/bot with a web UI.

Configuration of the bot is done by copying the [settings.py](https://github.com/mammuth/bitcoin-arbitrage/blob/master/bitcoin_arbitrage/monitor/settings_sample.py) file.

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

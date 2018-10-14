Code of the monitor / trading bot is placed within the [`monitor/`](https://github.com/mammuth/bitcoin-arbitrage-trading-bot/blob/master/bitcoin_arbitrage/monitor) directory. Main class is [`monitor/monitor.py`](https://github.com/mammuth/bitcoin-arbitrage-trading-bot/blob/master/bitcoin_arbitrage/monitor/monitor.py). The current directory keeps mainly the flask app. Configuration is done via a [`settings.py` file](https://github.com/mammuth/bitcoin-arbitrage-trading-bot/blob/master/bitcoin_arbitrage/monitor/settings_sample.py).

The monitor gets started in a separate thread when the flask app starts.

We use Gentella Admin for the templates.

Check out the GitHub repo for all the available widgets and components.
https://github.com/afourmy/flask-gentelella

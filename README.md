Sanic-Rollbar
=============

A Rollbar plugin for Sanic, inspired by flask-rollbar.

Free software: MIT license

## Installation

```bash
pip install sanic-rollbar
```    

## Usage

Set your Rollbar token in config file, like:

```python
    ROLLBAR_TOKEN = os.getenv('ROLLBAR_TOKEN')
```

In your Sanic app, initialize the plugin:

```python
    from sanic import Sanic, response
    from sanic_rollbar import SanicRollbar
    from yourapp import config

    app = Sanic(__name__)
    app.config.from_object(config)
    SanicRollbar(app)
```

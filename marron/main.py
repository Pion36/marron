# -*- coding: utf-8 -*-
import requests
from flask import *
from tradedemo2 import tradeDemo2

app = Flask(__name__)

@app.route('/')
def index():
    api = tradeDemo2()

    # レートは外部から取得したもので代用
    info = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=10').json()

    rate = {}
    for i in info:
        rate[i['symbol']] = float(i['price_btc'])

    # 模擬の板情報
    api.addIntent('makeraddress1', 'BTC', 'XRP', 1, 'pass1', 1.6146, rate['BTC']/rate['XRP'])
    api.addIntent('makeraddress2', 'ETH', 'XRP', 2, 'pass2', 0.234659, rate['ETH']/rate['XRP'])
    api.addIntent('makeraddress3', 'BTC', 'BCH', 3, 'pass3', 1.26, rate['BTC']/rate['BCH'])
    api.addIntent('makeraddress4', 'LTC', 'ADA', 4, 'pass4', 15.2465, rate['LTC']/rate['ADA'])
    api.addIntent('makeraddress5', 'ETH', 'XRP', 5, 'pass5', 20.9824, rate['ETH']/rate['XRP'])
    api.addIntent('makeraddress6', 'BTC', 'NEO', 6, 'pass6', 3.65791, rate['BTC']/rate['NEO'])
    api.addIntent('makeraddress7', 'ADA', 'BCH', 7, 'pass7', 97.5, rate['ADA']/rate['BCH'])
    api.addIntent('makeraddress8', 'EOS', 'XRP', 8, 'pass8', 0.3659, rate['EOS']/rate['XRP'])
    api.addIntent('makeraddress9', 'XRP', 'ADA', 9, 'pass9', 5.94213, rate['XRP']/rate['ADA'])
    
    return(render_template('index.html', list=api.watchIntent()))


@app.route('/trade', methods=['GET', 'POST'])
def trade():
    api = tradeDemo2()

    takerAddress = request.form['takerAddress']
    makerAddress = request.form['makerAddress']
    takerAmount = int(request.form['takerAmount'])
    makerAmount = int(request.form['makerAmount'])
    takerCurrency = request.form['takerCurrency']
    makerCurrency = request.form['makerCurrency']

    try:
        api.takerOrder(takerAddress, takerCurrency, makerAmount, makerCurrency, takerAmount=takerAmount)
    except Exception as e:
        print(e)
        return(render_template('result.html', message='取引失敗'))

    return(render_template('result.html', message='取引成功'))


if __name__ == '__main__':
    app.run(port=80)

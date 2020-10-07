from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
import fintech.Model.QTS as qts
import json


def get_stock_list(request):
    if request.method == 'GET':
        try:
            cursor = connection.cursor()
            sql = ("select `Symbol` from Fintech.Stocks")
            cursor.execute(sql)
            stocks = []
            for items in cursor.fetchall():
                stocks.append(items[0])
            return JsonResponse({'stock list': stocks})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'database connection error', 'error': e})

    return JsonResponse({'status': 'fail'})


@require_http_methods(["POST"])
def recommend_sma(request):
    try:
        indicator = 'sma'
        body = json.loads(request.body)
        symbol = body['symbol']['title']
        stock_data = get_stock_price(symbol, body['start'], body['end'])
        ti1, ti2, ti3, ti4, holding_period, profit, strategy = qts.QTS(stock_data['price'], indicator)
        context = {'stock price': stock_data['price'][256:], 'holding period': holding_period, 'profit': profit,
                   'strategy': strategy, 'ti1': ti1, 'ti2': ti2, 'ti3': ti3, 'ti4': ti4}

        return JsonResponse(context)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'fail', 'error': e})


def get_stock_price(symbol, start, end):
    try:
        cursor = connection.cursor()
        sql = ("select `Date`, `Adj Close` from Fintech.{} where `Date` between '{}' and '{}'") \
            .format(symbol, start, end)
        cursor.execute(sql)
        data = {'date': [], 'price': []}
        for items in cursor.fetchall():
            date, price = items
            data['date'].append(date)
            data['price'].append(price)
        sql = ("select `Date`, `Adj Close` from Fintech.{} where `Date` < '{}' ORDER BY `Date` DESC limit 256") \
            .format(symbol, start)

        cursor.execute(sql)
        data_training = {'date': [], 'price': []}
        for items in cursor.fetchall():
            date, price = items
            data_training['date'].append(date)
            data_training['price'].append(price)
        data_training['date'].reverse()
        data_training['price'].reverse()

        data_training['date'].extend(data['date'])
        data_training['price'].extend(data['price'])
        return data_training
    except Exception as e:
        return e


@require_http_methods(["POST"])
def custom(request):
    try:
        indicator = 'sma'
        body = json.loads(request.body)
        symbol = body['symbol']['title']
        stock_data = get_stock_price(symbol, body['start'], body['end'])
        strategy = {'buy1': body['buy1'], 'buy2': body['buy2'], 'sell1': body['sell1'], 'sell2': body['sell2']}
        holding_period, profit = qts.fitness(stock_data['price'],
                                             [body['buy1'], body['buy2'], body['sell1'], body['sell2']], indicator)
        context = {'stock price': stock_data['price'][256:], 'holding period': holding_period, 'profit': profit,
                   'strategy': strategy}
        return JsonResponse(context)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'fail', 'error': e})

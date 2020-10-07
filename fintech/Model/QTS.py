import random
from fintech.Model import TIs as techi

stock = []
ID = 'AAPL'
TI = 'ema'


def fitness(stock, stre, TI):  # 給策略參數  回傳持有區間,收益
    stre[0]
    if (TI == 'sma'):
        date_ti, l = techi.sma(stock)
    elif (TI == 'wma'):
        date_ti, l = techi.wma(stock)
    elif (TI == 'ema'):
        date_ti, l = techi.ema(stock)
    elif (TI == 'rsi'):
        date_ti, l = techi.rsi(stock)
    fund = 1000000  # 資金
    hold = []
    b = 0
    for d in range(256, l):  # 訓練期開始
        if (b == 0):
            tmp = 0
        else:
            tmp = 1
        if (date_ti[d - 255][int(stre[0])] > date_ti[d - 255][int(stre[1])] and
                date_ti[d - 256][int(stre[0])] <= date_ti[d - 256][int(stre[1])] and d != l - 1 and b == 0):
            remain = float(fund % float(stock[d]))
            shares = int((fund - remain) / float(stock[d]))
            fund -= shares * float(stock[d])
            b = 1
            print(date_ti[d - 255][int(stre[0])], '>', date_ti[d - 255][int(stre[1])],
                  date_ti[d - 256][int(stre[0])], '<', date_ti[d - 256][int(stre[1])], stre[0], stre[1])
        elif (date_ti[d - 255][int(stre[2])] < date_ti[d - 255][int(stre[3])] and
              date_ti[d - 256][int(stre[2])] >= date_ti[d - 256][int(stre[3])] and b == 1):
            fund += float(stock[d]) * shares + remain
            b = 0
        elif (d == l - 1 and b == 1):
            fund += float(stock[d]) * shares + remain
            b = 0
        if (b == 1):
            hold.append(float(stock[d]))
        else:
            if (tmp == 1):
                hold.append(float(stock[d]))
            else:
                hold.append('NaN')
    return hold, (fund - 1000000.0) / 1000000.0


def QTS(stock, TI):  # 給股價 回傳最佳策略,收益,持有
    if (TI == 'sma'):
        date_ti, l = techi.sma(stock)
    elif (TI == 'wma'):
        date_ti, l = techi.wma(stock)
    elif (TI == 'ema'):
        date_ti, l = techi.ema(stock)
    elif (TI == 'rsi'):
        date_ti, l = techi.rsi(stock)
    fund = 1000000  #
    beta = [0.5] * 32
    theta = 0.002
    partical = 10
    generation = 30
    pm = [[0] * 32 for _ in range(partical)]
    gbest = [0] * 32
    gbest_prof = 0
    pworst = [0] * 32
    pworst_prof = 2000000
    stre = [0] * 4
    hold = []
    b = 0  #
    ti = [[], [], [], []]
    bs = [0, 0, 0, 0]
    stre_sum = 0
    for _ in range(generation):  # 代數
        # print("generation:" + str(g+1))
        for p in range(partical):  # 粒子
            # print("partical:" + str(p+1))
            for s in range(32):  # 32bit策略
                if (random.random() > beta[s]):
                    pm[p][s] = 0
                    if (s % 8 == 7):
                        stre[int(s / 8)] = stre_sum
                        stre_sum = 0
                else:
                    pm[p][s] = 1
                    stre_sum += pow(2, s % 8)
                    if (s % 8 == 7):
                        stre[int(s / 8)] = stre_sum
                        stre_sum = 0
            for d in range(256, l):  # 訓練期開始
                if (b == 0):
                    tmp = 0
                else:
                    tmp = 1
                if (date_ti[d - 255][int(stre[0])] > date_ti[d - 255][int(stre[1])] and
                        date_ti[d - 256][int(stre[0])] <= date_ti[d - 256][int(stre[1])] and d != l - 1 and b == 0):
                    remain = float(fund % float(stock[d]))
                    shares = int((fund - remain) / float(stock[d]))
                    fund -= shares * float(stock[d])
                    b = 1
                    print(date_ti[d - 255][int(stre[0])], '>', date_ti[d - 255][int(stre[1])],
                          date_ti[d - 256][int(stre[0])], '<', date_ti[d - 256][int(stre[1])], stre[0], stre[1])
                elif (date_ti[d - 255][int(stre[2])] < date_ti[d - 255][int(stre[3])] and
                      date_ti[d - 256][int(stre[2])] >= date_ti[d - 256][int(stre[3])] and b == 1):
                    fund += float(stock[d]) * shares + remain
                    b = 0
                elif (d == l - 1 and b == 1):
                    fund += float(stock[d]) * shares + remain
                    b = 0
                if (b == 1):
                    hold.append(float(stock[d]))
                else:
                    if (tmp == 1):
                        hold.append(float(stock[d]))
                    else:
                        hold.append('NaN')
            # hold,fund = fitness(date_ti,stre)
            # print(shares)
            # print(fund)
            # print(hold)
            if (fund >= gbest_prof):
                gbest_prof = fund
                best_stre = stre
                best_hold = hold
                gbest = pm[p]
                bs[0] = best_stre[0] + 1
                bs[1] = best_stre[1] + 1
                bs[2] = best_stre[2] + 1
                bs[3] = best_stre[3] + 1
            if (fund < pworst_prof):
                pworst = pm[p]
            hold = []  #
            fund = 1000000  #
        for i in range(32):
            if (gbest[i] == 1 and pworst[i] == 0):
                beta[i] += theta
            elif (gbest[i] == 0 and pworst[i] == 1):
                beta[i] -= theta
        # if(){
        #     jump
        # }        
        pworst = [0] * 32
        pworst_prof = 2000000
    for i in range(4):
        for j in range(l - 256):
            ti[i].append(date_ti[j][bs[i] - 1])
    return ti[0], ti[1], ti[2], ti[3], best_hold, (gbest_prof - 1000000) / 1000000, {'buy1': bs[0], 'buy2': bs[1],
                                                                                     'sell1': bs[2], 'sell2': bs[3]}

    # ddic = {'buy1':ti[0],'buy2':ti[1],'sell1':ti[2],'sell2':ti[3],
    # 'stock price':stock[256:],'holding period':best_hold,'profit':gbest_prof,
    # 'strategy':{'buy1':bs[0],'buy2':bs[1],'sell1':bs[2],'sell2':bs[3]}}
    # return ddic


for i in range(1):
    dd = QTS(stock, TI)
    print(dd)

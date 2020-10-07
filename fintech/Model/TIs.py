def sma(stock):  # 計算訓練期每天的MA(1-256) 回傳二維陣列,stock長度
    l = len(stock)
    date_sma = [[0] * 256 for _ in range(l - 255)]
    numer = 0
    denomi = 0
    for i in range(1, l - 254):  # i代表每個訓練天數
        for j in range(1, 257):  # j代表訓練天數的MA(1-256)
            for k in range(1, j + 1):  # k計算MA[j]
                numer += float(stock[255 + i - k])
                denomi += 1
            date_sma[i - 1][j - 1] = numer / denomi
            numer = 0
            denomi = 0
    return date_sma, l


def wma(stock):  # 計算訓練期每天的MA(1-256) 回傳二維陣列,stock長度
    l = len(stock)
    date_wma = [[0] * 256 for _ in range(l - 255)]
    numer = 0
    denomi = 0
    for i in range(1, l - 254):  # i代表每個訓練天數
        for j in range(1, 257):  # j代表訓練天數的MA(1-256)
            for k in range(1, j + 1):  # k計算MA[j]
                numer += float(stock[255 + i - k]) * (j - k + 1)
                denomi += k
            date_wma[i - 1][j - 1] = numer / denomi
            numer = 0
            denomi = 0
    return date_wma, l


def ema(stock):  # 計算訓練期每天的MA(1-256) 回傳二維陣列,stock長度
    l = len(stock)
    date_ema = [[0] * 256 for _ in range(l - 255)]
    numer = 0
    denomi = 0
    ema_tmp = 0
    for i in range(1, l - 254):  # i代表每個訓練天數
        for j in range(1, 257):  # j代表訓練天數的MA(1-256)
            alpha = 2 / (j + 1)
            # for k in range(1,j+1):      #k計算MA[j]
            if (i == 1):
                for e in range(j):
                    numer += float(stock[256 - e])
                date_ema[i - 1][j - 1] = numer / j
                numer = 0
            else:
                date_ema[i - 1][j - 1] = float(stock[254 + i]) * alpha + date_ema[i - 2][j - 1] * (1 - alpha)
    return date_ema, l


def rsi(stock):
    l = len(stock)
    date_rsi = [[0] * 256 for _ in range(l - 255)]
    up = 0
    down = 0
    for i in range(1, l - 254):  # i代表每個訓練天數
        for j in range(1, 257):  # j代表訓練天數
            for k in range(j, 0, -1):  # k計算
                if (float(stock[255 + i - k]) > float(stock[254 + i - k])):  # i = 1 j = 1 k = 1
                    up += (float(stock[255 + i - k]) - float(stock[254 + i - k]))
                elif (float(stock[255 + i - k]) < float(stock[254 + i - k])):
                    down += (float(stock[254 + i - k]) - float(stock[255 + i - k]))
            date_rsi[i - 1][j - 1] = up / (up + down) * 100
            up = 0
            down = 0
    return date_rsi, l

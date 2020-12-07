import yfinance as yf
import sys
import math

class DcaData:
    def __init__(self, total_cost, total_equity, growth_percentage):
        self.total_cost = total_cost
        self.growth_percentage = growth_percentage
        self.total_equity = total_equity

def main():
    action = sys.argv[1]
    ticker_name = sys.argv[2]

    if action == "insight":
        get_insight(ticker_name)
    else:
        cost = sys.argv[3]
        get_dca_simulation(ticker_name, cost)

def get_insight(ticker_name):
    ticker = yf.Ticker(ticker_name)
    data = ticker.history(period="10y", interval="1mo")
    data = data.dropna()
    close = data['Close']
    length_close = len(close)
    growth_5y = 0
    growth_3y = 0
    growth_2y = 0
    growth_1y = 0

    i = 0
    total_loop = 0
    while i < 2:
        pos = i*60
        growth = get_avg_data(close, pos, 60)
        print("Growth 5Y "+str(total_loop)+": "+str(growth)+"%")
        if growth != None:
            growth_5y = growth_5y + growth
            total_loop = total_loop + 1
        i = i+1
        
    growth_5y = round(growth_5y/total_loop,2)

    i = 0
    total_loop = 0
    while i < 3:
        pos = i*36
        growth = get_avg_data(close, pos, 36)
        print("Growth 3Y "+str(total_loop)+": "+str(growth)+"%")
        if growth != None:
            growth_3y = growth_3y + growth
            total_loop = total_loop + 1
        i = i+1
        
    growth_3y = round(growth_3y/total_loop,2)

    i = 0
    total_loop = 0
    while i < 5:
        pos = i*24
        growth = get_avg_data(close, pos, 24)
        print("Growth 2Y "+str(total_loop)+": "+str(growth)+"%")
        if growth != None:
            growth_2y = growth_2y + growth
            total_loop = total_loop + 1
        i = i+1
        
    growth_2y = round(growth_2y/total_loop,2)

    i = 0
    total_loop = 0
    while i < 10:
        pos = i*12
        growth = get_avg_data(close, pos, 12)
        print("Growth 1Y "+str(total_loop)+": "+str(growth)+"%")
        if growth != None:
            growth_1y = growth_1y + growth
            total_loop = total_loop + 1
        i = i+1
        
    growth_1y = round(growth_1y/total_loop,2)

    print("Growth 5Y AVG: "+str(growth_5y)+"%")
    print("Growth 3Y AVG: "+str(growth_3y)+"%")
    print("Growth 2Y AVG: "+str(growth_2y)+"%")
    print("Growth 1Y AVG: "+str(growth_1y)+"%")

def get_avg_data(data, start_range, total):
    length = len(data)
    curr_range = start_range
    actual_total = 0
    last_price = 0
    price = 0
    i = 0
    while actual_total < total and curr_range < length:
        curr_close = data[curr_range]
        price = price + curr_close
        actual_total = actual_total + 1
        last_price = curr_close
        curr_range = curr_range + 1

    if actual_total == 0 or actual_total < total:
        return None

    average_price = price/actual_total
    growth = (last_price - average_price)/last_price * 100
    return round(growth,2)

def get_dca_simulation(ticker_name, cost):
    ticker = yf.Ticker(ticker_name)
    data = ticker.history(period="10y", interval="1mo")
    data = data.dropna()
    close = data['Close']
    length_close = len(close)
    growth_5y = 0
    growth_3y = 0
    growth_2y = 0
    growth_1y = 0

    i = 0
    total_loop = 0
    while i < 2:
        pos = i*60
        dca_data = get_dca_data(close, pos, 60, cost)
        print("Total Cost 5Y "+str(total_loop)+": "+str(dca_data.total_cost))
        print("Total Equity 5Y "+str(total_loop)+": "+str(dca_data.total_equity))
        print("Growth 5Y "+str(total_loop)+": "+str(dca_data.growth_percentage)+"%")
        if dca_data.growth_percentage != None:
            growth_5y = growth_5y + dca_data.growth_percentage
            total_loop = total_loop + 1
        i = i+1
        
    growth_5y = round(growth_5y/total_loop,2)

   

    print("Growth 5Y AVG: "+str(growth_5y)+"%")


def get_dca_data(data, start_range, total, cost):
    length = len(data)
    curr_range = start_range
    actual_total = 0
    last_price = 0
    price = 0
    i = 0
    shares = 0
 
    
    while actual_total < total and curr_range < length:
        curr_close = data[curr_range]
        shares = shares + (float(cost)/float(curr_close))
        price = price + curr_close
        actual_total = actual_total + 1
        last_price = curr_close
        curr_range = curr_range + 1

    if actual_total == 0 or actual_total < total:
        return None

    print(cost)
    print(actual_total)
    total_cost = int(cost) * int(actual_total)
    total_equity = shares * last_price
    print(shares)
    print(total_cost)
    print(total_equity)
    growth = ((float(total_equity) - float(total_cost)) / float(total_equity) * 100)
    dca_data = DcaData(round(total_cost,2), round(total_equity,2), round(growth,2))
    return dca_data




main()
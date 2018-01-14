from datetime import datetime
from datetime import timedelta
import re

class DataCenter():
    def __init__(self, robot):
        self._robot = robot
        self._crypto_history = {"BTC-USD": [], "BCH-USD": [], "LTC-USD": [], "ETH-USD": []}
        self._trade_history  = []
        self._portfolio_history = []
        self._ma_collection = {1:[], 5:[], 10:[], 30:[], 60:[], 120: []}
        #self._time_date_regex = re.compile('\dT\d.\d\w') # ^[0-9]*T[0-9]*\.[0-9]*[^0-9]*?

    def dispatch_message(self, msg):
        msg_type = msg["msg_type"]
        if msg_type == "price_match":
            self.update_crypto_history(msg)
            self.update_moving_averages()

        elif msg_type == "trade":
            self.update_trade_history(msg)
            self.update_portfolio_history()

    def update_trade_history(self, msg):
        #each entry will take the following form:
        #   {"time": None, "side": None, "volume": None, "price": None}

        product_id =   str(msg['product_id'])
        price      = float(msg['price'     ])
        side       =   str(msg['side'      ])
        time       =   str(msg['time'      ])
        sequence   =   int(msg['sequence'  ])

        self._trade_history[msg['product_id']].append({"price": price, "side": side, "time": time, "sequence": sequence})

    def update_portfolio_history(self):
        #each entry will take the following form:
        #   {"time": None,
        #    "total": None,
        #    "BTC-USD": {"amount": None, "value": None},
        #    "LTC-USD": {"amount": None, "value": None},
        #    "ETH-USD": {"amount": None, "value": None},
        #    "BCH-USD": {"amount": None, "value": None}}

        msg = {}

        accounts = self._robot._client.get_accounts()   #retrieve list of accounts
        for account in accounts:
            currency = account["currency"]
            amount = float(account["balance"])
            value = float(self._robot._client.get_product_ticker(currency))
            if currency != "USD":
                msg[currency+"-USD"] = {"amount": amount, "value": value}
            else:
                USD = amount

        msg["total"] = msg["BTC-USD"]["value"] + msg["ETH-USD"]["value"] + msg["LTC-USD"]["value"] + msg["BCH-USD"]["value"] + USD
        msg["time"] = self.to_datetime(msg["time"])

        self._portfolio_history.append(msg)
        
    def update_crypto_history(self, msg):
        #each entry will take the following form:
        #   {"price": None, "side": None, "time": None, "sequence": None}
        #   NOTE: other information may be available in the message. These messages come from the botsocket

        product_id        =   str(msg['product_id'])
        msg['price']      = float(msg['price'     ])
        msg['side']       =   str(msg['side'      ])
        msg['sequence']   =   int(msg['sequence'  ])
        msg['time']       = self.to_datetime(msg['time'])
        
        del msg['product_id']

        #find appropriate spot for message in price history and insert it.
        i = 0
        length = len(self._crypto_history[product_id])
        while length != 0 and msg['sequence'] < self._crypto_history[product_id][length-i-1]["sequence"]:
            i = i + 1
        if i == 0:
            self._crypto_history[product_id].append(msg)
        else:
            self._crypto_history[product_id].insert(length-i, msg)

    def update_moving_averages(self):
        #NOTE: these averages are not calculated correctly. We'll fix this later, but whatever.
    
        #each entry will take the following form:
        #   {"time": None, "simple": None, "weighted": None}
        
        currency = self._robot.currency()
        if len(self._crypto_history[currency]) == 0:
            return
        
        
        for average_size in self._ma_collection.keys():
            last_time = self._crypto_history[currency][-1]["time"]
            current_time_delta = timedelta(minutes=average_size)
            earliest_time = last_time - current_time_delta
            
            print(current_time_delta, " -> ", earliest_time)
            
            if self._crypto_history[currency][0]["time"] > earliest_time:
                continue
            
            index = -1
            weighted_summation = 0
            while self._crypto_history[currency][index]["time"] > earliest_time:
                weighted_summation += self._crypto_history[currency][index]["price"]
                index -= 1
                
            new_weighted_average = weighted_summation / ((-1)*index)
            
            msg = {"time": last_time, "simple": new_weighted_average, "weighted": new_weighted_average}
            
            print("\n\nNEW MOVING AVERAGE: ")
            print(self._ma_collection)
            print()
            
            self._ma_collection[average_size].append(msg) 
        
        
    def to_datetime(self, time):
        # get a datetime object from the string and append that to the message
        new_date_str = time[0:-1]
        new_date_str = new_date_str[:10] + " " + new_date_str[11:-7]
        return datetime.strptime(new_date_str, '%Y-%m-%d %H:%M:%S')



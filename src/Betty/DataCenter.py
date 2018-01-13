class DataCenter():
    def __init__(self, robot):
        self._robot = robot
        self._crypto_history = {"BTC-USD": [], "BCH-USD": [], "LTC-USD": [], "ETH-USD": []}
        self._trade_history  = []
        self._portfolio_history = [] 
        self._sma_collection = {5:[], 10:[], 30:[], 60:[], 120: []}
                               
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
        #msg["time"] =    TODO: decide on time format to use universally
        
        self._portfolio_history.append(msg)
        
    def update_crypto_history(self, msg):
        #each entry will take the following form:
        #   {"price": None, "side": None, "time": None, "sequence": None}
        #   NOTE: other information may be available in the message. These messages come from the botsocket
        
        product_id        =   str(msg['product_id'])
        msg['price']      = float(msg['price'     ])
        msg['side']       =   str(msg['side'      ])
        msg['time']       =   str(msg['time'      ])
        msg['sequence']   =   int(msg['sequence'  ])
        
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
        #each entry will take the following form:
        #   {"time": None, "simple": None, "weighted": None}
        
        pass

    """
    Don't worry about this code for now. It will all change later.
    
    
    #This method just generates a portfolio donut chart using plotly. 
    #Currently, the picture gets put on their website
    def create_portfolio(self):
        prices = {}
        for i in self._robot.client().get_products():
            p_id = i["id"]
            if "USD" in p_id:
                prices[p_id] = float(self.client().get_product_ticker(product_id=p_id)["price"])

        USD, BTC_amount, BCH_amount, ETH_amount, LTC_amount = self.get_balances(all_currencies=True)
        BTC_worth, BCH_worth, ETH_worth, LTC_worth = (BTC_amount * prices["BTC-USD"]), (BCH_amount * prices["BCH-USD"]), (ETH_amount * prices["ETH-USD"]), (LTC_amount * prices["LTC-USD"]),

        net_worth = USD + BTC_worth + BCH_worth + ETH_worth + LTC_worth
        net_worth = round(net_worth, 2)
        title = "GDAX\n${}".format(net_worth)

        plotly.tools.set_credentials_file(username='TradeBotTeam', api_key='SJTSXTDYHHtwLyul8olP')
        fig = {
            "data": [{
                 "values": [USD, BTC_worth, BCH_worth, ETH_worth, LTC_worth],
                 "labels": ["USD", "BTC", "BCH", "ETH", "LTC"],
                 "domain": {"x": [0, 1]},
                 "name"  : "Portfolio",
                 "hoverinfo": "label+percent+name",
                 "hole": .5,
                 "type": "pie"
             }],
             "layout": {
                 "title": "Portfolio",
                 "annotations": [{
                     "font": { "size": 20 },
                     "showarrow": False,
                     "text": title
                 }]
             }
        }

        pie_chart = py.plot(fig, filename="GDAX_porfolio_pie_chart")
        return pie_chart

    #This method uses the client object to print a list of all available crypto prices
    def print_current_prices(self):
        for i in self._robot.client().get_products():
            p_id = i["id"]
            if "USD" in p_id:
                print(p_id + " : " + str(self.client().get_product_ticker(product_id=p_id)["price"]))


    def plot_session(self): 
            
        base_price = self._crypto_history[self._robot.currency()][0]['price']
        base_portfolio_value = self._portfolio_history[0]["total"]
        
        x_axis = []
        portfolio_value_at_trading = self._portfolio_at_trading[:] 
        prices_at_trading = self._prices_at_trading[:]
        
        difference = []
        for i in range(len(self._prices_at_trading)):
            x_axis.append(i)
            portfolio_value_at_trading[i] = ((self._portfolio_at_trading[i]["value"] / base_portfolio_value) -1 ) * 100
            prices_at_trading[i] = ((self._prices_at_trading[i]["value"] / base_price) -1 )* 100
            
            difference.append(portfolio_value_at_trading[i] - prices_at_trading[i])
            
            #if self._portfolio_value_at_trading[i]["state"] != 0:
            #    portfolio_color_at_trading[i] = self._portfolio_value_at_trading[i]["state"] + 1
            #else:
            #    portfolio_color_at_trading[i] = self._portfolio_value_at_trading[i]["state"]
            
            
        trace1 = go.Scatter(
            x = x_axis,
            y = prices_at_trading,
            name = 'product',
            connectgaps = True
        )
        trace2 = go.Scatter(
            x = x_axis,
            y = portfolio_value_at_trading,
            name = 'portfolio',
            connectgaps = True
        )
        trace3 = go.Scatter(
            x = x_axis,
            y = difference,
            name = 'difference',
            connectgaps = True
        )

        data = [trace1, trace2, trace3]

        fig = dict(data=data)
        py.plot(fig, filename=(self.name()+"_results"))
        """
        

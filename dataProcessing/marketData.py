import yfinance as yf

class MarketData(object):
    def __init__(self, data_logger) -> None:
        self.tickerList = {}
        self.data_logger = data_logger
    

    def addTicker(self, ticker):
        # Check if the ticker exists
        try:
            stock = yf.Ticker(ticker)
            # If the ticker exists, add it to the ticker list
            self.tickerList[ticker] = stock.income_stmt
            self.data_logger.addtext("____________________________________________________")
            self.data_logger.addtext(f"Added {ticker} to the ticker list.")

            company_info = stock.info
            # Extracting specific attributes for the summary
            self.data_logger.addtext("Company Name: " +  company_info.get('longName', 'N/A'))
            self.data_logger.addtext("Industry: " +  company_info.get('industry', 'N/A'))
            self.data_logger.addtext("Sector: " +  company_info.get('sector', 'N/A'))
            self.data_logger.addtext("Country: " +  company_info.get('country', 'N/A'))
            self.data_logger.addtext("Company Website: " +  company_info.get('website', 'N/A'))

        except Exception as e:
            self.data_logger.addtext(f"Error adding {ticker} to the ticker list: {e}")
    

    def getIncomeStatement(self, ticker):
        try:
            if ticker in self.tickerList:
                return self.tickerList[ticker].keys()
            else:
                raise ValueError(f"{ticker} not found in the ticker list.")
        except Exception as e:
            print(f"Error retrieving income statement for {ticker}: {e}")
            return None
    
    def getVars(self, ticker, dep, ind):
        if ticker in self.tickerList:
            if ind in self.tickerList[ticker] and dep in self.tickerList[ticker]:
                return {"X": self.tickerList[ticker][ind], "Y": self.tickerList[ticker][dep]}
        self.data_logger.addtext("Error getting ticker variables")
    
    def getTickerRecommendations(self):
        recommendations = {}
        try:
            with open("./assets/tickers.txt", "r") as file:
                tickers = file.readlines()
                for ticker in tickers:
                    ticker = ticker.strip()
                    self.addTicker(ticker)
                    if ticker in self.tickerList:
                        industry = self.tickerList[ticker].info.get('industry')
                        if industry:
                            if industry not in recommendations:
                                recommendations[industry] = []
                            recommendations[industry].append({'ticker': ticker, 'name': self.tickerList[ticker].info['longName']})
                    else:
                        print(f"Ticker {ticker} not found in the ticker list.")
        except Exception as e:
            print(f"Error reading or processing tickers: {e}")
        return recommendations

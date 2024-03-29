import yfinance as yf
import pandas as pd


class MarketData(object):
    def __init__(self, data_logger) -> None:
        self.tickerList = {}
        self.data_logger = data_logger

        self.plotList = {"X" : [], "Y": []}
    

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
            self.data_logger.addtext("____________________________________________________")

        except Exception as e:
            self.data_logger.addtext(f"Error adding {ticker} to the ticker list: {e}")
    

    def getIncomeStatement(self, ticker):
        try:
            if ticker in self.tickerList:
                # Assuming self.tickerList[ticker] contains your DataFrame
                df = self.tickerList[ticker]
                # Get all the names of the rows (index)
                row_names = df.index.tolist()
                return row_names
            else:
                raise ValueError(f"{ticker} not found in the ticker list.")
        except Exception as e:
            print(f"Error retrieving income statement for {ticker}: {e}")
            return None
    
    def getVars(self, ticker, dep, ind):
        if ticker in self.tickerList:
            # Assuming self.tickerList[ticker] contains your DataFrame
            data = self.tickerList[ticker]
            # Extracting Total Revenue, Operating Revenue, and the years
            X_vals = data.loc[ind].values
            Y_vals = data.loc[dep].values
            years = data.columns.tolist()
            years = [timestamp.year for timestamp in years]
            ratio = [a / b for a, b in zip(Y_vals, X_vals)]

            
            

            self.data_logger.addtext("Here is the data for " + ticker + " for ...")
            self.data_logger.addtext(dep + " : " + str(Y_vals))
            self.data_logger.addtext(ind + " : " + str(X_vals))
            self.data_logger.addtext("Creates ratio of : " + str(ratio))
            self.data_logger.addtext("Across Years : " + str(years))

            # add to list
            self.plotList["X"] += years
            self.plotList["Y"] += ratio

            return {"years": years, "ratio": ratio}
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


    def removeTicker(self, ticker):
        if ticker in self.tickerList:
            del self.tickerList[ticker]
            self.data_logger.addtext(f"Removed {ticker} from the ticker list.")
        else:
            self.data_logger.addtext(f"{ticker} not found in the ticker list.")


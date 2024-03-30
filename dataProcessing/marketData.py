import yfinance as yf
import pandas as pd
import numpy as np

class MarketData(object):
    def __init__(self, data_logger) -> None:
        self.tickerList = {}
        self.data_logger = data_logger
        self.plotList = {}
    

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

            years = np.array(years)
            ratio = np.array(ratio)
            X_vals = np.array(X_vals)
            Y_vals = np.array(Y_vals)
            # Convert X_vals, Y_vals, and years to numeric types
            X_vals = pd.to_numeric(X_vals, errors='coerce')
            Y_vals = pd.to_numeric(Y_vals, errors='coerce')
            years = pd.to_numeric(years, errors='coerce')
           
            # Find indices where either years or ratio has NaN value
            nan_indices = np.isnan(years) | np.isnan(X_vals) | np.isnan(Y_vals)

            self.data_logger.addtext("The following indices have NaN values: " + str(nan_indices))
            self.data_logger.addtext("Removed Succesfully.")

            # Remove rows where either years or ratio has NaN value
            years = years[~nan_indices].tolist()
            ratio = ratio[~nan_indices].tolist()
            X_vals = X_vals[~nan_indices].tolist()
            Y_vals = Y_vals[~nan_indices].tolist()


            self.data_logger.addtext("Here is the data for " + ticker + " for ...")
            self.data_logger.addtext(dep + " : " + str(Y_vals))
            self.data_logger.addtext(ind + " : " + str(X_vals))
            self.data_logger.addtext("Creates ratio of : " + str(ratio))
            self.data_logger.addtext("Across Years : " + str(years))

            # add to list
            self.plotList[ticker] = {"X" :[], "Y": [], "ratio": [], "years": []}
            self.plotList[ticker]["X"] += X_vals
            self.plotList[ticker]["Y"] += Y_vals
            self.plotList[ticker]["ratio"] += ratio
            self.plotList[ticker]["years"] += years

            return self.plotList[ticker]
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
            if ticker in self.plotList:
                del self.plotList[ticker]
        else:
            self.data_logger.addtext(f"{ticker} not found in the ticker list.")
    

    def getPlotList(self, var1, var2):
        output = {var1 :[], var2: []}
        for i in self.plotList:
            output[var1] += self.plotList[i][var1]
            output[var2] += self.plotList[i][var2]
        
        return output





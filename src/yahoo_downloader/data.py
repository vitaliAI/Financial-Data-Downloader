""""
Weaknesses:

- Not reliable (in the past)
- No (useful) Data for Bonds & Commodities
- No high-frequency real-time data
- No Bid/Ask
"""

import pandas as pd
import yfinance as yf


def downloand_ticker_price_data(ticker: str = 'FB', start=None, end=None, actions=False) -> pd.DataFrame:
    """Download yahoo tickers
        :Parameters:
            tickers : str, list
                List of tickers to download
            start: str
                Download start date string (YYYY-MM-DD) or _datetime.
                Default is 1900-01-01
            end: str
                Download end date string (YYYY-MM-DD) or _datetime.
                Default is now
            actions: bool
                Download dividend + stock splits data. Default is False
    """
    df = yf.download(ticker, start=start, end=end, actions=actions)
    return df


def downloand_ticker_fundamental_data(ticker: str = 'FB', start=None, end=None, actions=True) -> pd.DataFrame:
    """Download yahoo tickers
        :Parameters:
            tickers : str, list
                List of tickers to download
            start: str
                Download start date string (YYYY-MM-DD) or _datetime.
                Default is 1900-01-01
            end: str
                Download end date string (YYYY-MM-DD) or _datetime.
                Default is now
            actions: bool
                Download dividend + stock splits data. Default is False
    """
    ticker_inst = yf.Ticker(ticker=ticker)
    df = ticker_inst.history(start=start, end=end, actions=actions)
    return ticker_inst.option_chain()[0].T


if __name__ == '__main__':
    print(downloand_ticker_fundamental_data())

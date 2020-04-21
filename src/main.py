import argparse
import time
import os

import pandas as pd

from pytrends.request import TrendReq


class GoogleTrends(object):

    def __init__(self, DATA_PATH, SAVING_PATH, GEO, TIMEFRAME, PYTREND):
        self.data_path = DATA_PATH
        self.saving_path = SAVING_PATH
        self.geo = GEO
        self.timeframe = TIMEFRAME
        self.pytrend = PYTREND

    def get_ticker_list(self, TICKER_PATH):

        ticker = pd.read_excel(TICKER_PATH)

        return ticker.ticker.tolist()

    def get_trends(self):

        ticker_list = self.get_ticker_list(self.data_path)
        limit = 50
        df = pd.DataFrame({'date': [], 'variable': [], 'value': []})

        for count, ticker in enumerate(ticker_list):
            if count == limit:
                time.sleep(90)
                limit = limit + 50
                df.to_csv(self.saving_path,
                          index=False)
                continue
            else:
                self.pytrend.build_payload(
                    kw_list=[ticker], geo=self.geo, timeframe=self.timeframe)

                trends_df = self.pytrend.interest_over_time().reset_index()

                try:
                    melted_df = pd.melt(trends_df, id_vars=[
                        'date'], value_vars=[ticker])
                except KeyError:

                    os.write(1, ticker.encode())
                df = df.append(melted_df, ignore_index=True)

        return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data source and saving paths')
    parser.add_argument('data_path', type=str, help='Input dir stock ticker')
    parser.add_argument('saving_path', type=str, help='Saving path', default=None)
    parser.add_argument('-g', '--geo', type=str, help='Geo eg.: "US"')
    parser.add_argument('-tf', '--timeframe', type=str, help='Timeframe default: today 5-y', default=None)
    args = parser.parse_args()

    GoogleTrends(args.data_path, args.saving_path, args.geo, args.timeframe, TrendReq())
    os.write(1,'finished'.encode('UTF8'))

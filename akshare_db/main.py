import asyncio
import sys, os
import argparse
import datetime

from akshare_db.client import DBClient
from akshare_db.tables.index_table import update_index_info, update_all_cons_sina
from akshare_db.tables.symbol_table import update_symbol_table
from akshare_db.tables.history_table import update_all_history
from akshare_db.tables.info_table import update_all_stock_info

from akshare_db.tables.financial_table import update_all_financial_indicator_db
from akshare_db.tables.dividend_table import update_all_dividend
from akshare_db.tables.allotment_table import update_all_allotment
from akshare_db.tables.stockadd_table import update_all_stockadd
from akshare_db.tables.revenue_table import update_all_revenue
from akshare_db.tables.restricted_table import update_all_restricted_release


def parse_args():
    parser = argparse.ArgumentParser(description="""Download stock data
        --all
        --index, -i       # 股票指数, 000300
        --cons, -c        # 指数的成分股
        --symbol, -s      # 个股列表
        --info, -n        # 个股信息
        --history, -h     # 个股历史数据
        --allotment, -l   # 个股配股数据
        --financial, -f   # 个股财经数据
        --dividend, -d    # 个股分红数据
        --restricted, -r  # 个股限售
        --revenue, -v     # 个股财报                           
        --stockadd, -a    # 个股定增
    """)
    parser.add_argument("--basic", action="store_true", \
        help="update basic tables: index, cons, symbol, info")
    parser.add_argument("--index", "-i", \
        action="store_true", help="update list of stock indices")
    parser.add_argument("--cons", "-c", \
        action="store_true", help="update constituent stock tickers of index")
    parser.add_argument("--symbol", "-s", \
        action="store_true", help="update list of stock tickers")
    parser.add_argument("--info", "-n", \
        action="store_true", help="update stock information")
    group = parser.add_argument_group("Download history data")
    group.add_argument("--history", "-y", \
        action="store_true", help="update history data of stocks")
    group.add_argument("--freq", choices=["daily", "weekly", "monthly"], 
        default="daily", help="frequency of history data")
    group.add_argument("--fq", choices=["qfq", "hfq"], 
        default="hfq", help="adjust method")
    group.add_argument("--start", type=str, 
        default="19900101", help="start data: yyyymmdd")
    group.add_argument("--end", type=str, 
        default=None, help="end data: yyyymmdd")
    parser.add_argument("--allotment", "-l", \
        action="store_true", help="update allotment data of stocks")    
    parser.add_argument("--financial", "-f", \
        action="store_true", help="update financial data of stocks")
    parser.add_argument("--dividend", "-d", \
        action="store_true", help="update dividend data of stocks")
    parser.add_argument("--restricted", "-r", \
        action="store_true", help="update restricted data of stocks")
    parser.add_argument("--revenue", "-v", \
        action="store_true", help="update revenue data of stocks")
    parser.add_argument("--stockadd", "-a", \
        action="store_true", help="update stockadd data of stocks")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    with DBClient() as db:
        loop = asyncio.get_event_loop()
        if args.basic or args.index:
            update_index_info(db)
            print("Updated list of stock indices")
        
        if args.basic or args.cons:
            loop.run_until_complete(update_all_cons_sina(db))
            print("Updated constituent stocks of stock indices")
        
        if args.basic or args.symbol:
            update_symbol_table(db)
            print("Updated list of stock tickers")
        
        if args.basic or args.info:
            loop.run_until_complete(update_all_stock_info(db))
            print("Updated stock information")
    
        if args.history:
            if args.end is None:
                args.end = datetime.datetime.today().strftime("%Y%m%d")
            loop.run_until_complete(
                update_all_history(db, period=args.freq, start_date=args.start, \
                end_date=args.end, adjust=args.fq)
            )
        
        if args.financial:
            loop.run_until_complete(update_all_financial_indicator_db(db))
    
        if args.dividend:
            loop.run_until_complete(update_all_dividend(db))

        if args.allotment:
            loop.run_until_complete(update_all_allotment(db))

        if args.restricted:
            loop.run_until_complete(update_all_restricted_release(db))

        if args.stockadd:
            loop.run_until_complete(update_all_stockadd(db))

        if args.revenue:
            loop.run_until_complete(update_all_revenue(db))

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(
        #     update_all_history(period="daily", start_date="19900101", \
        #         end_date="20230905", adjust="qfq")
        # )

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(
        #     update_all_history(period="weekly", start_date="19900101", \
        #         end_date="20230905", adjust="qfq")
        # )

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(
        #     update_all_history(period="monthly", start_date="19900101", \
        #         end_date="20230905", adjust="qfq")
        # )
    

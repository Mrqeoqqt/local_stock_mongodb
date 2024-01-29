import asyncio
import functools
import akshare as ak
from typing import List
from akshare_db.client import BaseField, BaseCollection
from akshare_db.client import DBClient
from akshare_db.tables.symbol_table import get_symbol_list


class HistoryField(BaseField):
    code: str
    header: List
    value: List[List]
    
    class Config:
        schema_extra = {
            "example": {
                "code": "000001",
                "header": ['日期', '开盘', '收盘', '最高', '最低', \
                        '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'],
                "value": [['1991-04-03', '-1.25', '-1.25', '-1.25', '-1.25',
                            '1', '5000.0', '0.0', '4.58', '0.06', '0.0']]
            }
        }


class HistoryTable(BaseCollection):
    def __init__(self, db, name="history", freq="daily"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name+f"_{freq}"]
        self.fieldtype = HistoryField


async def update_history(db, symbol, period, \
                      start_date, end_date, adjust):
    """_summary_

    Parameters
    ----------
    symbol : str
        stock symbol
    period : str
        'daily', 'weekly', 'monthly'
    start_date : str
        YYYYmmdd
    end_date : str
        YYYYmmdd
    adjust : str
        "qfq", "hfq"
    """
    try:
        hist_df = ak.stock_zh_a_hist(symbol, period, \
                    start_date, end_date, adjust)
        table = HistoryTable(db.db, freq=period)
        try:
            entry = table.get(code=symbol)
            table.update(entry.dict(), code=symbol, header=hist_df.columns.tolist(), \
                        value=hist_df.astype(str).values.tolist())
        except:
            field = HistoryField(code=symbol, header=hist_df.columns.tolist(), \
                        value=hist_df.astype(str).values.tolist())
            table.create(field)
    except Exception as e:
        print(f"Fetching error {e}: {symbol}")


async def update_all_history(db, period, \
                start_date, end_date, adjust):
    tasks = []
    codelist = await get_symbol_list(db)
    func = functools.partial(update_history, db=db, period=period, \
                start_date=start_date, end_date=end_date, adjust=adjust)
    for symbol in codelist:
        tasks.append(
            func(symbol=symbol)
        )
    await asyncio.gather(*tasks)
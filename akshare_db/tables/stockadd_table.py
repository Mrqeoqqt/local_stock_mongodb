import asyncio
import akshare as ak
from typing import List
from akshare_db.client import DBClient
from akshare_db.client import BaseField, BaseCollection
from akshare_db.tables.symbol_table import get_symbol_list


class StockAddField(BaseField):
    code: str
    header: List
    value: List[List]

    class Config:
        schema_extra = {
            "example": {
                "code": "000001",
                "header": ["日期", "发行方式", "发行价格", "实际公司募集资金总额", "发行费用总额", ],
                "value": [
                    ["2015-05-20", "定向配售、网下询价配售", "16.70元", "1,000,000.00万元", ]
                ]
            }
        }


class StockAddTable(BaseCollection):
    def __init__(self, db, name="stock_add"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = StockAddField


async def update_stockadd(db, symbol):
    try:
        df = ak.stock_add_stock(stock=symbol) # 增发
        df["日期"] = df.index.values.tolist()
        table = StockAddTable(db.db)
        try:
            entry = table.get(code=symbol)
            table.update(entry.dict(), code=symbol, header=df.columns.tolist(), \
                        value=df.astype(str).values.tolist())
        except:
            field = StockAddField(code=symbol, header=df.columns.tolist(), \
                        value=df.astype(str).values.tolist())
            table.create(field)
    except Exception as e:
        print(f"Fetching error {e}: {symbol}")


async def update_all_stockadd(db, ):
    tasks = []
    codelist = await get_symbol_list(db)
    for symbol in codelist:
        tasks.append(
            update_stockadd(db, symbol)
        )
    await asyncio.gather(*tasks)
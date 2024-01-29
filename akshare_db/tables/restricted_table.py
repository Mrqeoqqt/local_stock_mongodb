import asyncio
import akshare as ak
from typing import List
from akshare_db.client import DBClient
from akshare_db.client import BaseField, BaseCollection
from akshare_db.tables.symbol_table import get_symbol_list


class RestrictedField(BaseField):
    code: str
    header: List
    value: List[List]

    class Config:
        schema_extra = {
            "example": {
                "code": "000001",
                "header": ["代码", "名称", "解禁日期", "解禁数量", ],
                "value": [
                    ["1", "平安银行", "2018-05-21", "25224.8", ],
                ]
            }
        }


class RestrictedTable(BaseCollection):
    def __init__(self, db, name="restricted"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = RestrictedField


async def update_restricted_release(db, symbol):
    try:
        df = ak.stock_restricted_release_queue_sina(symbol=symbol) # 限售解禁-新浪
        table = RestrictedTable(db.db)
        try:
            entry = table.get(code=symbol)
            table.update(entry.dict(), code=symbol, header=df.columns.tolist(), \
                        value=df.astype(str).values.tolist())
        except:
            field = RestrictedField(code=symbol, header=df.columns.tolist(), \
                        value=df.astype(str).values.tolist())
            table.create(field)
    except Exception as e:
        print(f"Fetching error {e}: {symbol}")


async def update_all_restricted_release(db, ):
    tasks = []
    codelist = await get_symbol_list(db)
    for symbol in codelist:
        tasks.append(
            update_restricted_release(db, symbol)
        )
    await asyncio.gather(*tasks)
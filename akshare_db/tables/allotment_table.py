import asyncio
import akshare as ak
from typing import List
from akshare_db.client import DBClient
from akshare_db.client import BaseField, BaseCollection
from akshare_db.tables.symbol_table import get_symbol_list


class AllotmentField(BaseField):
    code: str
    header: List
    value: List[List]

    class Config:
        schema_extra = {
            "example": {
                "code": "000001",
                "header": ["记录标识", "证券简称", "停牌起始日", "上市公告日期", ],
                "value": [
                    ["26002185", "平安银行", "NaT", "NaT", ]
                ]
            }
        }


class AllotmentTable(BaseCollection):
    def __init__(self, db, name="allotment"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = AllotmentField


async def update_allotment(db, symbol):
    try:
        df = ak.stock_allotment_cninfo(symbol=symbol) # 配股
        table = AllotmentTable(db.db)
        try:
            entry = table.get(code=symbol)
            table.update(entry.dict(), code=symbol, header=df.columns.tolist(), \
                        value=df.astype(str).values.tolist())
        except:
            field = AllotmentField(code=symbol, header=df.columns.tolist(), \
                        value=df.astype(str).values.tolist())
            table.create(field)
    except Exception as e:
        print(f"Fetching error {e}: {symbol}")


async def update_all_allotment(db):
    tasks = []
    codelist = await get_symbol_list(db)
    for symbol in codelist:
        tasks.append(
            update_allotment(db, symbol)
        )
    await asyncio.gather(*tasks)
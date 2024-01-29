import asyncio
import akshare as ak
from typing import List
from akshare_db.client import DBClient
from akshare_db.client import BaseField, BaseCollection
from akshare_db.tables.symbol_table import get_symbol_list


class RevenueField(BaseField):
    code: str
    header: List
    value: List[List]

    class Config:
        schema_extra = {
            "example": {
                "code": "000001",
                "header": ["报告期", "分类方向", "分类", "营业收入", ],
                "value": [
                    ["2023中期", "按行业分", "零售金融业务", "526.31亿", ],
                ]
            }
        }


class RevenueTable(BaseCollection):
    def __init__(self, db, name="revenue"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = RevenueField


async def update_revenue(db, symbol):
    try:
        df = ak.stock_zygc_ym(symbol) # 主营
        table = RevenueTable(db.db)
        try:
            entry = table.get(code=symbol)
            table.update(entry.dict(), code=symbol, header=df.columns.tolist(), \
                        value=df.astype(str).values.tolist())
        except:
            field = RevenueField(code=symbol, header=df.columns.tolist(), \
                        value=df.astype(str).values.tolist())
            table.create(field)
    except Exception as e:
        print(f"Fetching error {e}: {symbol}")


async def update_all_revenue(db, ):
    tasks = []
    codelist = await get_symbol_list(db)
    for symbol in codelist:
        tasks.append(
            update_revenue(db, symbol)
        )
    await asyncio.gather(*tasks)



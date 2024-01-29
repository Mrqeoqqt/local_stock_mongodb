import asyncio
import akshare as ak
from typing import List
from akshare_db.client import DBClient
from akshare_db.client import BaseField, BaseCollection
from akshare_db.tables.symbol_table import get_symbol_list


class DividendField(BaseField):
    code: str
    header: List
    value: List[List]

    class Config:
        schema_extra = {
            "example": {
                "code": "000001",
                "header": ["报告期", "业绩披露日期", "现金分红-现金分红比例", ],
                "value": [
                    ["2022-12-31", "2023-03-09", "2.850", ], 
                    ["2021-12-31", "2022-03-10", "2.280", ],
                ]
            }
        }


class DividendTable(BaseCollection):
    def __init__(self, db, name="dividend"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = DividendField


async def update_dividend(db, symbol):
    try:
        fhps_df = ak.stock_fhps_detail_em(symbol) # 分红配送
        table =  DividendTable(db.db)
        try:
            entry = table.get(code=symbol)
            table.update(entry.dict(), code=symbol, header=fhps_df.columns.tolist(),\
                        value=fhps_df.astype(str).values.tolist())
        except:
            field = DividendField(code=symbol, header=fhps_df.columns.tolist(),\
                        value=fhps_df.astype(str).values.tolist())
            table.create(field)
    except Exception as e:
        print(f"Fetching error {e}: {symbol}")


async def update_all_dividend(db):
    tasks = []
    codelist = await get_symbol_list(db)
    for symbol in codelist:
        tasks.append(
            update_dividend(db, symbol)
        )
    await asyncio.gather(*tasks)
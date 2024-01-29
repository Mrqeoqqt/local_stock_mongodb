import asyncio
import akshare as ak
from typing import List
from akshare_db.client import DBClient 
from akshare_db.client import BaseField, BaseCollection
from akshare_db.tables.symbol_table import get_symbol_list

class IndicatorField(BaseField):
    code: str
    header: List
    value: List[List]

    class Config:
        schema_extra = {
            "example": {
                "code": "000001",
                "header": ["日期", "摊薄每股收益(元)", "加权每股收益(元)", ],
                "value": [
                    ["2023-06-30", "1.3082", "1.2", ],
                    ["2023-03-31", "0.7525", "0.65", ],
                ]
            }
        }


class IndicatorTable(BaseCollection):
    def __init__(self, db, name="financial_indicator"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = IndicatorField


async def update_financial_indicator_info(db, symbol):
    try:
        ind_df = ak.stock_financial_analysis_indicator(symbol=symbol)  # 财务指标
        table = IndicatorTable(db.db)
        try:
            entry = table.get(code=symbol)
            table.update(entry.dict(), code=symbol, header=ind_df.columns.tolist(), \
                        value=ind_df.astype(str).values.tolist())
        except:
            field = IndicatorField(code=symbol, header=ind_df.columns.tolist(), \
                        value=ind_df.astype(str).values.tolist())
            table.create(field)
    except Exception as e:
        print(f"Fetching error {e}: {symbol}")


async def update_all_financial_indicator_db(db, ):
    tasks = []
    codelist = await get_symbol_list(db)
    for symbol in codelist:
        tasks.append(
            update_financial_indicator_info(db, symbol)
        )
    await asyncio.gather(*tasks)
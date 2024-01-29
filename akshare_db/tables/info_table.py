import asyncio
import akshare as ak
from typing import Dict
from akshare_db.client import DBClient
from akshare_db.client import BaseField, BaseCollection
from akshare_db.tables.symbol_table import get_symbol_list

class InfoField(BaseField):
    code: str
    info: Dict[str, str]

    class Config:
        schema_extra = {
            "example": {
                "code": "000001",
                "info": {
                    '总市值': "219674994001.36002",
                    '流通市值': "219670791474.0",
                    '行业': '银行',
                    '上市时间': "19910403",
                    '股票代码': '000001',
                    '股票简称': '平安银行',
                    '总股本': "19405918198.0",
                    '流通股': "19405546950.0"
                }
            }
        }


class InfoTable(BaseCollection):
    def __init__(self, db, name="stock_info"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = InfoField



async def update_stock_info(db, symbol):
    info_df = None
    try:
        info_df = ak.stock_individual_info_em(symbol=symbol)
        info_dct = dict(zip(info_df['item'].values.tolist(), info_df['value'].values.tolist()))
        table = InfoTable(db.db)
        try:
            entry = table.get(code=symbol)
            table.update(entry.dict(), code=symbol, info=info_dct)
        except:
            field = InfoField(code=symbol, info=info_dct)
            table.create(field)
    except Exception as e:
        print(f"Fetching error {e}: {symbol}")
    return info_df


async def update_all_stock_info(db, ):
    """
    Update Collection: stock_info
    """
    tasks = []
    codelist = await get_symbol_list(db)
    for symbol in codelist:
        tasks.append(
            update_stock_info(db, symbol)
        )
    await asyncio.gather(*tasks)


async def get_stock_info(db, symbol):
    table = InfoTable(db.db)
    entry = table.get(code=symbol)
    return entry
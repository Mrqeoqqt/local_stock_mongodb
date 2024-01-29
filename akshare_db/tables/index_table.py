import asyncio
import akshare as ak
from typing import List
from akshare_db.client import DBClient
from akshare_db.client import BaseField, BaseCollection

class IndexInfoField(BaseField):
    code: str
    name: str
    publish_date: str

    class Config:
        schema_extra = {
            "example": {
                "code": "000300",
                "value": "沪深300",
                "publish_date": "2005-04-08"
            }
        }

class IndexInfoTable(BaseCollection):
    def __init__(self, db, name="index_info"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = IndexInfoField


class IndexField(BaseField):
    code: str
    value: List

    class Config:
        schema_extra = {
            "example": {
                "code": "000300",
                "value": ["000983", "600732", "601872", ]
            }
        }

class IndexTable(BaseCollection):
    def __init__(self, db, name="index_constituents"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = IndexField


def update_index_info(db):
    """
    Update Collection: index
    """
    df = None
    try:
        df = ak.index_stock_info()
        df = df.astype(str)
    except Exception as e:
        print(e)
        return

    updated = 0
    created = 0
    table = IndexInfoTable(db.db)
    for idx, row in df.iterrows():
        try:
            entry = table.get(code=row["index_code"])
            table.update(entry.dict(), 
                        code=row["index_code"], name=row["display_name"], \
                        publish_date=row["publish_date"])
            updated += 1
        except Exception as e:
            field = IndexInfoField(code=row["index_code"], \
                        name=row["display_name"], publish_date=row["publish_date"])
            table.create(field)
            created += 1
    lst = table.list()
    print(f"Number of index available: {df.shape[0]}")
    print(f"Number of index created/updated: {created}/{updated}")
    print(f"Number of index in database: {len(lst)}")


async def get_indexlist(db, ):
    """
    Returns
    -------
    codelist : lst
        index
    """
    codelist = []
    table = IndexInfoTable(db.db)
    lst = table.list()
    codelist = [item.code for item in lst]
    return codelist


async def update_cons_sina(db, symbol):
    """Return constituent stocks, such as 000300
    Returns
    -------
    lst : str
        list that contains constituent stock
    """
    try:
        index_stock_cons_df = ak.index_stock_cons(symbol)
        lst = index_stock_cons_df['品种代码'].unique().tolist()
        lst = sorted([i.strip() for i in lst])
        table = IndexTable(db.db)
        try:
            entry = table.get(code=symbol)
            table.update(entry.dict(), code=symbol, value=lst)
        except:
            field = IndexField(code=symbol, value=lst)
            table.create(field)
    except Exception as e:
        print(f"Fetching error {e}: {symbol}")


async def update_all_cons_sina(db, ):
    tasks = []
    codelist = await get_indexlist(db)
    for symbol in codelist:
        tasks.append(
            update_cons_sina(db, symbol)
        )
    await asyncio.gather(*tasks)


async def get_cons(db, symbol):
    """
    Returns
    -------
    codelist : list
        constituent stock tickers of a given index
    """
    table = IndexTable(db.db)
    entry = table.get(code=symbol)
    return entry
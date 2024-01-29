import akshare as ak
from akshare_db.client import DBClient
from akshare_db.client import BaseField, BaseCollection


class SymbolField(BaseField):
    code: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "code": "000001",
                "name": "平安银行"
            }
        }


class SymbolTable(BaseCollection):
    def __init__(self, db, name="symbol"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = SymbolField



def update_symbol_table(db, ):
    """
    Update Collection: symbol
    """
    df = None
    try:
        df = ak.stock_info_a_code_name()
    except Exception as e:
        print(e)
        return

    updated = 0
    created = 0
    table = SymbolTable(db.db)
    for idx, row in df.iterrows():
        code = row["code"]
        name = row["name"]
        try:
            entry = table.get(code=code)
            table.update(entry.dict(), code=code, name=name)
            updated += 1
        except Exception as e:
            field = SymbolField(code=row["code"], name=row["name"])
            table.create(field)
            created += 1
    lst = table.list()
    print(f"Number of stocks available: {df.shape[0]}")
    print(f"Number of stocks created/updated: {created}/{updated}")
    print(f"Number of stocks in database: {len(lst)}")


async def get_symbol_list(db, ):
    codelist = []
    table = SymbolTable(db.db)
    lst = table.list()
    codelist = [item.code for item in lst]
    return codelist
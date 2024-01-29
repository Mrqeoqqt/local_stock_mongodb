"""
table records
========================
TABLE NAME | COMMENT
========================
SYMBOL     |             # 股票代码, 股票名称
------------------------
STOCK INFO |             # 股票信息
------------------------
DIVIDEND   |             # 分红配送 
------------------------
REPURCHASE EM|           # 回购信息
------------------------
INNER TRADE|             # 内部交易
------------------------
PLEDGE     |             # 股权质押
------------------------
LAWSUIT    |             # 公司诉讼
------------------------
GUARANTEE  |             # 公司担保
------------------------
GOODWILL   |             # 商誉
------------------------
MANAGEMENT HOLD|         # 高管持股
------------------------
INDUSTRY SW|             # 行业分类
========================
"""
from akshare_db.client import BaseField, BaseCollection


class MetaField(BaseField):
    tablename: str
    comment: str

    class Config:
        schema_extra = {
            "example": {
                "tablename": "symbol",
                "comment": "股票代码/名称"
            }
        }


class MetaTable(BaseCollection):
    def __init__(self, db, name="meta"):
        super().__init__(db, name)
        self.name = name
        self.collection = db[self.name]
        self.fieldtype = MetaField

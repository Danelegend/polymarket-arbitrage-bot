from pydantic import BaseModel

class AssetIdentifier(BaseModel):
    market_name: str
    market_outcome: str
    asset_id: int

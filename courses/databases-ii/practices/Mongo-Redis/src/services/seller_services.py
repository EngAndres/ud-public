""""""

from typing import Optional, List
from datetime import datetime, timezone
from bson import ObjectId
from ..repositories import MongoDB
from ..models import Seller

class SellerServices:
    """"""

    def __init__(self):
        self.collection = MongoDB.get_database()["sellers"]

    async def create_seller(self, seller_data: Seller) -> bool:
        """
        
        Args:
            seller_data (Seller):
        """
        success = True
        
        # check email as unique
        if self.collection.find_one({"email": seller_data.email}):
            success = False
            raise ValueError("El email ya existe.")
        
        # save
        seller_dict = seller_data.model_dump()
        self.collection.insert_one(seller_dict)

        return success
    
    async def get_seller(self, seller_id: str) -> Optional[Seller]:
        try:
            seller = self.collection.find_one({"_id": ObjectId(seller_id)})
            if seller:
                seller['id'] = str(seller['_id'])
                return Seller(**seller)
            else:
                return None
        except Exception as e:
            with open('error_services_log.txt', 'a') as f:
                error = f"{datetime.now(timezone.utc)}. Fallo buscando \
                    al vendedor con id {seller_id}. \n{e}."
                f.write(error)

    async def get_sellers(self, skip_parameter: int = 0, 
                          limit_parameter: int = 10) -> List[Seller]:
        sellers = list( self.collection.find().skip(skip_parameter)
                       .limit(limit_parameter) )
        for seller in sellers:
            seller['id'] = str( seller['_id'] )
        
        return [Seller(**seller) for seller in sellers]
    
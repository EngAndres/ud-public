""""""

from typing import List, Optional
from bson import ObjectId
from ..repositories import MongoDB
from ..models import ProductIn, ProductOut

class ProductServices:
    """"""

    def __init__(self):
        self.products_collection = MongoDB.get_database()["products"]
        self.sellers_collection = MongoDB.get_database()["sellers"]

    async def create_product(self, product_data: ProductIn) -> ProductOut:
        # verify seller
        seller = self.sellers_collection.find_one(
                    {'_id' : ObjectId(product_data.seller_code)})
        if not seller:
            raise ValueError("El vendedor está incorrecto.")
        
        # save
        product_dict = product_data.model_dump()
        result = self.products_collection.insert_one(product_dict)
        result['seller_name'] = seller.name
        return ProductOut(**result)
    
    async def get_products_by_seller(self, seller_id: str) -> List[ProductOut]:
        products = list(self.products_collection.
                        find({'seller_code': seller_id}))

        seller = self.sellers_collection.find_one(
                    {'_id' : ObjectId(seller_id)})
        
        for product in products:
            product['seller_name'] = seller.name

        return [ProductOut(**product) for product in products]
        
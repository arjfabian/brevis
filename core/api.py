from ninja import NinjaAPI
from brevis.api import brevis_router

api = NinjaAPI()
api.add_router('', brevis_router)
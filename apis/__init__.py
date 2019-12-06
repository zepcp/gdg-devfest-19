from flask_restplus import Api
from .zomic import api as zomic_api

api = Api(
    version="1.0",
    title="Zomic API",
    description="Zomic API"
)

api.add_namespace(zomic_api, "/zomic")

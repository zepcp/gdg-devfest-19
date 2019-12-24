from flask_restplus import Api
from .write import api as write
from .read import api as read
from .audit import api as transparency
from .news import api as newsletter

api = Api(
    version="1.0",
    title="Zomic APIs",
    description="Get Involved On Your Community"
)

api.add_namespace(write, "/write")
api.add_namespace(read, "/read")
api.add_namespace(transparency, "/audit")
api.add_namespace(newsletter, "/news")

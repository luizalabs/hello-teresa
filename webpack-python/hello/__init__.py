import os

import aiohttp_jinja2
import jinja2
from aiohttp import web


def here(*dirs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *dirs)


@aiohttp_jinja2.template('index.html')
async def home(request):
    return {}


app = web.Application()
app.router.add_route('GET', '/', home)
app.router.add_static('/static', here('static'))

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(here('templates'))
)

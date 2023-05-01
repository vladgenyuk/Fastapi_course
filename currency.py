from fastapi import FastAPI
from ws_config.router import router as router_ws
from ws_config.page_router import router as router_page

app = FastAPI()

app.include_router(router_ws)
app.include_router(router_page)


@app.get('/')
async def exchange_rates():
    return {'data': 1}

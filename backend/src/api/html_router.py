from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services import PricesService, allow_get_items


router = APIRouter()

templates = Jinja2Templates(directory="backend/src/templates")


@router.get("/index", response_class=HTMLResponse)
def read_item(
    request: Request,
    service_prices: PricesService = Depends(),
    # allowed: allow_get_items = Depends(),
):
    return templates.TemplateResponse("index.html",{
        "request": request,
        "data": {
            'price':service_prices.get()
        }
        })


@router.get("/sign-in", response_class=HTMLResponse)
def read_item(
    request: Request,
    # maker: str = '',
):
    return templates.TemplateResponse("sign-in.html",{
        "request": request,
        "data": {}
        })

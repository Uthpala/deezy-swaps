from http import HTTPStatus

from fastapi import Request
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates
from lnbits.core.models import User
from lnbits.decorators import check_user_exists  # type: ignore
from lnbits.extensions.diagonalley import diagonalley_ext, diagonalley_renderer
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse

from .crud import get_diagonalley_products, get_diagonalley_stall

templates = Jinja2Templates(directory="templates")


@diagonalley_ext.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(check_user_exists)):
    return diagonalley_renderer().TemplateResponse(
        "diagonalley/index.html", {"request": request, "user": user.dict()}
    )


@diagonalley_ext.get("/{stall_id}", response_class=HTMLResponse)
async def display(request: Request, stall_id):
    stall = await get_diagonalley_stall(stall_id)
    products = await get_diagonalley_products(stall_id)

    if not stall:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Stall does not exist."
        )
    return diagonalley_renderer().TemplateResponse(
        "diagonalley/stall.html",
        {
            "request": request,
            "stall": stall.dict(),
            "products": [product.dict() for product in products]
        },
    )

from fastapi import APIRouter
# from fastapi.responses import JSONResponse

from .auth import router as authrouter

from .reports import router as reports_router

from .html_router import router as page_router

from .routers import (
    MakersRouter,
    BrandsRouter,
    TypeDecorsRouter,
    TypePlatesRouter,
    FormatsRouter,
    DecorsRouter,
    PlatesRouter,
    PricesRouter,
    MaterialsRouter
)


router = APIRouter()

router.include_router(
    reports_router
)

router.include_router(
    page_router
)

router.include_router(
    authrouter
)

router.include_router(
    MakersRouter()
)

router.include_router(
    BrandsRouter()
)

router.include_router(
    TypeDecorsRouter()
)

router.include_router(
    TypePlatesRouter()
)

router.include_router(
    FormatsRouter()
)

router.include_router(
    DecorsRouter()
)

router.include_router(
    PlatesRouter()
)

router.include_router(
    PricesRouter()
)

router.include_router(
    MaterialsRouter()
)

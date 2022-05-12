from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from fastapi.responses import StreamingResponse

from models import User
from services import allow_create_items
from services import ReportsService



router = APIRouter(
    prefix = '/routers',
    tags = ['reports']
)


@router.post('/import')
def import_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    allowed: allow_create_items = Depends(),
    reports_service: ReportsService = Depends()

):
    background_tasks.add_task(
        reports_service.import_csv,
        file.file
    )

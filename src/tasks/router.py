from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from .tasks import send_email_report
from base_config import current_user

router = APIRouter(prefix='/report', tags=['tasks'])


@router.get('/dashboard')
async def get_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
    # background_tasks.add_task(send_email_report, user.username)
    send_email_report.delay(user.username)
    return {
        'status': 200,
        'data': 'Letter sent',
        'details': None
    }

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix='/pages',
    tags=['pages']
)

template = Jinja2Templates(directory='templates')


@router.get('/course')
async def get_course(request: Request):
    return template.TemplateResponse('course.html', {'request': request})

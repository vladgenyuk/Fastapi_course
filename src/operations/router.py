import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from .models import operations
from database import get_async_session
from .schemas import OperationCreate

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


@router.get('/',)
async def get_specific_operations(
        operation_type: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(operations).where(operations.c.type == operation_type)
        result = await session.execute(query)
        ret = [dict(r._mapping) for r in result]
        return {
            'status': 'success',
            'data': ret,
            'details': None
        }
    except Exception:
        # SDELATb LOG B DB!!!!!!!!!!!!!!!!!, Put Patch!!!!!!!!! 
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.post('/')
async def add_specific_operations(new_operation: OperationCreate,  session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operations).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {'result': 'success'}


@router.get('/long_operation')
@cache(expire=30)
async def get_long_op():
    time.sleep(2)
    return "A Lot of info"

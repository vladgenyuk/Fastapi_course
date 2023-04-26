import pytest

from sqlalchemy import insert, select
from auth.models import role
from conftest import client, async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name='admin', permissions=None)
        await session.execute(stmt)
        await session.commit()
        query = select(role)
        result = await session.execute(query)
        result = result.all()
        print("RESULT!!", result)
        assert result == [(1, 'admin', None)], "ROLE not added"


def test_register():
    response = client.post('/auth/register', json={
        "email": "ZUMBA",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    })
    assert response.status_code == 201, "Status code differ from 201"
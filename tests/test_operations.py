from httpx import AsyncClient


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post("/operations/", json={
        "id": 0,
        "quantity": "string",
        "figi": "string",
        "instrument_type": "string",
        "date": "2023-04-22T13:00:50.496",
        "type": "string"
    })
    response = await ac.post("/operations/", json={
        "id": 1,
        "quantity": "string",
        "figi": "string",
        "instrument_type": "string",
        "date": "2023-04-22T13:00:50.492",
        "type": "string"
    })

    assert response.status_code == 200


async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get('/operations/',
                            params={'operation_type': 'string'})

    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert len(response.json()['data']) == 2
"""Test class for endpoints"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from backend.app import create_app
from backend.db.tables import Product as ProductTable
from backend.db.tables import UserCart

test_server = TestClient(create_app())


class MockedQueryResult:
    """class for mocking the results from sqlAlchemy"""
    result: list = []

    def __init__(self, result: list) -> None:
        self.result = result

    def first(self):
        return self.result[0]

    def fetchall(self):
        return self.result


class TestRouter(IsolatedAsyncioTestCase):

    def test_search(self):
        
        record1 = ProductTable(
            id="27ddedb9-d493-423a-8eae-4484419986ba",
            name="Cappotto",
            price=150,
            description="Cappotto di lana merinos",
        )
        record2 = ProductTable(
            id="2badeb13-81a8-4b2c-911a-2f8850fc366d",
            name="T-shirt",
            price=14,
            description="Maglietta con una banana sopra",
        )
        with patch(
            "backend.db.utils.DatabaseSessionMaker", return_value=AsyncMock()
        ), patch(
            "backend.db.utils.DatabaseSessionMaker.get_session",
            return_value=AsyncMock(),
        ), patch(
            "sqlalchemy.ext.asyncio.AsyncSession.execute",
            return_value=MockedQueryResult(result=[[record1], [record2]]),
        ), patch(
            "sqlalchemy.engine.result.ChunkedIteratorResult.fetchall", return_value=None
        ):
            response = test_server.post(url="/search", json={"query": "cuffia"})
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json()["products"][0]["id"],
                "27ddedb9-d493-423a-8eae-4484419986ba",
            )
            self.assertEqual(response.json()["products"][1]["name"], "T-shirt")

            with self.subTest("Test empty result"):
                with patch(
                    "backend.db.utils.DatabaseSessionMaker",
                    return_value=AsyncMock(),
                ), patch(
                    "backend.db.utils.DatabaseSessionMaker.get_session",
                    return_value=AsyncMock(),
                ), patch(
                    "sqlalchemy.ext.asyncio.AsyncSession.execute",
                    return_value=MockedQueryResult(result=[]),
                ), patch(
                    "sqlalchemy.engine.result.ChunkedIteratorResult.fetchall",
                    return_value=None,
                ):
                    response = test_server.post(url="/search", json={"query": "cuffia"})
                    self.assertEqual(len(response.json()["products"]), 0)
    def test_add(self):
        with self.subTest("Test successful add"):
            with patch(
                "backend.db.utils.DatabaseSessionMaker", return_value=AsyncMock()
            ), patch(
                "backend.db.utils.DatabaseSessionMaker.get_session",
                return_value=AsyncMock(),
            ), patch(
                "sqlalchemy.ext.asyncio.AsyncSession.execute",
                return_value=MockedQueryResult(
                    result=[
                        [
                            UserCart(
                                uid="ad5ce827-4a17-4b74-9693-53a2b74f177c",
                                pid="9e94e4ac-4a33-4945-b4aa-cd10f84e6351",
                                quantity=1,
                            )
                        ]
                    ]
                ),
            ):
                response = test_server.post(
                    url="/add_product",
                    json={
                        "user_id": "ad5ce827-4a17-4b74-9693-53a2b74f177c",
                        "product_id": "9e94e4ac-4a33-4945-b4aa-cd10f84e6351",
                        "quantity": 1,
                    },
                )
                self.assertEqual(response.status_code, 200)
            with self.subTest("Test wrong add"):
                with patch(
                    "backend.db.utils.DatabaseSessionMaker",
                    return_value=AsyncMock(),
                ), patch(
                    "backend.api.routers.check_user_exists", return_value=False
                ), patch(
                    "backend.db.utils.DatabaseSessionMaker.get_session",
                    return_value=AsyncMock(),
                ), patch(
                    "sqlalchemy.ext.asyncio.AsyncSession.execute",
                    return_value=MockedQueryResult(
                        result=[
                            [
                                UserCart(
                                    uid="ad5ce827-4a17-4b74-9693-53a2b74f177c",
                                    pid="9e94e4ac-4a33-4945-b4aa-cd10f84e6351",
                                    quantity=1,
                                )
                            ]
                        ]
                    ),
                ):
                    response = test_server.post(
                        url="/add_product",
                        json={
                            "user_id": "ad5ce827-4a17-4b74-9693-53a2b74f177c",
                            "product_id": "9e94e4ac-4a33-4945-b4aa-cd10f84e6351",
                            "quantity": 1,
                        },
                    )
                    self.assertEqual(response.status_code, 404)

    def test_details(self):
        record1 = ProductTable(
            id="27ddedb9-d493-423a-8eae-4484419986ba",
            name="Cappotto",
            price=150,
            description="Cappotto di lana merinos",
        )
        with patch(
            "backend.db.utils.DatabaseSessionMaker", return_value=AsyncMock()
        ), patch(
            "backend.db.utils.DatabaseSessionMaker.get_session",
            return_value=AsyncMock(),
        ), patch(
            "sqlalchemy.ext.asyncio.AsyncSession.execute",
            return_value=MockedQueryResult(result=[[record1]]),
        ), patch(
            "sqlalchemy.engine.result.ChunkedIteratorResult.fetchall", return_value=None
        ):
            response = test_server.post(
                url="/product_details",
                json={"product_id": "27ddedb9-d493-423a-8eae-4484419986ba"},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["product_name"], "Cappotto")
            self.assertEqual(
                response.json()["product_description"], "Cappotto di lana merinos"
            )
            with self.subTest("Test empty result"):
                with patch(
                    "backend.db.utils.DatabaseSessionMaker",
                    return_value=AsyncMock(),
                ), patch(
                    "backend.db.utils.DatabaseSessionMaker.get_session",
                    return_value=AsyncMock(),
                ), patch(
                    "sqlalchemy.ext.asyncio.AsyncSession.execute",
                    return_value=MockedQueryResult(result=[[]]),
                ), patch(
                    "sqlalchemy.engine.result.ChunkedIteratorResult.first",
                    return_value=None,
                ):
                    response = test_server.post(
                        url="/product_details",
                        json={"product_id": "27ddedb9-d493-423a-8eae-4484419986ba"},
                    )
                    self.assertEqual(response.status_code, 404)

    def test_remove_all(self):
        with self.subTest("Test successful removed"):
            with patch(
                "backend.db.utils.DatabaseSessionMaker", return_value=AsyncMock()
            ), patch(
                "backend.db.utils.DatabaseSessionMaker.get_session",
                return_value=AsyncMock(),
            ), patch(
                "sqlalchemy.ext.asyncio.AsyncSession.execute",
                return_value=MockedQueryResult(
                    result=[
                        [
                            UserCart(
                                uid="ad5ce827-4a17-4b74-9693-53a2b74f177c",
                                pid="9e94e4ac-4a33-4945-b4aa-cd10f84e6351",
                                quantity=1,
                            )
                        ]
                    ]
                ),
            ):
                response = test_server.post(
                    url="/product_removal_all",
                    json={
                        "user_id": "ad5ce827-4a17-4b74-9693-53a2b74f177c",
                    },
                )
                self.assertEqual(response.status_code, 200)
            with self.subTest("Test wrong remove"):
                with patch(
                    "backend.db.utils.DatabaseSessionMaker",
                    return_value=AsyncMock(),
                ), patch(
                    "backend.api.routers.check_user_exists", return_value=False
                ), patch(
                    "backend.db.utils.DatabaseSessionMaker.get_session",
                    return_value=AsyncMock(),
                ), patch(
                    "sqlalchemy.ext.asyncio.AsyncSession.execute",
                    return_value=MockedQueryResult(
                        result=[
                            [
                                UserCart(
                                    uid="ad5ce827-4a17-4b74-9693-53a2b74f177c",
                                    pid="9e94e4ac-4a33-4945-b4aa-cd10f84e6351",
                                    quantity=1,
                                )
                            ]
                        ]
                    ),
                ):
                    response = test_server.post(
                        url="/product_removal_all",
                        json={
                            "user_id": "ad5ce827-4a17-4b74-9693-53a2b74f177c",
                        },
                    )
                    self.assertEqual(response.status_code, 404)

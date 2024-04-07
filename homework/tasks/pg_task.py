from dataclasses import dataclass

import asyncpg


@dataclass
class ItemEntry:
    item_id: int
    user_id: int
    title: str
    description: str


class ItemStorage:
    def __init__(self):
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        # We initialize client here, because we need to connect it,
        # __init__ method doesn't support awaits.
        #
        # Pool will be configured using env variables.
        self._pool = await asyncpg.create_pool()

    async def disconnect(self) -> None:
        # Connections should be gracefully closed on app exit to avoid
        # resource leaks.
        await self._pool.close()

    async def create_tables_structure(self) -> None:
        """
        Создайте таблицу items со следующими колонками:
         item_id (int) - обязательное поле, значения должны быть уникальными
         user_id (int) - обязательное поле
         title (str) - обязательное поле
         description (str) - обязательное поле
        """
        # In production environment we will use migration tool
        # like https://github.com/pressly/goose
        # YOUR CODE GOES HERE

        query = """
            create table items
            (
                item_id integer PRIMARY KEY,
                user_id integer NOT NULL,
                title text NOT NULL,
                description text NOT NULL
            )
        """
        await self._pool.execute(query)

    async def save_items(self, items: list[ItemEntry]) -> None:
        """
        Напишите код для вставки записей в таблицу items одним запросом, цикл
        использовать нельзя.
        """
        # Don't use str-formatting, query args should be escaped to avoid
        # sql injections https://habr.com/ru/articles/148151/.
        # YOUR CODE GOES HERE

        items = [
            (item.item_id, item.user_id, item.title, item.description) for item in items
        ]
        await self._pool.executemany(
            """
            insert into items values ($1, $2, $3, $4);
        """,
            items,
        )

    async def find_similar_items(
        self, user_id: int, title: str, description: str
    ) -> list[ItemEntry]:
        """
        Напишите код для поиска записей, имеющих указанные user_id, title и description.
        """
        # YOUR CODE GOES HERE
        query = f"""
            select
                item_id,
                user_id,
                title,
                description

            from items

            where user_id = {user_id}
              and title = '{title}'
              and description = '{description}'
        """
        data = await self._pool.fetch(query)
        data = [
            ItemEntry(
                item_id=item_id, user_id=user_id, title=title, description=description
            )
            for (item_id, user_id, title, description) in data
        ]
        return data

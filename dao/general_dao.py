from sqlalchemy import select, update, delete, and_, func, desc

from sqlalchemy.ext.asyncio import AsyncSession


class GeneralDAO:
    @classmethod
    async def get_all_items(cls, session: AsyncSession, item):
        """
        :param db: database
        :param item: Founding itemS, like models.User
        :return: Founded itemS
        """
        query = select(item)
        items = await session.execute(query)

        return items.scalars().all()

    @classmethod
    async def get_item_by_id(cls, session: AsyncSession, item, item_id: int):
        """
        :param db: database
        :param item: Founding item, like models.User
        :param item_id: Item id
        :return: Founded item
        """

        query = select(item).where(item.id == item_id)
        item = await session.execute(query)

        return item.scalars().first()

    @classmethod
    async def get_item_by_tg_id(cls, session: AsyncSession, item, item_tg_id: int):
        """
        :param db: database
        :param item: Founding item, like models.User
        :param item_tg_id: Item telegram id
        :return: Founded item
        """

        query = select(item).where(item.tg_id == item_tg_id)
        item = await session.execute(query)

        return item.scalars().first()

    @classmethod
    async def delete_item(cls, session: AsyncSession, item, item_id: int):
        """
        :param db: database
        :param item: deleting item
        :param item_id: item id
        :return: nothing
        """

        query = delete(item).where(item.id == int(item_id))

        await session.execute(query)
        await session.commit()



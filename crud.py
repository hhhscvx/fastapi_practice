import asyncio
from pprint import pprint

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload

from core.models import db_helper, User, Profile, Post
from core.models.order import Order
from core.models.order_product_association import OrderProductAssociation
from core.models.product import Product


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print('user:', user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(statement=stmt)
    user: User | None = result.scalar_one_or_none()
    print("Fount user:", username, user)
    return user


async def create_profile(session: AsyncSession,
                         user: User,
                         first_name: str | None,
                         last_name: str | None,
                         bio: str | None) -> Profile:
    profile = Profile(user=user, first_name=first_name, last_name=last_name, bio=bio)
    session.add(profile)
    try:
        await session.commit()
    except IntegrityError:
        print("Profile already exists")
    print('profile:', profile)
    return profile


async def show_users_with_profile(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)  # select_related
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile)


async def create_posts(session: AsyncSession, user: User, *posts_titles: str) -> Post:
    posts = [Post(user=user, title=title) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    pprint(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(
        selectinload(User.posts)  # selectinload использовать для связей ко многим. Делает отдельный запрос для всех постов
    ).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        for post in user.posts:
            print('-', post)


async def get_posts_with_autors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print(post)


async def get_users_with_profile_and_posts(session: AsyncSession):
    stmt = select(User).options(
        joinedload(User.profile),
        selectinload(User.posts)  # подтягивает юзеров именно только с профилем и постами selectinload и joinedload
    ).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile)
        for post in user.posts:
            print('-', post)


async def get_profiles_with_users_and_users_posts(session: AsyncSession):
    stmt = select(Profile).options(
        joinedload(Profile.user).
        selectinload(User.posts)  # подтягивает юзеров именно только с профилем и постами selectinload и joinedload
    ).order_by(Profile.id)

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.last_name)
        print(profile.user.posts)


async def create_order(session: AsyncSession,
                       promocode: str | None = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()

    return order


async def create_product(session: AsyncSession,
                         name: str,
                         description: str,
                         price: int) -> Product:
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()

    return product


async def get_order_with_products_assoc(session: AsyncSession) -> list["Order"]:
    stmt = (
        select(Order)
        .options(selectinload(Order.products_details)  # OrderAssociation.
                 .joinedload(OrderProductAssociation.product)).order_by(Order.id))
    orders = await session.scalars(stmt)

    return list(orders)


async def create_gift_product_to_existing_orders(session: AsyncSession):
    orders = await get_order_with_products_assoc(session)
    product_gift = await create_product(
        session,
        name="Gift",
        description="HUetaaaa",
        price=0
    )
    for order in orders:
        order.products_details.append(OrderProductAssociation(
            count=1,
            unit_price=0,
            product=product_gift
        ))

    await session.commit()


async def main():
    async with db_helper.session_factory() as session:  # тут можно делать че угодно с базой, создавать, выбирать и т.д.
        ...


if __name__ == "__main__":
    asyncio.run(main())

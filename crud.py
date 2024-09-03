import asyncio
from pprint import pprint

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload

from core.models import db_helper, User, Profile, Post


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


async def main():
    async with db_helper.session_factory() as session:  # тут можно делать че угодно с базой, создавать, выбирать и т.д.
        user_sam = await get_user_by_username(session, username="sam")
        user_john = await get_user_by_username(session, username="john")

        # await create_posts(session, user_sam, 'govnojopa', 'celerybroker')
        # await create_posts(session, user_john, 'fastapi VS django', 'Backend > Frontend')
        await get_profiles_with_users_and_users_posts(session)


if __name__ == "__main__":
    asyncio.run(main())

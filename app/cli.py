import asyncio

import typer

from app import schemas
from app.crud import create_user, get_user_by_username, update_user
from app.security import hash_password

app = typer.Typer()


@app.command()
def create_superuser(
        username: str = typer.Option(..., help='The username of the superuser'),
        password: str = typer.Option(..., help='The password of the superuser'),
):
    """Create a superuser."""

    async def _create_superuser():
        db_user = await get_user_by_username(username)
        user = schemas.UserCreateUpdate(username=username, password=hash_password(password), is_staff=True,
                                        is_superuser=True)
        if db_user:
            await update_user(db_user, user)
            typer.echo(f'User with username {username} already exists. But password is updated.')
            raise typer.Exit(code=1)
        await create_user(user)
        typer.echo(f'Superuser {username} created successfully.')

    asyncio.run(_create_superuser())


if __name__ == '__main__':
    app()

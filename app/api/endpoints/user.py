from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.delete(
    '/users/{id}',
    tags=['users'],
    deprecated=True
)
def delete_user(id: str):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=405,
        detail="Удаление пользователей запрещено!"
    )

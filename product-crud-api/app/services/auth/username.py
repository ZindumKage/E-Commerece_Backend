from sqlalchemy.orm import Session

from app.models.user import User

from app.utils.username_suggestions import (
    generate_username_suggestions,
)


def check_username_service(
    db: Session,
    username: str,
):

    existing_user = (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )

    if not existing_user:
        return {
            "available": True,
            "suggestions": [],
        }

    suggestions = (
        generate_username_suggestions(
            db,
            username,
        )
    )

    return {
        "available": False,
        "suggestions": suggestions,
    }
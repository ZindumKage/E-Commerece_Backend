import random

from sqlalchemy.orm import Session

from app.models.user import User


def generate_username_suggestions(
    db: Session,
    username: str,
    count: int = 3,
) -> list[str]:

    suggestions = set()

    while len(suggestions) < count:

        random_number = random.randint(
            100,
            9999,
        )

        suggested_username = (
            f"{username}{random_number}"
        )

        existing_user = (
            db.query(User)
            .filter(
                User.username
                == suggested_username
            )
            .first()
        )

        if not existing_user:
            suggestions.add(
                suggested_username
            )

    return list(suggestions)
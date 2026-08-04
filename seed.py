from faker import Faker

from app import app
from models.db import db
from models.user import User
from models.note import Note

fake = Faker()

with app.app_context():
    print("Clearing old data...")
    Note.query.delete()
    User.query.delete()
    db.session.commit()

    print("Seeding users...")
    users = []
    for _ in range(5):
        user = User(username=fake.unique.user_name())
        user.password = "password123"
        users.append(user)
        db.session.add(user)

    db.session.commit()

    print("Seeding notes...")
    for user in users:
        for _ in range(4):
            note = Note(
                title=fake.sentence(nb_words=4),
                content=fake.paragraph(nb_sentences=3),
                user_id=user.id,
            )
            db.session.add(note)

    db.session.commit()

    print(f"Done! Seeded {len(users)} users, each with 4 notes.")
    print("Example login -> username:", users[0].username, "| password: password123")

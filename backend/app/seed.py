from sqlmodel import Session, select
from app.models.item import Item
from app.config.env import BUCKET_IMAGE_URL
from app.db.database import engine


def seed():
    with Session(engine) as session:
        items_exists = session.exec(select(Item)).first()
        if items_exists:
            return

        items = [
            Item(name="Broad Sword", types="Weapon", quantity=1,
                 image_url=f"{BUCKET_IMAGE_URL}/bronze_sword.png"),

            Item(name="Bronze Helmet", types="Weapon", quantity=1,
                 image_url=f"{BUCKET_IMAGE_URL}/bronze_helmet.png"),

            Item(name="Bronze Armor", types="Armor", quantity=1,
                 image_url=f"{BUCKET_IMAGE_URL}/bronze_armor.png"),

            Item(name="Healing Potion(S)", types="Consumables", quantity=5,
                 image_url=f"{BUCKET_IMAGE_URL}/healing_potion(s).png"),

            Item(name="Mana Potion(S)", types="Consumables", quantity=5,
                 image_url=f"{BUCKET_IMAGE_URL}/mana_potion(s).png"),
        ]

        session.add_all(items)
        session.commit()

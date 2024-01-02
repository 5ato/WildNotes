from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert

from typing import Sequence

from database.models import User, Product
from API.parse import WildberrisParse


class Service:
    def __init__(self, session: Session) -> None:
        self.session = session


class UserService(Service):
    def get(self, telegram_id: int) -> User | None:
        return self.session.execute(select(User).where(User.telegram_id==telegram_id)).scalar()
    
    def create(self, telegram_id: int) -> User | None:
        user = self.get(telegram_id)
        if user: return user
        self.session.execute(insert(User).values(telegram_id=telegram_id))
        self.session.commit()
        return User(telegram_id=telegram_id)


class ProductService(Service):
    def get(self, telegram_id: int, article: str) -> Product | None:
        return self.session.execute(select(Product).where(
            (Product.user_telegram_id==telegram_id) & (Product.article==article))
        ).scalar()

    def get_all(self, telegram_id: int) -> Sequence[Product | None]:
        return self.session.execute(select(Product).where(Product.user_telegram_id==telegram_id)).scalars().all()

    def update(self, telegram_id: int, article: str) -> Product:
        data = WildberrisParse(article).parse(with_image=False)
        self.session.execute(update(Product).where(
            (Product.user_telegram_id==telegram_id) & (Product.article==article)
        ).values(**data, user_telegram_id=telegram_id))
        self.session.commit()
        return Product(**data, user_telegram_id=telegram_id)

    def create(self, telegram_id: int, article: str) -> Product | None:
        product = self.get(telegram_id, article)
        if product: return product
        data = WildberrisParse(article).parse()
        self.session.execute(insert(Product).values(**data, user_telegram_id=telegram_id))
        self.session.commit()
        return Product(**data, user_telegram_id=telegram_id)
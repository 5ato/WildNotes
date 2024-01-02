from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .core import Base
from .annotated import str256, uuidpk


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[uuidpk]
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    
    products: Mapped[list['Product']] = relationship(back_populates='user')
    
    
class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[uuidpk]
    brand: Mapped[str256]
    feedbacks: Mapped[int]
    article: Mapped[str256]
    name: Mapped[str256]
    rating: Mapped[int]
    rating_feedbacks: Mapped[float]
    url_image: Mapped[str | None] = mapped_column(nullable=True)
    price: Mapped[int]
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id', ondelete='CASCADE'))

    user: Mapped[User] = relationship(back_populates='products')

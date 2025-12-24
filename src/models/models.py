from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):  # Пустой базовый класс от которого наследуются все остальные классы для табл
    pass


class ChatRequests(Base):
    __tablename__ = 'chat_requests'

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(index=True)
    prompt: Mapped[str]
    response: Mapped[str]

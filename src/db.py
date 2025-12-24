from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.models.models import ChatRequests

engine = create_engine(url='sqlite:///jarvis.db')

session = sessionmaker(engine)





def get_user_requests(ip_address: str) -> list[ChatRequests]:
    with session() as new_session:
        query = select(ChatRequests).filter_by(ip_address=ip_address)
        result = new_session.execute(query)
        return result.scalars().all()


def add_request_data(ip_address: str, prompt: str, response: str) -> None:
    with session() as new_session:
        new_request = ChatRequests(
            ip_address=ip_address,
            prompt=prompt,
            response=response,
        )
        new_session.add(new_request)
        new_session.commit()

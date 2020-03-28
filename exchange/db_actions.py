from datetime import datetime

from exchange.config import settings
from exchange.data_base import Base, create_session, engine
from exchange.models import Currency


def add_default_currencies() -> None:
    Base.metadata.create_all(engine)
    with create_session() as session:
        if len(session.query(Currency).all()) == 0:
            for c in settings.default_currencies:
                currency = Currency(
                    name=c.name,
                    selling_price=c.selling_price,
                    purchasing_price=c.purchasing_price,
                    modified_at=datetime.now(),
                )
                session.add(currency)


def clear_db() -> None:
    Base.metadata.drop_all(engine)

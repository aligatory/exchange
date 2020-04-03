from datetime import datetime

from exchange.config import settings
from exchange.data_base import Base, create_session, engine
from exchange.models import Currency, CurrencyHistory


def add_default_currencies() -> None:
    Base.metadata.create_all(engine)
    with create_session() as session:
        if len(session.query(Currency).all()) == 0:
            for c in settings.default_currencies:
                now = datetime.now()
                currency = Currency(
                    name=c.name,
                    selling_price=c.selling_price,
                    purchasing_price=c.purchasing_price,
                    modified_at=now,
                )
                session.add(currency)
                session.flush()
                currency_history: CurrencyHistory = CurrencyHistory(
                    currency_id=currency.id,
                    time=now,
                    purchasing_price=currency.purchasing_price,
                    selling_price=currency.selling_price,
                )
                session.add(currency_history)


def clear_db() -> None:
    Base.metadata.drop_all(engine)

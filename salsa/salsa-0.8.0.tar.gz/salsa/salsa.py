from datetime import datetime

from pytz import utc
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy import Table, MetaData
from sqlalchemy import event
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base

from yargs import parse


config = parse('settings')
engine = create_engine(config.dburl, echo=False)
Session = sessionmaker(bind=engine)

metadata = MetaData(bind=engine)
Base = declarative_base()


@event.listens_for(Table, "column_reflect")
def set_utc_date(inspector, table, column_info):
    if isinstance(column_info['type'], types.DateTime):
        column_info['type'] = UTCDateTime()


class UTCDateTime(types.TypeDecorator):
    """Timezone shoud be striped befored inserted into the database.
    Python datetime object will always have a timezone of UTC on read.

    """

    impl = types.DateTime

    def process_bind_param(self, value, engine):
        """Convert datetime into UTC value and Postgres should not store
        timezone info.

        """
        if isinstance(value, datetime):
            return value.astimezone(utc)

    def process_result_value(self, value, engine):
        """All datetime values read from the database are assumed to be UTC."""
        if value is not None:
            return value.replace(tzinfo=utc)

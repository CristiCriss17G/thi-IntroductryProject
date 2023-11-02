from typing import Union

from sqlalchemy.exc import IntegrityError

from src.database import get_db_opener
from src.models import Settings


def get_settings(name: str) -> Union[Settings, None]:
    with get_db_opener() as db:
        return db.query(Settings).filter_by(name=name).first()


def set_settings(name: str, value: str) -> Settings:
    setting = get_settings(name)
    if setting:
        with get_db_opener() as db:
            setting.value = value
            db.commit()
            db.refresh(setting)
            return setting
    else:
        with get_db_opener() as db:
            try:
                db_settings = Settings(name=name, value=value)
                db.add(db_settings)
                db.commit()
                db.refresh(db_settings)
            except IntegrityError as e:
                db.rollback()
                raise e
            return db_settings

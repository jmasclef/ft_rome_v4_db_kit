import time
from typing import Callable, Any

import sqlmodel
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from db.data_access import get_session, create_db_and_tables
from apis.rome_apis import FranceTravailClient
from schemas import rome_schemas
from server_cfg import general_logger


def download_one(session: Session, name: str, get_func: Callable, schema: Any):
    time.sleep(2)
    elements_list = get_func()
    general_logger.info(f"Got list of {name} with {len(elements_list.root)} elements")
    for index, element in enumerate(elements_list):
        time.sleep(0.5)
        try:
            ft_element = get_func(code=element.code)
        except OverflowError:
            general_logger.warning("Exceed requests quota, wait for 2 seconds...")
            time.sleep(2)
            ft_element = get_func(code=element.code)
        db_element = schema(**ft_element.model_dump())
        session.add(db_element)
        try:
            session.commit()
            general_logger.info(f"Element {name} with code={element.code} downloaded in database")
        except IntegrityError:
            general_logger.warning(f"Download element {name} with code={element.code} caused Integrity Error, element skipped")
            session.rollback()
    else:
        general_logger.info(f"List of {name} with {len(elements_list.root)} elements finished")


def download_all(session: Session):
    ft_client = FranceTravailClient(load_credentials_from_env=True)
    jobs = [
        ('Domaines', ft_client.get_domaines, rome_schemas.DomaineMetiers),
        ('GrandsDomaines', ft_client.get_grands_domaines, rome_schemas.GrandDomaineMetiers),
        ('Thèmes', ft_client.get_themes, rome_schemas.Theme),
        ('Métiers', ft_client.get_metiers, rome_schemas.Metier),
        ('Appellations', ft_client.get_appellations, rome_schemas.Appellation),
    ]
    for (name, get_func, schema) in jobs:
        general_logger.info(f"Start job to download {name}")
        download_one(session, name, get_func, schema)
        general_logger.info(f"End of job for {name}")
    else:
        general_logger.info(f"All of the {len(jobs)} jobs are finished")



if __name__ == '__main__':
    create_db_and_tables()
    session = get_session()
    download_all(session)

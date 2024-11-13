from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, text

from iara.database import engine, init_db
from iara.populate import populate_all
from iara.query import (
    query_event_affected_organisms,
    query_event_affected_waters,
    query_event_affects_humans,
    query_event_pollutants,
    query_flow_affected_waters,
    query_directly_affected_organisms,
    query_predation_affects_humans,
    query_predation_affected_organisms,
)


def main():
    # Initialize the database
    init_db()

    # Populate the database
    try:
        populate_all()
    except IntegrityError:
        print("INFO: database was already populated")

    # Query the database
    print(query_predation_affected_organisms(6))
    print(query_predation_affects_humans())
    print(query_flow_affected_waters(5))
    print(query_event_affected_waters(1))
    print(query_event_pollutants(1))
    print(query_directly_affected_organisms(7, 5))
    print(query_event_affected_organisms(2))
    print(query_event_affects_humans(4))


if __name__ == "__main__":
    main()

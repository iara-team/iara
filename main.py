from sqlmodel import Session, text

from iara.database import engine, init_db
from iara.populate import populate_all

def main():
    init_db()
    populate_all()

if __name__ == "__main__":
    main()

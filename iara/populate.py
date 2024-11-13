from sqlmodel import Session, text

from .database import engine

def populate_evento():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO evento (data, epicentro_lat, epicentro_lon) VALUES
                ('2023-01-15', 20.3739, 43.4163);
                """
            ) # type: ignore
        )
        session.commit()

def populate_corpodagua():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO corpodagua (nome, tipo) VALUES 
                ('Lago Paranoá', 'Lago'),
                ('Rio Amazonas', 'Rio'),
                ('Rio Paraná', 'Rio'),
                ('Oceano', 'Oceano');
                """
            ) # type: ignore
        )
        session.commit()

def populate_tipopoluente():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO tipopoluente (nome) VALUES
                ('Agroquímico'),
                ('Microplástico'),
                ('Metal Pesado');
                """
            ) # type: ignore
        )
        session.commit()

def populate_organismo():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO organismo (nome_popular, reino, filo, classe, ordem, familia, genero, especie) VALUES
                ('Tilápia', 'Animalia', 'Chordata', 'Actinopterygii', 'Perciformes', 'Cichlidae', 'Oreochromis', 'Oreochromis niloticus'),
                ('Jacaré-açu', 'Animalia', 'Chordata', 'Reptilia', 'Crocodylia', 'Alligatoridae', 'Melanosuchus', 'Melanosuchus niger'),
                ('Capivara', 'Animalia', 'Chordata', 'Mammalia', 'Rodentia', 'Hydrochoeridae', 'Hydrochoerus', 'Hydrochoerus hydrochaeris'),
                ('Humano', 'Animalia', 'Chordata', 'Mammalia', 'Primata', 'Hominidae', 'Homo', 'Homo sapiens');
                """
            ) # type: ignore
        )
        session.commit()

def populate_poluente():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO Poluente (nome, dl50, tipo_poluente_id) VALUES 
                ('DDT', 115.0, 2),
                ('PET', NULL, 1),
                ('Mercúrio', 0.0005, 3);
                """
            ) # type: ignore
        )
        session.commit()

def populate_fluxo():
    with Session(engine) as session:
        session.exec(
            text(
                """
                """
            ) # type: ignore
        )
        session.commit()

def populate_emissao():
    with Session(engine) as session:
        session.exec(
            text(
                """
                """
            ) # type: ignore
        )
        session.commit()

def populate_compatibilidade():
    with Session(engine) as session:
        session.exec(
            text(
                """
                """
            ) # type: ignore
        )
        session.commit()

def populate_predacao():
    with Session(engine) as session:
        session.exec(
            text(
                """
                """
            ) # type: ignore
        )
        session.commit()


def populate_all():
    populate_evento()
    populate_corpodagua()
    populate_tipopoluente()
    populate_organismo()
    populate_poluente()

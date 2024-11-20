from sqlmodel import Session, text

from .database import engine


def populate_evento():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO evento (data, epicentro_lat, epicentro_lon, descricao) VALUES
                ('2015-11-05', -20.3739, -43.4163, 'Rompimento de barragem de rejeitos de mineração de ferro'),
                ('2020-04-30', -1.217199, -61.748173, 'Escoamento de agrotóxicos utilizados numa grande propriedade rural'),
                ('2023-07-18', -25.667850, -48.416705, 'Naufrágio de um navio de importação de bens de consumo'),
                ('2024-02-27', -20.030595, -39.933147, 'Explosão de uma plataforma de extração de petróleo');
                """
            )  # type: ignore
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
                ('Rio Paracatu', 'Rio'),
                ('Rio Catiringa', 'Rio'),
                ('Rio Indaiá', 'Rio'),
                ('Riacho do Junco', 'Rio'),
                ('Oceano', 'Oceano');
                """
            )  # type: ignore
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
                ('Metal Pesado'),
                ('Petroquímico');
                """
            )  # type: ignore
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
                ('Humano', 'Animalia', 'Chordata', 'Mammalia', 'Primata', 'Hominidae', 'Homo', 'Homo sapiens'),
                ('Espirogira', 'Plantae', 'Chlorophyta', 'Zygnematophyceae', 'Zygnematales', 'Zygnemataceae', 'Spirogyra', 'Spirogyra sp.'),
                ('Sardinha', 'Animalia', 'Chordata', 'Actinopterygii', 'Clupeiformes', 'Clupeidae', 'Sardinella', 'Sardinella brasiliensis'),
                ('Búzio-espinhoso', 'Animalia', 'Mollusca', 'Gastropoda', 'Neogastropoda', 'Muricidae', 'Murex', 'Murex pecten'),
                ('Moreia', 'Animalia', 'Chordata', 'Actinopterygii', 'Anguilliformes', 'Muraenidae', 'Gymnothorax', 'Gymnothorax funebris');
                """
            )  # type: ignore
        )
        session.commit()


def populate_poluente():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO poluente (nome, dl50, tipo_poluente_id) VALUES
                ('DDT', 115.0, 1),
                ('PET', NULL, 2),
                ('LDPE', NULL, 2),
                ('HDPE', NULL, 2),
                ('ABS', NULL, 2),
                ('PA', NULL, 2),
                ('Metil mercúrio', 11.9, 3),
                ('Chumbo', 5610.0, 3),
                ('Anthraceno', NULL, 4),
                ('Tetraceno', NULL, 4),
                ('Pentaceno', NULL, 4);
                """
            )  # type: ignore
        )
        session.commit()


def populate_fluxo():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO fluxo (origem_id, destino_id) VALUES
                (3, 1),  -- Do Rio Paracatu para o Lago Paranoá
                (4, 3),  -- Do Rio Catiringa para o Rio Paracatu
                (1, 2),  -- Do Lago Paranoá para o Rio Amazonas
                (1, 6),  -- Do Lago Paranoá para o Riacho do Junco
                (5, 2),  -- Do Rio Indaiá para o Rio Amazonas
                (2, 7);  -- Do Rio Amazonas para o Oceano
                """
            )  # type: ignore
        )
        session.commit()


def populate_emissao():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO emissao (evento_id, poluente_id, corpodagua_id) VALUES
                (1, 07, 4),  -- Emissão de Metil mercúrio no Rio Catiringa
                (1, 08, 4),  -- Emissão de Chumbo no Rio Catiringa
                (2, 01, 5),  -- Emissão de DDT no Rio Indaiá
                (3, 02, 7),  -- Emissão de PET no Oceano
                (3, 03, 7),  -- Emissão de LDPE no Oceano
                (3, 04, 7),  -- Emissão de HDPE no Oceano
                (3, 05, 7),  -- Emissão de ABS no Oceano
                (3, 06, 7),  -- Emissão de PA no Oceano
                (4, 09, 7),  -- Emissão de Anthraceno no Oceano
                (4, 10, 7),  -- Emissão de Tetraceno no Oceano
                (4, 11, 7);  -- Emissão de Pentaceno no Oceano
                """
            )  # type: ignore
        )
        session.commit()


def populate_compatibilidade():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO compatibilidade (poluente_id, organismo_id) VALUES
                (1, 5),  -- Compatibilidade de DDT com Espirogira

                (2, 1),  -- Compatibilidade de PET com Tilápia
                (2, 2),  -- Compatibilidade de PET com Jacaré-açu
                (2, 3),  -- Compatibilidade de PET com Capivara
                (2, 4),  -- Compatibilidade de PET com Humano
                (2, 6),  -- Compatibilidade de PET com Sardinha

                (3, 1),  -- Compatibilidade de LDPE com Tilápia
                (3, 2),  -- Compatibilidade de LDPE com Jacaré-açu
                (3, 3),  -- Compatibilidade de LDPE com Capivara
                (3, 4),  -- Compatibilidade de LDPE com Humano
                (3, 6),  -- Compatibilidade de LDPE com Sardinha

                (4, 1),  -- Compatibilidade de HDPE com Tilápia
                (4, 2),  -- Compatibilidade de HDPE com Jacaré-açu
                (4, 3),  -- Compatibilidade de HDPE com Capivara
                (4, 4),  -- Compatibilidade de HDPE com Humano
                (4, 6),  -- Compatibilidade de HDPE com Sardinha

                (5, 1),  -- Compatibilidade de ABS com Tilápia
                (5, 2),  -- Compatibilidade de ABS com Jacaré-açu
                (5, 3),  -- Compatibilidade de ABS com Capivara
                (5, 4),  -- Compatibilidade de ABS com Humano
                (5, 6),  -- Compatibilidade de ABS com Sardinha

                (6, 1),  -- Compatibilidade de PA com Tilápia
                (6, 2),  -- Compatibilidade de PA com Jacaré-açu
                (6, 3),  -- Compatibilidade de PA com Capivara
                (6, 4),  -- Compatibilidade de PA com Humano
                (6, 6),  -- Compatibilidade de PA com Sardinha

                (7, 1),  -- Compatibilidade de Metil mercúrio com Tilápia
                (7, 2),  -- Compatibilidade de Metil mercúrio com Jacaré-açu
                (7, 3),  -- Compatibilidade de Metil mercúrio com Capivara
                (7, 4),  -- Compatibilidade de Metil mercúrio com Humano
                (7, 5),  -- Compatibilidade de Metil mercúrio com Espirogira
                (7, 6),  -- Compatibilidade de Metil mercúrio com Sardinha

                (8, 1),  -- Compatibilidade de Chumbo com Tilápia
                (8, 2),  -- Compatibilidade de Chumbo com Jacaré-açu
                (8, 3),  -- Compatibilidade de Chumbo com Capivara
                (8, 4),  -- Compatibilidade de Chumbo com Humano
                (8, 5),  -- Compatibilidade de Chumbo com Espirogira
                (8, 6),  -- Compatibilidade de Chumbo com Sardinha

                (9,  7),  -- Compatibilidade de Anthraceno com Búzio-espinhoso
                (10, 7),  -- Compatibilidade de Tetraceno com Búzio-espinhoso
                (11, 7);  -- Compatibilidade de Pentaceno com Búzio-espinhoso
                """
            )  # type: ignore
        )
        session.commit()


def populate_predacao():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO predacao (presa_id, predador_id) VALUES
                (5, 1),  -- Espirogira é presa de Tilápia
                (1, 2),  -- Tilápia é presa de Jacaré-açu
                (3, 2),  -- Capivara é presa de Jacaré-açu
                (1, 4),  -- Tilápia é presa de Humano
                (6, 4),  -- Sardinha é presa de Humano
                (2, 4),  -- Jacaré-açu é presa de Humano
                (7, 8);  -- Búzio-espinhoso é presa de Moreia
                """
            )  # type: ignore
        )
        session.commit()


def populate_habitat():
    with Session(engine) as session:
        session.exec(
            text(
                """
                INSERT INTO habitat (organismo_id, corpodagua_id) VALUES
                (1, 1),  -- Tilápia  vive no Lago do Paranoá
                (1, 2),  -- Tilápia  vive no Rio Amazonas
                (1, 3),  -- Tilápia  vive no Rio Paracatu
                (1, 4),  -- Tilápia  vive no Rio Catiringa
                (1, 5),  -- Tilápia  vive no Rio Indaiá
                (1, 6),  -- Tilápia  vive no Riacho do Junco

                (2, 2),  -- Jacaré vive no Rio Amazonas
                (3, 2),  -- Capivara vive no Rio Amazonas

                (4, 6),  -- Humano vive no Riacho do Junco

                (5, 1),  -- Espirogira vive no Lago do Paranoá
                (5, 2),  -- Espirogira vive no Rio Amazonas
                (5, 3),  -- Espirogira vive no Rio Paracatu
                (5, 4),  -- Espirogira vive no Rio Catiringa
                (5, 5),  -- Espirogira vive no Rio Indaiá
                (5, 6),  -- Espirogira vive no Riacho do Junco

                (6, 7),  -- Sardinha vive no Oceano
                (7, 7),  -- Búzio-espinhoso vive no Oceano
                (8, 7);  -- Moreia vive no Oceano
                """
            )  # type: ignore
        )
        session.commit()


def populate_all():
    populate_evento()
    populate_corpodagua()
    populate_tipopoluente()
    populate_organismo()
    populate_poluente()
    populate_fluxo()
    populate_emissao()
    populate_compatibilidade()
    populate_predacao()
    populate_habitat()


if __name__ == "__main__":
    populate_all()

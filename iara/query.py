from sqlmodel import Session, select, text

from iara.models import CorpoDagua, Evento, Habitat

from .database import engine


def query_predation_affected_organisms(organismo_id):
    with Session(engine) as session:
        data = session.exec(
            text(
                """
                WITH RECURSIVE cadeia_predadores AS (
                    SELECT
                        o.id,
                        o.nome_popular,
                        o.especie,
                        1 as nivel_cadeia_alimentar
                    FROM organismo o
                    WHERE o.id = :organismo_id
                    UNION
                    SELECT
                        pred.id,
                        pred.nome_popular,
                        pred.especie,
                        cp.nivel_cadeia_alimentar + 1
                    FROM cadeia_predadores cp
                    JOIN predacao p ON cp.id = p.presa_id
                    JOIN organismo pred ON p.predador_id = pred.id
                )
                SELECT * FROM cadeia_predadores ORDER BY nivel_cadeia_alimentar;
                """
            ),  # type: ignore
            params={"organismo_id": organismo_id},
        )
        result = data.all()
        return result


def query_predation_affects_humans():
    with Session(engine) as session:
        data = session.exec(
            text(
                """
                WITH RECURSIVE cadeia_alimentar_humana AS (
                    SELECT
                        o.id,
                        o.nome_popular,
                        o.especie,
                        1 as distancia_do_humano
                    FROM organismo o
                    JOIN predacao p ON o.id = p.presa_id
                    JOIN organismo humano ON p.predador_id = humano.id
                    WHERE humano.nome_popular = 'Humano'
                    UNION

                    SELECT
                        presa.id,
                        presa.nome_popular,
                        presa.especie,
                        cah.distancia_do_humano + 1
                    FROM cadeia_alimentar_humana cah
                    JOIN predacao p ON cah.id = p.predador_id
                    JOIN organismo presa ON p.presa_id = presa.id
                )
                SELECT * FROM cadeia_alimentar_humana ORDER BY distancia_do_humano DESC;
                """
            ),  # type: ignore
        )
        result = data.all()
        return result


def query_flow_affected_waters(corpodagua_id):
    with Session(engine) as session:
        data = session.exec(
            text(
                """
                WITH RECURSIVE fluxo_agua AS (
                    SELECT
                        cd.id AS origem_id,
                        cd.id AS destino_id,
                        cd.nome,
                        cd.tipo,
                        1 AS distancia_fluxo
                    FROM corpodagua cd
                    WHERE cd.id = :corpodagua_id
                    UNION
                    SELECT
                        fa.origem_id,
                        f.destino_id,
                        cd.nome,
                        cd.tipo,
                        fa.distancia_fluxo + 1
                    FROM fluxo_agua fa
                    JOIN fluxo f ON fa.destino_id = f.origem_id
                    JOIN corpodagua cd ON f.destino_id = cd.id
                    WHERE fa.distancia_fluxo < 10
                )
                SELECT * FROM fluxo_agua ORDER BY distancia_fluxo;
                """
            ),  # type: ignore
            params={"corpodagua_id": corpodagua_id},
        )
        result = data.all()
        return result


def query_event_affected_waters(evento_id):
    with Session(engine) as session:
        data = session.exec(
            text(
                """
                WITH RECURSIVE aguas_afetadas AS (
                    SELECT DISTINCT cd.id, cd.nome, cd.tipo, 1 as nivel_contaminacao
                    FROM corpodagua cd
                    INNER JOIN emissao em ON cd.id = em.corpodagua_id
                    WHERE em.evento_id = :evento_id
                    UNION ALL

                    SELECT
                        cd.id,
                        cd.nome,
                        cd.tipo,
                        aa.nivel_contaminacao + 1 as nivel_contaminacao
                    FROM aguas_afetadas aa
                    INNER JOIN fluxo f ON aa.id = f.origem_id
                    INNER JOIN corpodagua cd ON cd.id = f.destino_id
                )
                SELECT
                    aa.id,
                    aa.nome,
                    aa.tipo,
                    aa.nivel_contaminacao,
                    em.evento_id,
                    em.poluente_id,
                    pol.nome,
                    tp.nome
                FROM aguas_afetadas aa, emissao em
                INNER JOIN poluente pol ON em.poluente_id = pol.id
                INNER JOIN tipopoluente tp ON pol.tipo_poluente_id = tp.id
                WHERE em.evento_id = :evento_id
                ORDER BY aa.nivel_contaminacao, aa.nome;
                """
            ),  # type: ignore
            params={"evento_id": evento_id},
        )
        result = data.all()
        return result

def query_waters_inhabited_by_humans():
    with Session(engine) as session:
        statement = select(CorpoDagua.id).join(Habitat).where(Habitat.organismo_id == 4)
        result = session.exec(statement).all()
        return result

def query_event_pollutants(evento_id):
    with Session(engine) as session:
        data = session.exec(
            text(
                """
                SELECT DISTINCT p.nome, p.dl50, tp.nome as tipo_poluente
                FROM emissao em
                JOIN poluente p ON em.poluente_id = p.id
                JOIN tipopoluente tp ON p.tipo_poluente_id = tp.id
                WHERE em.evento_id = :evento_id
                """
            ),  # type: ignore
            params={"evento_id": evento_id},
        )
        result = data.all()
        return result


def query_directly_affected_organisms(corpodagua_id, poluente_id):
    with Session(engine) as session:
        data = session.exec(
            text(
                """
                SELECT DISTINCT
                    o.id,
                    o.nome_popular,
                    o.especie
                FROM organismo as o
                INNER JOIN habitat h ON o.id = h.organismo_id
                INNER JOIN compatibilidade c ON o.id = c.organismo_id
                WHERE h.corpodagua_id = :corpodagua_id AND c.poluente_id = :poluente_id
                """
            ),  # type: ignore
            params={
                "corpodagua_id": corpodagua_id,
                "poluente_id": poluente_id,
            },
        )
        result = data.all()
        return result


def query_event_affected_organisms(evento_id):
    affected_waters = query_event_affected_waters(evento_id)

    result = set()
    for aw in affected_waters:
        corpodagua_id = aw[0]
        poluente_id = aw[5]

        directly_affected_organisms = query_directly_affected_organisms(
            corpodagua_id=corpodagua_id,
            poluente_id=poluente_id,
        )

        for dao in directly_affected_organisms:
            organismo_id = dao[0]
            data = query_predation_affected_organisms(organismo_id)
            result = result.union(set(data))

    return result


def query_event_affects_humans(evento_id):
    affected_organisms = query_event_affected_organisms(evento_id)

    for ao in affected_organisms:
        organism_common_name = ao[1]
        if organism_common_name == "Humano":
            return True
    return False

def query_all_events():
    with Session(engine) as session:
        statement = select(Evento)
        events = session.exec(statement).all()
        return events

def query_event_by_id(event_id):
    with Session(engine) as session:
        evento = session.get(Evento, event_id)
        return evento

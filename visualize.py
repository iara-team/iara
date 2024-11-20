from enum import unique
from typing import TYPE_CHECKING, Sequence
from sqlmodel import Session, select
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd


from iara.query import (
    query_all_events,
    query_event_affected_organisms,
    query_event_affected_waters,
    query_event_affects_humans,
    query_event_by_id,
    query_event_pollutants,
    query_waters_inhabited_by_humans,
)

events = query_all_events()

@st.cache_data
def create_map():
    # Create the folium map
    m = folium.Map(location=[-12, -50], zoom_start=4)

    # Add points to the map
    for event in events:
        lat = event.epicentro_lat
        lon = event.epicentro_lon
        id = event.id
        folium.Marker(
            location=[lat, lon],
            popup=f"Evento {id}",
            tooltip=f"Evento {id}"
        ).add_to(m)
    return m

# Load the cached map
st.write("# Sistema de Monitoramento Iara 🧜🏾‍♀️")

st.write("## Mapa de Eventos de Bioacumulação")
st.write("**Clique em um ponto do mapa para visualizar detalhes do evento**")

m = create_map()
map_data = st_folium(m, width=700, height=500, returned_objects=["last_object_clicked"])

# Handle click events without re-rendering
if map_data and map_data.get("last_object_clicked"):
    clicked_data = map_data["last_object_clicked"]
    lat = clicked_data["lat"]
    lon = clicked_data["lng"]
    event_id = next(
        (event.id for event in events if event.epicentro_lat == lat and event.epicentro_lon == lon),
        None
    )

    # Get data for event
    evento = query_event_by_id(event_id)
    if evento is None:
        raise Exception("Unexpected None value")

    # Get data for emitted pollutants
    emitted_pollutants = query_event_pollutants(event_id)
    columns = ["Nome", "DL50 (mg/mg)", "Categoria"]
    df_pol = pd.DataFrame(emitted_pollutants, columns=columns) # type: ignore

    # Get data for contaminated waters
    contaminated_waters = query_event_affected_waters(event_id)
    waters_name_to_pollutant = {}
    for cw in contaminated_waters:
        water_name = cw[1]
        if water_name not in waters_name_to_pollutant:
            waters_name_to_pollutant[water_name] = []

        pollutant_name = cw[-2]
        pollutant_type = cw[-1]
        waters_name_to_pollutant[water_name].append(
            f"{pollutant_name} ({pollutant_type})"
        )

    # Get data for affected organisms
    affected_organisms = query_event_affected_organisms(event_id)
    affected_organisms = [ao[1:] for ao in affected_organisms]
    columns = ["Nome", "Espécie", "Nível trófico"]
    df_org = pd.DataFrame(affected_organisms, columns=columns) # type: ignore

    # Get data for waters inhabited by humans
    waters_with_humans = query_waters_inhabited_by_humans()
    contaminated_waters_ids = [cw[0] for cw in contaminated_waters]
    waters_with_humans_affected: bool = False
    for wh in waters_with_humans:
        if wh in contaminated_waters_ids:
            waters_with_humans_affected = True
            break

    # Were humans affected?
    humans_affected: bool = query_event_affects_humans(event_id)

    # Display event header
    st.write(f"## Evento {event_id}")
    st.write(f"**Data:** {evento.data.strftime('%d/%m/%Y')}")
    st.write(f"**Epicentro:** {lat} x {lon}")
    st.write(evento.descricao)

    # Display summary dashboard
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            if humans_affected:
                st.error("Este evento resultou/resultará em bioacumulação humana", icon="🚨")
            else:
                st.info("Este evento não resultou/resultará em bioacumulação humana", icon="ℹ️")
        with col2:
            if waters_with_humans_affected:
                st.error("Este evento afetou/afetará corpos d'água com populações humanas", icon="🚨")
            else:
                st.info("Este evento não afetou/afetará corpos d'água com populações humanas", icon="ℹ️")
    st.divider()

    # Display data for emitted pollutants
    st.write("### Poluentes emitidos")
    with st.container():
        st.dataframe(df_pol)

    # Display data for affected organisms
    st.write("### Organismos afetados")
    with st.container():
        st.dataframe(df_org)

    # Display data for contaminated waters
    st.write("### Corpos d'água contaminados")
    with st.container():
        for waters_name, pollutants in waters_name_to_pollutant.items():
            st.write(f"- **{waters_name}**: {", ".join(pollutants)}")

    # Display summary dashboard
    st.divider()
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Número de poluente emitidos",
                len(df_pol),
            )
        with col2:
            st.metric(
                "Número de organismos afetados",
                len(df_org),
            )
        with col3:
            st.metric(
                "Número de corpos d'água contaminados",
                len(waters_name_to_pollutant),
            )
    st.divider()


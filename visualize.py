from enum import unique
from typing import Sequence
from sqlmodel import Session, select
import streamlit as st
import folium
from streamlit_folium import st_folium


# fmt: off
from iara.query import query_event_affected_organisms, query_event_affected_waters
from iara.models import Evento
from iara.database import engine
# fmt: on

events: Sequence[Evento]
with Session(engine) as session:
    statement = select(Evento)
    affected_waters = session.exec(statement)
    events = affected_waters.all()

@st.cache_data
def create_map():
    # Create the folium map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Add points to the map
    for event in events:
        lat = event.epicentro_lat
        lon = event.epicentro_lon
        id = event.id
        folium.Marker(
            location=[lat, lon],
            popup=f"Evento: {id}<br>Lat: {lat}<br>Lng: {lon}",
            tooltip=f"Evento: {id}"
        ).add_to(m)
    return m

# Load the cached map
st.write("### Interactive Map with Clickable Points")
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

    with Session(engine) as session:
        evento = session.get(Evento, event_id)

    if evento is None:
        raise Exception("Unexpected None value")

    st.header(f"Evento: {event_id}")
    st.write("### Detalhes")
    st.write(evento.descricao)
    st.write(f"**Coordenadas:** {lat} x {lon}")

    affected_waters = query_event_affected_waters(event_id)


    st.subheader("Corpos d'água afetados")
    with st.container():
        unique_affected_waters = set()
        unique_pollutants = set()
        for aw in affected_waters:
            # Get waters name
            water_name = aw[1]
            unique_affected_waters.add(water_name)

            # Get pollutant name
            pollutant = aw[-2]
            unique_pollutants.add(pollutant)

            # Get pollutant type
            pollutant_type = aw[-1]

            # Write to page
            st.write(f"{water_name}: {pollutant} ({pollutant_type})")

        # Nested columns within container
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Número de corpos d'água afetados", len(unique_affected_waters))
        with col2:
            st.metric("Número de poluente emitidos", len(unique_pollutants))

else:
    st.write("Click on a point on the map to view details.")

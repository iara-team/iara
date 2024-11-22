# Iara 🧜🏾‍♀️

A relational database for bioaccumulation data

## Installation

1. Clone this repository and enter its directory

```bash
git clone https://github.com/iara-team/iara && cd iara
```

2. Create a python virtual environment and source it

```bash
python -m venv .venv && source .venv/bin/activate
```

3. Install the `poetry` Python package from PyPI

```bash
pip install poetry
```

4. Install the `iara` Python package from your local copy of the repository:

```bash
poetry install
```

5. Pull the container image for postgres

```bash
podman pull docker.io/library/postgres:latest
```
6. Create a podman container with the following command line:

```bash
podman run -d \
  --name iara \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_USER=username \
  -e POSTGRES_DB=iara \
  -v "$HOME/Documents/repos/iara/database" \
  -p 5432:5432 \
  postgres:latest
```

7. Then, run the script that populates the database

```bash
python main.py
```

8. Finally, run the visualization application

```bash
streamlit run visualize.py
```

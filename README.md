# Predictor
Ten projekt to prosta aplikacja predykcyjna uczenia maszynowego oparta na FastAPI, która akceptuje dane w postaci JSON lub CSV i zwraca przewidywane wartości. 
Można uruchomić ją lokalnie, w kontenerze Docker lub pobrać obraz z Docker Hub w celu łatwej konfiguracji.

## Spis treści
- [Funkcje](#funkcje)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
  - [Klonowanie repozytorium](#klonowanie-repozytorium)
  - [Uruchamianie lokalnie](#uruchamianie-lokalnie)
  - [Uruchamianie z Dockerem](#uruchamianie-z-dockerem)
  - [Użycie obrazu z Docker Hub](#użycie-obrazu-z-docker-hub)
- [Interface API](#interface-api)
- [Przykłady](#przykłady)

## Funkcje
- Akceptuje dane JSON i CSV do przewidywań
- Może być uruchamiany lokalnie lub w kontenerze Docker
- Wstępnie wyszkolony model

## Wymagania
- Python 3.9+
- menedżer pakietów `pip`

## Instalacja

### Klonowanie repozytorium
1. Sklonuj repozytorium:
    ```bash
    git clone https://github.com/KingaMendyk/predictor.git
    cd predictor
    ```

### Uruchamianie lokalnie

Uruchom aplikację lokalnie przy pomocy terminala. W katalogu ze sklonowanym repozytorium wykonaj następujące polecenia:

1. **Zainstaluj wymagania**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Uruchom aplikację Fast API**:
    ```bash
    uvicorn predictor:app --host 0.0.0.0 --port 8000
    ```

3. **Uzyskaj dostęp do aplikacji**:
   - Aplikacja dostępna jest pod `http://127.0.0.1:8000`.
   - Dostęp do dokumentacji można uzyskać pod adresem `http://127.0.0.1:8000/docs` do interaktywnego testowania.
  W celu przesłania danych do aplikacji uruchom nowe okno terminala i skorzystaj z sekcji [Przykłady](#przykłady). 

### Uruchamianie z Dockerem

Upewnij się, że uruchomiony jest Docker Engine w aplikacji Docker Desktop.

1. **Zbuduj obraz Dockera**:
    ```bash
    docker build -t predictor .
    ```

2. **Uruchom kontener Docker**:
    ```bash
    docker run -p 8000:8000 predictor
    ```

3. **Uzyskaj dostęp do aplikacji**:
   - Aplikacja dostępna jest pod `http://127.0.0.1:8000`.
  W celu przesłania danych do aplikacji uruchom nowe okno terminala i skorzystaj z sekcji [Przykłady](#przykłady). 

### Użycie obrazu z Docker Hub

Obraz aplikacji jest opublikowany w Docker Hub. Wykonaj następujące kroki, aby go pobrać i uruchomić:

1. **Pobierz obraz Dockera**:
    ```bash
    docker pull kingamendyk/predictor:latest
    ```

2. **Uruchom kontener Docker**:
    ```bash
    docker run -p 8000:8000 kingamendyk/predictor:latest
    ```

3. **Uzyskaj dostęp do aplikacji**:
   - Aplikacja dostępna jest pod `http://127.0.0.1:8000`.
  W celu przesłania danych do aplikacji uruchom nowe okno terminala i skorzystaj z sekcji [Przykłady](#przykłady).

## Interface API

- **`POST /predict-json`**: Akceptuje plik JSON zawierający listę danych wejściowych do przewidywania.
- **`POST /predict-csv`**: Akceptuje plik CSV zawierający dane wejściowe do przewidywania.

## Przykłady

### FastAPI

#### Plik CSV

Przygotuj plik CSV, np. o nazwie `data.csv`. Upewnij się, że plik znajduje się w tym samym katalogu, z którego uruchamiasz polecenie curl, lub podaj pełną ścieżkę do pliku. Następnie wykonaj polecenie poprzez:
```bash
curl -X POST "http://127.0.0.1:8000/predict-csv" -F "file=@data.csv"
```

#### Plik JSON

Przygotuj plik JSON, np. o nazwie `data.json`. Upewnij się, że wszystkie dane znajdują sie pod polem "data", przykładowo:
```json
{
	"data":
  {
    "rownames": [1],
    "gender": ["male"],
    "ethnicity": ["other"],
    "fcollege": ["yes"],
    "mcollege": ["no"],
    "home": ["yes"],
    "urban": ["yes"],
    "unemp": [6.199999809],
    "wage": [8.090000153],
    "distance": [0.200000003],
    "tuition": [0.889150023],
    "education": [12],
    "income": ["high"],
    "region": ["other"]
  }
}
```

Upewnij się, że plik znajduje się w tym samym katalogu, z którego uruchamiasz polecenie curl, lub podaj pełną ścieżkę do pliku. Następnie wykonaj polecenie poprzez:
```bash
curl -X POST "http://127.0.0.1:8000/predict-json" -H "Content-Type: application/json" -d @data.json
```

### CLI

#### Plik CSV

Przygotuj plik CSV, np. o nazwie `data.csv`. Upewnij się, że plik znajduje się w tym samym katalogu, z którego uruchamiasz polecenie curl, lub podaj pełną ścieżkę do pliku. Następnie wykonaj polecenie poprzez:
```bash
python predictor.py predict-csv data.csv 
```

#### Plik JSON

Przygotuj plik JSON, np. o nazwie `data.json`. Upewnij się, że wszystkie dane znajdują sie pod polem "data", przykładowo:
```json
{
	"data":
  {
    "rownames": [1],
    "gender": ["male"],
    "ethnicity": ["other"],
    "fcollege": ["yes"],
    "mcollege": ["no"],
    "home": ["yes"],
    "urban": ["yes"],
    "unemp": [6.199999809],
    "wage": [8.090000153],
    "distance": [0.200000003],
    "tuition": [0.889150023],
    "education": [12],
    "income": ["high"],
    "region": ["other"]
  }
}
```
 
Upewnij się, że plik znajduje się w tym samym katalogu, z którego uruchamiasz polecenie curl, lub podaj pełną ścieżkę do pliku. Następnie wykonaj polecenie poprzez:
```bash
python predictor.py predict-json data.json 
```


# Predictor
Ten projekt to prosta aplikacja predykcyjna uczenia maszynowego oparta na FastAPI, która akceptuje dane w postaci JSON lub CSV i zwraca p5rzewidywane wartości. 
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

### Uruchamianie z Dockerem

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

### Użycie obrazu z Docker Hub

Obraz aplikacji jest również opublikowany w Docker Hub w celu łatwego dostępu. Wykonaj następujące kroki, aby go pobrać i uruchomić:

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

## Interface API

- **`POST /predict-json`**: Akceptuje obiekt JSON zawierający listę danych wejściowych do przewidywania.
- **`POST /predict-csv`**: Akceptuje plik CSV zawierający dane wejściowe do przewidywania.

### Przykłady

## Plik CSV
Przygotuj plik CSV, np. o nazwie `data.csv`. Nastepnie wykonaj żądanie poprzez:
```bash
curl -X POST "http://127.0.0.1:8000/predict-csv" -F "file=@data.csv"
```

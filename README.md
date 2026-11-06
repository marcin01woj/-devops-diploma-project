# DevOps Monitoring Project

## 1. Opis projektu

Projekt przedstawia środowisko DevOps służące do konteneryzacji, monitorowania i automatyzacji procesu budowania oraz publikowania aplikacji internetowej.

Głównym celem projektu jest stworzenie aplikacji internetowej opartej na Python Flask, uruchamianej w Dockerze, której działanie jest monitorowane przez Prometheus i Grafana.

Projekt wykorzystuje również GitHub Actions do automatycznego testowania aplikacji, budowania obrazów Docker oraz publikowania ich w GitHub Container Registry (GHCR).

## 2. Wykorzystane technologie

- **Python** – język programowania.
- **Flask** – framework do budowy aplikacji internetowej.
- **Docker** – konteneryzacja aplikacji i usług.
- **Docker Compose** – zarządzanie wieloma kontenerami.
- **Prometheus** – zbieranie i przechowywanie metryk.
- **Grafana** – wizualizacja danych i monitorowanie systemu.
- **Gmail SMTP** – wysyłanie powiadomień e-mail.
- **Pytest** – automatyczne testowanie aplikacji.
- **Git i GitHub** – kontrola wersji i przechowywanie kodu.
- **GitHub Actions** – automatyzacja procesu CI/CD.
- **GitHub Container Registry (GHCR)** – przechowywanie obrazów Docker.

## 3. Architektura systemu

System monitorowania składa się z trzech głównych usług:

1. **Flask Application** – aplikacja internetowa udostępniająca endpointy `/`, `/health` i `/metrics`.
2. **Prometheus** – cyklicznie pobiera metryki z aplikacji Flask.
3. **Grafana** – pobiera dane z Prometheusa, prezentuje je na dashboardzie i obsługuje reguły alertów.

Usługi uruchamiane są za pomocą Docker Compose.

Dane Grafany przechowywane są w trwałym wolumenie Docker.

## 4. Dashboard Grafana

Dashboard `DevOps Monitoring` zawiera siedem paneli:

1. **Request Rate** – tempo przychodzących żądań.
2. **Total Requests** – łączna liczba żądań.
3. **Application Health** – aktualny stan aplikacji.
4. **Memory Usage** – zużycie pamięci RAM przez proces.
5. **CPU Usage** – wykorzystanie procesora przez proces.
6. **HTTP 5xx Errors** – tempo występowania błędów serwera HTTP.
7. **HTTP Success Rate** – procent poprawnych odpowiedzi HTTP.

## 5. System alertów

W Grafanie skonfigurowano regułę alertu:

**Application is DOWN!**

Reguła wykorzystuje zapytanie PromQL:

```promql
up{job="devops-app"}
```

Warunki alertu:
- wartość poniżej 1;
- czas oczekiwania: 1 minuta;
- częstotliwość ewaluacji: 1 minuta.

Powiadomienia wysyłane są za pomocą Gmail SMTP.

Dane dostępowe SMTP przechowywane są w lokalnym pliku `.env`.

## 6. Testowanie aplikacji

Projekt wykorzystuje framework Pytest do automatycznego testowania aplikacji Flask.

Przygotowano trzy testy:

1. **test_home_page** – sprawdza dostępność strony głównej i kod odpowiedzi HTTP 200.
2. **test_health_endpoint** – sprawdza endpoint `/health` i zwracany status `healthy`.
3. **test_metrics_endpoint** – sprawdza dostępność endpointu `/metrics` i obecność metryk Prometheus.

Uruchomienie testów lokalnie:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

Wszystkie trzy testy zakończyły się powodzeniem.

## 7. CI/CD – GitHub Actions

Projekt wykorzystuje GitHub Actions do automatyzacji procesu Continuous Integration i Continuous Delivery.

Workflow znajduje się w pliku:

`.github/workflows/ci.yml`

### Continuous Integration (CI)

Po wysłaniu zmian do gałęzi `main` lub `feature/ci-cd` GitHub Actions automatycznie:

1. Pobiera kod repozytorium.
2. Przygotowuje środowisko Python 3.12.
3. Instaluje zależności z `requirements-dev.txt`.
4. Uruchamia testy automatyczne Pytest.
5. Buduje obraz Docker na podstawie Dockerfile.

Workflow jest również uruchamiany przy Pull Requestach kierowanych do gałęzi `main`.

### Continuous Delivery (CD)

Po pomyślnym zakończeniu zadania `test-and-build` uruchamiane jest zadanie `publish`.

Proces publikowania:

1. Konfiguruje Docker Buildx.
2. Loguje się do GitHub Container Registry przy użyciu `GITHUB_TOKEN`.
3. Generuje tagi obrazu.
4. Buduje obraz Docker.
5. Publikuje obraz w GHCR.

Publikowanie wykonywane jest po zdarzeniu `push`, a nie podczas samego Pull Requesta.

Do publikowania wykorzystywane są uprawnienia `packages: write`.

### Schemat pipeline'u

```text
        Git Push / Pull Request
                  |
                  v
             GitHub Actions
                  |
                  v
          Instalacja zależności
                  |
                  v
          Automatyczne testy
                  |
                  v
          Budowanie obrazu
                  |
                  v
             Test-and-build
                  |
                  v
          Czy zadanie udane?
                  |
                  v
          Publikowanie obrazu
                  |
                  v
       GitHub Container Registry
                  |
                  v
          Gotowy obraz Docker
```

## 8. GitHub Container Registry

Obrazy aplikacji publikowane są w GitHub Container Registry.

Repozytorium obrazu:

`ghcr.io/marcin01woj/devops-diploma-project`

Wykorzystywane tagi:

- `latest` – najnowsza opublikowana wersja obrazu.
- `sha-...` – wersja obrazu powiązana z konkretnym commitem Git.

Przykład pobrania obrazu:

```bash
docker pull ghcr.io/marcin01woj/devops-diploma-project:latest
```

Uruchomienie pobranego obrazu:

```bash
docker run -d --name devops-app-ghcr-test -p 5001:5000 ghcr.io/marcin01woj/devops-diploma-project:latest
```

Sprawdzenie działania aplikacji:

- Strona główna: `http://localhost:5001/`
- Health check: `http://localhost:5001/health`
- Metryki: `http://localhost:5001/metrics`

## 9. Uruchomienie projektu

### Wymagania

- Docker Desktop.
- Docker Compose.
- Git.

### Uruchomienie usług

```bash
docker compose up -d --build
```

Sprawdzenie kontenerów:

```bash
docker compose ps
```

Zatrzymanie usług:

```bash
docker compose stop
```

## 10. Dostęp do usług

| Usługa | Adres |
|---|---|
| Flask Application | http://localhost:5000 |
| Flask Metrics | http://localhost:5000/metrics |
| Prometheus | http://localhost:9090 |
| Prometheus Targets | http://localhost:9090/targets |
| Grafana | http://localhost:3000 |

## 11. Bezpieczeństwo i przechowywanie danych

- Hasła i dane dostępowe SMTP przechowywane są w lokalnym pliku `.env`.
- Plik `.env` jest wykluczony z repozytorium za pomocą `.gitignore`.
- Publikowanie obrazów GHCR wykorzystuje automatyczny token `GITHUB_TOKEN`.
- Uprawnienia do publikowania pakietów ograniczone są do zadania `publish`.
- Dane Grafany przechowywane są w trwałym wolumenie Docker.

## 12. Wyniki projektu

W ramach realizacji projektu potwierdzono poprawność działania następujących elementów:

- uruchamianie aplikacji Flask w kontenerze Docker;
- zbieranie metryk przez Prometheus;
- wizualizacja metryk w Grafanie;
- automatyczne wykrywanie niedostępności aplikacji;
- wysyłanie powiadomień e-mail;
- wykonywanie testów automatycznych;
- automatyczne budowanie obrazu Docker przez GitHub Actions;
- publikowanie obrazu w GitHub Container Registry;
- pobieranie opublikowanego obrazu na komputer;
- uruchamianie aplikacji z opublikowanego obrazu.

Projekt realizuje Continuous Integration oraz Continuous Delivery. Automatyczne wdrażanie na zewnętrznym serwerze nie jest częścią obecnego zakresu projektu.
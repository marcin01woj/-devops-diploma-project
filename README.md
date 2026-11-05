# DevOps Monitoring Project

## 1. Opis projektu

Projekt przedstawia system monitorowania aplikacji internetowej oparty na technologii Docker, Python Flask, Prometheus oraz Grafana.

Głównym celem projektu jest stworzenie środowiska umożliwiającego monitorowanie działania aplikacji, zbieranie i analizowanie metryk oraz automatyczne wykrywanie awarii i wysyłanie powiadomień e-mail.

## 2. Wykorzystane technologie

- **Python** – język programowania.
- **Flask** – framework do budowy aplikacji internetowej.
- **Docker** – konteneryzacja aplikacji i usług.
- **Docker Compose** – zarządzanie wieloma kontenerami.
- **Prometheus** – zbieranie i przechowywanie metryk.
- **Grafana** – wizualizacja danych i monitorowanie systemu.
- **Gmail SMTP** – wysyłanie powiadomień e-mail.

## 3. Architektura systemu

System składa się z trzech głównych usług:

1. **Flask Application** – aplikacja internetowa udostępniająca metryki pod adresem `/metrics`.
2. **Prometheus** – cyklicznie pobiera metryki z aplikacji Flask.
3. **Grafana** – pobiera dane z Prometheusa, prezentuje je na dashboardzie i obsługuje reguły alertów.

Wszystkie usługi uruchamiane są za pomocą Docker Compose.

## 4. Dashboard Grafana

Dashboard DevOps Monitoring zawiera siedem paneli:

1. Request Rate – tempo przychodzących żądań.
2. Total Requests – łączna liczba żądań.
3. Application Health – aktualny stan aplikacji.
4. Memory Usage – zużycie pamięci RAM przez proces.
5. CPU Usage – wykorzystanie procesora przez proces.
6. HTTP 5xx Errors – tempo występowania błędów serwera HTTP.
7. HTTP Success Rate – procent poprawnych odpowiedzi HTTP.

## 5. System alertów

W Grafanie skonfigurowano regułę alertu:

**Application is DOWN!**

Reguła wykorzystuje zapytanie PromQL:

```promql
up{job="devops-app"}
```

Warunek alertu:
- wartość poniżej 1,
- czas oczekiwania: 1 minuta,
- częstotliwość ewaluacji: 1 minuta.

Powiadomienia wysyłane są za pomocą Gmail SMTP.

## 6. Testowanie systemu

Przeprowadzono test wykrywania awarii aplikacji.

**Scenariusz awarii:**
1. Zatrzymanie kontenera aplikacji.
2. Wykrycie niedostępności przez Prometheus.
3. Zmiana stanu alertu w Grafanie.
4. Wysłanie powiadomienia e-mail.

**Scenariusz odzyskiwania:**
1. Ponowne uruchomienie kontenera aplikacji.
2. Przywrócenie statusu UP w Prometheusie.
3. Powrót alertu Grafany do stanu Normal.

Oba scenariusze zakończyły się powodzeniem.

## 7. Uruchomienie projektu

Wymagania:
- Docker Desktop,
- Docker Compose,
- Git.

Uruchomienie usług:

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

## 8. Dostęp do usług

| Usługa | Adres |
|---|---|
| Flask Application | http://localhost:5000 |
| Flask Metrics | http://localhost:5000/metrics |
| Prometheus | http://localhost:9090 |
| Prometheus Targets | http://localhost:9090/targets |
| Grafana | http://localhost:3000 |

## 9. Bezpieczeństwo i przechowywanie danych

- Hasła i dane dostępowe przechowywane są w pliku `.env`.
- Plik `.env` jest wykluczony z repozytorium za pomocą `.git
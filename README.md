# Task Tracker - Menadżer Zadań

Prosta aplikacja CLI do zarządzania zadaniami napisana w Pythonie.

## Funkcjonalności
- Dodawanie nowych zadań
- Usuwanie istniejących zadań
- Wyświetlanie listy wszystkich zadań
- Sortowanie zadań
- Wyszukiwanie zadań
- Edycja zadań (od wersji 1.2.0)
- Prosty interfejs tekstowy 
- Prosty interfejs webowy (obecnie w formie webowej z ograniczoną funkcjonalnością)

## Instalacja
1. Sklonuj repozytorium za pomocą komendy: git clone https://github.com/Dawid123DJ/task-tracker.git  
2. Zainstaluj wymagane biblioteki z pliku requirements.txt  
3. Następnie przejdź do odpowiedniego katalogu za pomocą: cd task-tracker  
4. Uruchom aplikację komendą: python task_tracker.py  
5. Dokonaj wyboru czy chcesz używać aplikacji w formie tekstowej czy za pomocą Web UI: http://localhost:8000/  

## Użycie  
Po uruchomieniu programu wybierz opcję z menu:

### Przykład: 
1. Dodaj zadanie
2. Usuń zadanie
3. Wyświetl zadania
4. Sortuj zadania
5. Wyszukaj zadania
6. Edytuj zadanie
7. Powrót do menu głównego  
Wybierz opcję: 1  
Podaj treść zadania: Kupic mleko  
Dodano zadanie: Kupic mleko  

## Deployment  
AWS Elastic Beanstalk  
1. Zainstaluj AWS EB CLI
2. Skonfiguruj dostęp:  
eb init task-tracker -p python-3.11 --region eu-north-1  
eb create task-tracker-env  
3. Wypchnij zmiany i wdroż:  
git push origin main  
eb deploy  
4. Po zakończeniu wdrażania aplikacja będzie dostępna pod adresem wygenerowanym przez AWS Elastic Beanstalk

## Workflow CI/CD (GitHub Actions)  
Po każdym push/pull request na main:
- Uruchamiane są testy  
- Budowany jest Docker  
- Automatyczny deploy na AWS EB (tylko z main)
- Po wdrożeniu wykonywany jest health check aplikacji, aby upewnić się, że działa poprawnie  

## Wymagania
Python 3.6+ 

## Licencja
Projekt jest dostępny na licencji MIT - szczegóły w pliku LICENSE.

## Autor
Dawid123DJ
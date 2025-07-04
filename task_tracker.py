import yaml
import threading
from flask import Flask, jsonify, render_template, request, redirect, url_for

APP_VERSION = "1.3.0"
tasks = []
app = Flask(__name__)

# -------------------------------------------------------------------
# Flask REST & Web UI
# -------------------------------------------------------------------

@app.route('/health')
def health_check():
    """Endpoint health check zwraca JSON z podstawowymi danymi o usłudze."""
    return jsonify({
        'status': 'OK',
        'version': APP_VERSION,
        'task_count': len(tasks),
        'service': 'Task Tracker'
    })

@app.route('/')
def index():
    """Strona główna: pokazuje listę zadań i formularz do dodawania/usuwania."""
    return render_template(
        'index.html',
        version=APP_VERSION,
        tasks=list(enumerate(tasks))
    )

@app.route('/add', methods=['POST'])
def web_add():
    """Dodaje zadanie przez formularz webowy."""
    task = request.form.get('task', '').strip()
    if task:
        add_task(task)
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def web_remove():
    """Usuwa zadanie przez formularz webowy."""
    try:
        idx = int(request.form.get('index', -1))
        remove_task(idx)
    except ValueError:
        pass
    return redirect(url_for('index'))

# -------------------------------------------------------------------
# Funkcje wspólne (CLI + Web API)
# -------------------------------------------------------------------

def add_task(task: str):
    """Dodaje zadanie do listy, zapisuje i drukuje komunikat."""
    tasks.append(task)
    print(f"Dodano zadanie: {task}")
    save_tasks()

def remove_task(index: int):
    """Usuwa zadanie o danym indeksie, jeśli istnieje."""
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        print(f"Usunięto zadanie: {removed}")
        save_tasks()
    else:
        print("Nie ma zadania o podanym indeksie")

def list_tasks():
    """Wyświetla listę zadań w CLI."""
    if not tasks:
        print("Brak zadań.")
    else:
        print("Lista zadań:")
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task}")

def sort_tasks():
    """Sortuje zadania alfabetycznie w CLI."""
    tasks.sort(key=lambda x: x.lower())
    print("Zadania posortowane alfabetycznie!")
    save_tasks()

def search_tasks(task_list, keywords):
    """Wyszukiwanie zadań – zwraca listę zadań zawierających wszystkie słowa kluczowe."""
    if not task_list or not keywords:
        return []
    keyword_list = [k.lower() for k in keywords.split()]
    return [
        task for task in task_list
        if all(keyword in task.lower() for keyword in keyword_list)
    ]

def edit_task(task_list, index, new_task):
    """Edytuje treść zadania na pozycji `index`."""
    if not new_task.strip():
        raise ValueError("Treść zadania nie może być pusta")
    if 0 <= index < len(task_list):
        task_list[index] = new_task
    else:
        raise IndexError("Nieprawidłowy indeks zadania")

def save_tasks():
    """Zapisuje listę zadań do pliku YAML."""
    with open('tasks.yaml', 'w') as f:
        yaml.dump(tasks, f)

def load_tasks():
    """Ładuje listę zadań z pliku YAML (lub inicjuje pustą, jeśli nie ma pliku)."""
    global tasks
    try:
        with open('tasks.yaml', 'r') as f:
            tasks = yaml.safe_load(f) or []
    except FileNotFoundError:
        tasks = []

def show_main_menu():
    print(f"\n===== TASK TRACKER - SYSTEM ZADAŃ v{APP_VERSION} =====")
    print("1. Zarządzanie zadaniami")
    print("2. Zapisz i wyjdź")
    print(f"Status aplikacji: http://localhost:8000/health")
    return input("Wybierz opcję: ")

def show_task_menu():
    print("\n===== ZARZĄDZANIE ZADANIAMI =====")
    print("1. Dodaj zadanie")
    print("2. Usuń zadanie")
    print("3. Wyświetl zadania")
    print("4. Sortuj zadania")
    print("5. Wyszukaj zadania")
    print("6. Edytuj zadanie")
    print("7. Powrót do menu głównego")
    return input("Wybierz opcję: ")

def main_cli():
    """Interaktywny tryb CLI – dokładnie tak, jak było wcześniej."""
    load_tasks()
    while True:
        main_choice = show_main_menu()
        if main_choice == '1':
            while True:
                task_choice = show_task_menu()
                if task_choice == '1':
                    task = input("Podaj treść zadania: ")
                    add_task(task)
                elif task_choice == '2':
                    list_tasks()
                    if tasks:
                        idx = int(input("Podaj indeks zadania do usunięcia: ")) - 1
                        remove_task(idx)
                    else:
                        print("Brak zadań do usunięcia")
                elif task_choice == '3':
                    list_tasks()
                elif task_choice == '4':
                    sort_tasks()
                elif task_choice == '5':
                    keyword = input("Podaj frazę do wyszukania: ")
                    results = search_tasks(tasks, keyword)
                    if results:
                        print("\nZnalezione zadania:")
                        for i, t in enumerate(results, 1):
                            print(f"{i}. {t}")
                    else:
                        print("Brak wyników wyszukiwania")
                elif task_choice == '6':
                    list_tasks()
                    if tasks:
                        try:
                            idx = int(input("Podaj indeks zadania do edycji: ")) - 1
                            current = tasks[idx]
                            print(f"Edytujesz zadanie: '{current}'")
                            confirm = input("Czy na pewno chcesz edytować? (T/N): ")
                            if confirm.lower() != 't':
                                print("Anulowano edycję")
                                continue
                            new_content = input("Podaj nową treść zadania: ")
                            edit_task(tasks, idx, new_content)
                            save_tasks()
                            print("Zadanie zaktualizowane!")
                        except (ValueError, IndexError) as e:
                            print(f"Błąd: {e}")
                    else:
                        print("Brak zadań do edycji")
                elif task_choice == '7':
                    break
                else:
                    print("Nieprawidłowa opcja")
        elif main_choice == '2':
            save_tasks()
            print("Zapisano zmiany. Do zobaczenia!")
            break
        else:
            print("Nieprawidłowa opcja")

if __name__ == "__main__":
    # Uruchom serwer Flask w tle
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000), daemon=True)
    flask_thread.start()
    # A potem uruchom tryb CLI
    main_cli()

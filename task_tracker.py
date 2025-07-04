import json
import yaml
import threading
from flask import Flask, jsonify

APP_VERSION = "1.3.0"
tasks = []
app = Flask(__name__)

# Endpoint health check
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'OK',
        'version': APP_VERSION,
        'task_count': len(tasks),
        'service': 'Task Tracker'
    })

def run_flask_app():
    app.run(host='0.0.0.0', port=8000)

def add_task(task):
    tasks.append(task)
    print(f"Dodano zadanie: {task}")
    save_tasks()

def remove_task(index):
    if index < len(tasks):
        removed = tasks.pop(index)
        print(f"Usunięto zadanie: {removed}")
        save_tasks()
    else:
        print("Nie ma zadania o podanym indeksie")

def list_tasks():
    if not tasks:
        print("Brak zadań.")
    else:
        print("Lista zadań:")
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task}")

def save_tasks():
    with open('tasks.yaml', 'w') as f:
        yaml.dump(tasks, f)

def load_tasks():
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

def sort_tasks():
    global tasks
    tasks.sort(key=lambda x: x.lower())
    print("Zadania posortowane alfabetycznie!")
    save_tasks()

def search_tasks(task_list, keywords):
    if not task_list or not keywords:
        return []
    
    keyword_list = [k.lower() for k in keywords.split()]
    
    return [task for task in task_list 
            if all(keyword in task.lower() for keyword in keyword_list)]

def edit_task(task_list, index, new_task):
    if not new_task.strip():
        raise ValueError("Treść zadania nie może być pusta")
        
    if 0 <= index < len(task_list):
        task_list[index] = new_task
    else:
        raise IndexError("Nieprawidłowy indeks zadania")

def main_cli():
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
                        index = int(input("Podaj indeks zadania do usunięcia: ")) - 1
                        remove_task(index)
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
                        for i, task in enumerate(results, 1):
                            print(f"{i}. {task}")
                    else:
                        print("Brak wyników wyszukiwania")
                elif task_choice == '6':
                    list_tasks()
                    if tasks:
                        try:
                            index = int(input("Podaj indeks zadania do edycji: ")) - 1
                            current_task = tasks[index]
                            print(f"Edytujesz zadanie: '{current_task}'")
                            
                            confirm = input("Czy na pewno chcesz edytować? (T/N): ")
                            if confirm.lower() != 't':
                                print("Anulowano edycję")
                                continue
                                
                            new_content = input("Podaj nową treść zadania: ")
                            
                            if not new_content.strip():
                                print("Błąd: Treść zadania nie może być pusta!")
                                continue
                                
                            edit_task(tasks, index, new_content)
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
    # Uruchom serwer Flask w osobnym wątku
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Uruchom główną aplikację CLI
    main_cli()
import json
import yaml

APP_VERSION = "1.2.0"
tasks = []


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
    print(f"===== TASK TRACKER - SYSTEM ZADAŃ v{APP_VERSION} =====")
    print("1. Zarządzanie zadaniami")
    print("2. Zapisz i wyjdź")
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

if __name__ == "__main__":
    load_tasks()  # Ładowanie zadań przy starcie
    
    while True:
        main_choice = show_main_menu()

        if main_choice == '1':
            while True:
                task_choice = show_task_menu()

                if task_choice == '1':
                    task = input("Podaj treść zadania: ")
                    add_task(task)
                elif task_choice == '2':
                    index = int(input("Podaj indeks zadania do usunięcia: ")) - 1
                    remove_task(index)
                elif task_choice == '3':
                    list_tasks()
                elif task_choice == '4':  # Sortowanie
                    sort_tasks()
                elif task_choice == '5':  # Wyszukiwanie
                    keyword = input("Podaj frazę do wyszukania: ")
                    results = search_tasks(tasks, keyword)
                    if results:
                        print("\nZnalezione zadania:")
                        for i, task in enumerate(results, 1):
                            print(f"{i}. {task}")
                    else:
                        print("Brak wyników wyszukiwania")
                elif task_choice == '6':  # Edycja zadania
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
                            
                            # Walidacja nowej treści
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
                elif task_choice == '7':  # Powrót
                    break
                else:
                    print("Nieprawidłowa opcja")

        elif main_choice == '2':
            save_tasks()
            break
        else:
            print("Nieprawidłowa opcja")

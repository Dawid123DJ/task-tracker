import json
import yaml
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
    print("===== TASK TRACKER - SYSTEM ZADAŃ =====")
    print("1. Zarządzanie zadaniami")
    print("2. Zapisz i wyjdź")
    return input("Wybierz opcję: ")

def show_task_menu():
    print("1. Dodaj zadanie")
    print("2. Usuń zadanie")
    print("3. Wyświetl zadania")
    print("4. Powrót do menu głównego")
    print("5. Sortuj zadania")
    return input("Wybierz opcję: ")

def sort_tasks():
    global tasks
    tasks.sort(key=lambda x: x.lower())
    print("Zadania posortowane alfabetycznie!")

if __name__ == "__main__":
    # ... inicjalizacja zadań ...
    
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
                elif task_choice == '4':
                    break
                elif task_choice == '5':
                    sort_tasks()
                else:
                    print("Nieprawidłowa opcja")
                    
        elif main_choice == '2':
            save_tasks()  # Funkcja do zapisu zadań
            break
        else:
            print("Nieprawidłowa opcja")

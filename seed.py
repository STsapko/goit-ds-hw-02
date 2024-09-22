from faker import Faker
from random import randint
import sqlite3

NUMBER_USERS = 10
NUMBER_TASKS = 20
STATUSES = [('new',), ('in progress',), ('completed',)]

# Генерація випадкових даних для користувачів та завдань
def generate_fake_data(num_users, num_tasks):
    fake_users = []  # Зберігатимемо користувачів
    fake_tasks = []  # Зберігатимемо завдання
    fake_data = Faker()

    # Генерація випадкових користувачів з пов'язаними email
    for _ in range(num_users):
        full_name = fake_data.name()
        email = f"{full_name.replace(' ', '.').lower()}@example.com"
        fake_users.append((full_name, email))

    # Генерація випадкових завдань
    for _ in range(num_tasks):
        title = fake_data.sentence(nb_words=4)
        description = fake_data.paragraph(nb_sentences=3)
        fake_tasks.append((title, description))

    return fake_users, fake_tasks

# Підготовка даних для вставки у базу
def prepare_data(users, tasks):
    prepared_users = users  # Імена і email вже пов'язані при генерації
    prepared_tasks = []

    # Підготовка завдань з випадковими значеннями статусів та користувачів
    for task in tasks:
        status_id = randint(1, len(STATUSES))
        user_id = randint(1, NUMBER_USERS)
        prepared_tasks.append((task[0], task[1], status_id, user_id))

    return prepared_users, prepared_tasks

def insert_data_to_db(users, tasks, statuses):
    # Створюємо з'єднання з базою даних
    with sqlite3.connect('tasks_ms.db') as con:
        cur = con.cursor()

        # Вставка даних у таблицю users
        sql_to_users = """INSERT INTO users(fullname, email)
                          VALUES (?, ?)"""
        cur.executemany(sql_to_users, users)

        # Вставка даних у таблицю status з опцією IGNORE для уникнення помилок
        sql_to_statuses = """INSERT OR IGNORE INTO status(name)
                             VALUES (?)"""
        cur.executemany(sql_to_statuses, statuses)

        # Вставка даних у таблицю tasks
        sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id)
                          VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_tasks, tasks)

        # Фіксація змін
        con.commit()

if __name__ == "__main__":
    # Генерація випадкових даних
    users, tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    
    # Підготовка даних для вставки
    prepared_users, prepared_tasks = prepare_data(users, tasks)
    
    # Вставка даних у базу
    insert_data_to_db(prepared_users, prepared_tasks, STATUSES)
    
    print("Дані успішно додані до бази даних!")

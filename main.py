# Если я правильно понял, то в тестовой таблице "domains.db" существует 2 "project_id" и для каждого из них
# уникальным паттерном домена является "xxx.com" и "yyy.com" соответственно; и в таблицу "rules" нужно добавить,
# в данном случае, 2 записи: {project_id = 1234, regexp = \w+\.xxx\.com}; {project_id = 5678, regexp = \w+\.yyy\.com}
# Скрипт написал уникальный, который сначала собирает все уникальные домены по каждому "project_id" и потом добавляет
# "project_id" и "regexp" в таблицу "rules"

import sqlite3


def insert_regular_expressions():
    with sqlite3.connect('domains.db') as conn:
        cursor = conn.cursor()
        domains_result = cursor.execute('SELECT DISTINCT project_id FROM domains').fetchall()

        projects_id_list = []  # список уникальных значений поля "project_id" в таблице "domains"
        for project_id in domains_result:
            projects_id_list.append(int(project_id[0]))

        domains_dict = dict()  # в словаре "domains_dict" будут хранится пары key (project_id) и value (domain)
        # В результате, на основе "domains.db" словарь будет выглядеть следующим образом: {1234: "xxx.com", 5678: "yyy.com"}
        for project_id in projects_id_list:
            domain = cursor.execute('SELECT name FROM domains WHERE project_id = ?', (str(project_id),)).fetchone()
            domains_dict[project_id] = '.'.join(str(domain[0]).split('.')[-2::])

        for project_id, domain in domains_dict.items():
            pattern = rf'\w+\.{domain}'  # регулярное выражение для каждого домена (например, если домен имеет вид
            # "xxx.com", то регулярное выражение для него будет иметь вид "[some_domain].xxx.com")
            cursor.execute('INSERT INTO rules values (?, ?)', (project_id, pattern))  # вставляю в таблицу "rules"
            # уникальные "project_id" и "regexp" (pattern)


if __name__ == '__main__':
    insert_regular_expressions()

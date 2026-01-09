import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
import ttkbootstrap
import datetime
from PIL import ImageTk, Image

DB_FILENAME = "workshop.db"
current_date = datetime.datetime.now().strftime('%Y-%m-%d')


class Database:
    def __init__(self, filename=DB_FILENAME):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON;")
        self.conn.commit()
        self._ensure_schema()

    def _ensure_schema(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS clients(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullName TEXT NOT NULL,
                contactDetails TEXT NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS suppliers(
                idsupplier INTEGER PRIMARY KEY AUTOINCREMENT,
                nameOfCompany TEXT NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS componentPurchase(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nameOfComponent TEXT NOT NULL,
                supplier_id INTEGER,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(idsupplier) ON DELETE SET NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS masters(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullName TEXT NOT NULL,
                current INTEGER NOT NULL DEFAULT 1
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS listOfJob(
                id_viewOfJob INTEGER PRIMARY KEY AUTOINCREMENT,
                nameOfViewJob TEXT NOT NULL,
                cost INTEGER NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS components(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idComponents INTEGER NOT NULL,
                idListOfJob INTEGER NOT NULL,
                FOREIGN KEY (idListOfJob) REFERENCES listOfJob(id_viewOfJob) ON DELETE CASCADE,
                FOREIGN KEY (idComponents) REFERENCES listComponents(idComponents) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS listComponents(
                idComponents INTEGER PRIMARY KEY AUTOINCREMENT,
                nameOfComponents TEXT NOT NULL,
                cost INTEGER NOT NULL,
                manufacturer TEXT NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS ordersForDiagnostics(
                ordersForDiagnostics_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                master_id INTEGER NOT NULL,
                entry_date TEXT NOT NULL,
                yesOrNot TEXT NOT NULL DEFAULT 'false',
                doneNotDone TEXT NOT NULL DEFAULT 'false',
                payment TEXT NOT NULL DEFAULT 'false',
                gotARepairOrder TEXT NOT NULL DEFAULT 'false',
                FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
                FOREIGN KEY (master_id) REFERENCES masters(id) ON DELETE SET NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS viewOfJob(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ordersForDiagnostics_id INTEGER NOT NULL,
                id_view INTEGER NOT NULL,
                FOREIGN KEY (ordersForDiagnostics_id) REFERENCES ordersForDiagnostics(ordersForDiagnostics_id) ON DELETE CASCADE,
                FOREIGN KEY (id_view) REFERENCES listOfJob(id_viewOfJob) ON DELETE CASCADE
            );
            """,
        ]
        for q in queries:
            self.cur.execute(q)
        self.conn.commit()

    def execute(self, sql, params=None):
        if params is None:
            params = []
        self.cur.execute(sql, params)
        return self.cur

    def executemany(self, sql, seq_of_params):
        self.cur.executemany(sql, seq_of_params)
        return self.cur

    def commit(self):
        self.conn.commit()

    def fetchall(self, sql, params=None):
        c = self.execute(sql, params)
        return c.fetchall()

    def fetchone(self, sql, params=None):
        c = self.execute(sql, params)
        return c.fetchone()

    def lastrowid(self):
        return self.cur.lastrowid

    def close(self):
        self.conn.close()


# Инициализировать Базу Данных
db = Database()

# ----------------------
# GUI
# ----------------------
root = tk.Tk()
root.title("Управление базой данных мастерской")
root.geometry("950x750")

style = ttkbootstrap.Style('cosmo')

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill=BOTH)

# Создание фреймов
logAndPass = ttk.Frame(notebook)
client = ttk.Frame(notebook)
masters = ttk.Frame(notebook)
ordersForDiagnostics = ttk.Frame(notebook)
viewOfJob = ttk.Frame(notebook)
accessories = ttk.Frame(notebook)
order = ttk.Frame(notebook)
report_work = ttk.Frame(notebook)

# Добавляем вкладки
notebook.add(logAndPass, text="Авторизация")
notebook.add(client, text="Клиенты")
notebook.add(masters, text="Мастера")
notebook.add(ordersForDiagnostics, text="Диагностика")
notebook.add(viewOfJob, text="Виды работ")
notebook.add(accessories, text="Комплектующие")
notebook.add(order, text="Заказ")
notebook.add(report_work, text="Отчёт")

# Показываем только авторизацию
notebook.select(logAndPass)

# Скрываем остальные вкладки
notebook.hide(client)
notebook.hide(masters)
notebook.hide(ordersForDiagnostics)
notebook.hide(viewOfJob)
notebook.hide(accessories)
notebook.hide(order)
notebook.hide(report_work)

# ----------------------
# Авторизация
# ----------------------

def login():
    data_login = entry_login.get()
    if data_login:
        data_password = entry_password.get()
        if data_login == 'admin' and data_password == 'admin':

            # Показываю ВСЕ вкладки
            notebook.add(client, text="Клиенты")
            notebook.add(masters, text="Мастера")
            notebook.add(ordersForDiagnostics, text="Диагностика")
            notebook.add(viewOfJob, text="Виды работ")
            notebook.add(accessories, text="Комплектующие")
            notebook.add(order, text="Заказ")
            notebook.add(report_work, text="Отчёт")

            notebook.hide(logAndPass)
            notebook.select(client)

            messagebox.showinfo("Успешно", "Авторизован!")
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")


def showpass():
    entry_password.config(show='' if entry_password['show'] == '*' else '*')


ttkbootstrap.Label(logAndPass, text='Логин:', bootstyle='primary').pack(pady=16)
entry_login = ttkbootstrap.Entry(logAndPass, width=40, bootstyle='primary')
entry_login.pack()

ttkbootstrap.Label(logAndPass, text='Пароль:', bootstyle='primary').pack(pady=16)
entry_password = ttkbootstrap.Entry(logAndPass, width=40, show='*', bootstyle='primary')
entry_password.pack()
ttkbootstrap.Button(logAndPass, text='Показать', bootstyle='primary', command=showpass).place(x=650, y=180)

ttkbootstrap.Button(logAndPass, text='Войти', bootstyle='primary', command=login).pack(pady=20)

# ----------------------
# Вспомогательные функции пользовательского интерфейса
# ----------------------

def center_pack(widget, pady=6):
    widget.pack(anchor=NW, padx=6, pady=pady)

# ----------------------
# Clients
# ----------------------
client_Name = []


def update_client_lists():
    rows = db.fetchall("SELECT id, fullName, contactDetails FROM clients")
    client_Name.clear()
    for it in rows:
        client_Name.append(f"{it['id']} - {it['fullName']} - {it['contactDetails']}")

    # Обновляем comboboxes если они есть
    if 'combobox_ordersForDiagnostics' in globals():
        combobox_ordersForDiagnostics['values'] = client_Name
    if 'combobox_order' in globals():
        combobox_order['values'] = client_Name


def client_save():
    client_add = entry.get().strip()
    contact_details = entry2.get().strip()
    if client_add and contact_details:
        sql = "INSERT INTO clients (fullName, contactDetails) VALUES (?, ?)"
        db.execute(sql, (client_add, contact_details))
        db.commit()
        messagebox.showinfo("Успешно", "Клиент успешно добавлен!")
        entry.delete(0, END)
        entry2.delete(0, END)
        update_client_lists()
    else:
        messagebox.showerror("Ошибка", "Заполните все поля для регистрации нового клиента!")


# Инициализация списка клиентов
rows = db.fetchall("SELECT id, fullName, contactDetails FROM clients")
for i in rows:
    client_Name.append(f"{i['id']} - {i['fullName']} - {i['contactDetails']}")
languages_var_client_init = StringVar(value=client_Name[0] if client_Name else '')

# Виджеты вкладки Клиенты
label = ttk.Label(client, text="Имя")
label.pack(anchor=NW, padx=6, pady=6)

entry = ttk.Entry(client)
entry.pack(anchor=NW, padx=6, pady=6)

label2 = ttk.Label(client, text="Контактные данные")
label2.pack(anchor=NW, padx=6, pady=6)

entry2 = ttk.Entry(client)
entry2.pack(anchor=NW, padx=6, pady=6)

btn = ttk.Button(client, text="Сохранить", command=client_save)
btn.pack(anchor=NW, padx=6, pady=6)

# ----------------------
# Masters
# ----------------------
master_Name = []


def update_master_lists():
    rows = db.fetchall("SELECT id, fullName FROM masters WHERE current = 1")
    master_Name.clear()
    for i in rows:
        master_Name.append(f"{i['id']} - {i['fullName']}")

    if 'combobox_master' in globals():
        combobox_master['values'] = master_Name
        languages_var.set(master_Name[0] if master_Name else '')
    if 'combobox_ordersForDiagnostics_master' in globals():
        combobox_ordersForDiagnostics_master['values'] = master_Name
        languages_var22.set(master_Name[0] if master_Name else '')


def master_save():
    master_add = entry_master.get().strip()
    if master_add:
        sql = "INSERT INTO masters (fullName, current) VALUES (?, ?)"
        db.execute(sql, (master_add, 1))
        db.commit()
        entry_master.delete(0, END)
        update_master_lists()
        messagebox.showinfo("Успешно", "Добавлен новый мастер!")
    else:
        messagebox.showerror("Ошибка", "Введите имя мастера!")


def master_del():
    selected_master = combobox_master.get().strip()
    if selected_master:
        try:
            master_id = int(selected_master.split(" - ")[0])
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат ID мастера.")
            return

        sql = "UPDATE masters SET current = ? WHERE id = ?"
        db.execute(sql, (0, master_id))
        db.commit()
        update_master_lists()
        messagebox.showinfo("Успешно", "Мастер успешно уволен!")
    else:
        messagebox.showerror("Ошибка", "Выберите мастера для увольнения.")

# Инициализация списка мастеров
rows = db.fetchall("SELECT id, fullName FROM masters WHERE current = 1")
for i in rows:
    master_Name.append(f"{i['id']} - {i['fullName']}")

languages = master_Name
languages_var = StringVar(value=languages[0] if languages else '')

# Виджеты вкладки Мастера
label_view_master = ttk.Label(masters, text="Принять на работу мастера")
label_view_master.pack(anchor=NW, padx=6, pady=6)

label_master = ttk.Label(masters, text="Имя")
label_master.pack(anchor=NW, padx=6, pady=6)

entry_master = ttk.Entry(masters)
entry_master.pack(anchor=NW, padx=6, pady=6)

btn = ttk.Button(masters, text="Принять на работу нового мастера", command=master_save)
btn.pack(anchor=NW, padx=6, pady=6)

label1 = ttk.Label(masters, text="Увольнение мастера")
label1.pack(anchor=NW, padx=6, pady=6)

label = ttk.Label(masters, text="Выбрать мастера", textvariable=languages_var)
label.pack(anchor=NW, padx=6, pady=6)

combobox_master = ttk.Combobox(masters, textvariable=languages_var, values=languages)
combobox_master.pack(anchor=NW, padx=6, pady=6)

btn = ttk.Button(masters, text="Уволить мастера", command=master_del)
btn.pack(anchor=NW, padx=6, pady=6)

# --------------------
# Диагностика / Заказы
# --------------------

def ordersForDiagnostics_save():
    client_selected = languages_var11.get().strip()
    master_selected = languages_var22.get().strip()

    if not client_selected or not master_selected:
        messagebox.showerror("Ошибка", "Выберите клиента и мастера!")
        return

    try:
        client_id = int(client_selected.split(" - ")[0])
        master_id = int(master_selected.split(" - ")[0])
    except ValueError:
        messagebox.showerror("Ошибка", "Ошибка форматирования ID клиента/мастера.")
        return

    entry_date = str(current_date)
    yesOrNot = "false"
    doneNotDone = "false"
    payment = "false"
    gotARepairOrder = "false"

    sql = ("INSERT INTO ordersForDiagnostics (client_id, master_id, entry_date, yesOrNot, doneNotDone, payment, "
           "gotARepairOrder) VALUES (?, ?, ?, ?, ?, ?, ?)")
    val = (client_id, master_id, entry_date, yesOrNot, doneNotDone, payment, gotARepairOrder)
    db.execute(sql, val)
    db.commit()
    messagebox.showinfo("Успешно", "Заказ на диагностику успешно добавлен!")


# Инициализация списков для Comboboxes
master_Name_diag = master_Name
client_Name_diag = client_Name

languages_var22 = StringVar(value=master_Name_diag[0] if master_Name_diag else '')
languages_var11 = StringVar(value=client_Name_diag[0] if client_Name_diag else '')

# Виджеты вкладки Диагностика
label1 = ttk.Label(ordersForDiagnostics, text="Выбрать мастера")
label1.pack(anchor=NW, padx=6, pady=6)

labell = ttk.Label(ordersForDiagnostics, text="Выбранный мастер:", textvariable=languages_var22)
labell.pack(anchor=NW, padx=6, pady=6)

combobox_ordersForDiagnostics_master = ttk.Combobox(ordersForDiagnostics, textvariable=languages_var22,
                                                    values=master_Name_diag, width=40)
combobox_ordersForDiagnostics_master.pack(anchor=NW, padx=6, pady=6)

label2 = ttk.Label(ordersForDiagnostics, text="Выбрать клиента")
label2.pack(anchor=NW, padx=6, pady=6)

label2l = ttk.Label(ordersForDiagnostics, text="Выбранный клиент:", textvariable=languages_var11)
label2l.pack(anchor=NW, padx=6, pady=6)

combobox_ordersForDiagnostics = ttk.Combobox(ordersForDiagnostics, textvariable=languages_var11,
                                             values=client_Name_diag,
                                             width=40)
combobox_ordersForDiagnostics.pack(anchor=NW, padx=6, pady=6)

label_current_time = ttk.Label(ordersForDiagnostics, text="Текущая дата:")
label_current_time.pack(anchor=NW, padx=6, pady=6)

label_time = ttk.Label(ordersForDiagnostics, text=str(current_date))
label_time.pack(anchor=NW, padx=6, pady=6)

btn = ttk.Button(ordersForDiagnostics, text="Добавить заказ", command=ordersForDiagnostics_save)
btn.pack(anchor=NW, padx=6, pady=6)

# -----------------------
# Задания и компоненты
# -----------------------
selected_items_component = []


def update_listbox_job():
    rows = db.fetchall("SELECT id_viewOfJob, nameOfViewJob, cost FROM listOfJob")
    listofjob_Name.clear()
    for i in rows:
        listofjob_Name.append(f"{i['id_viewOfJob']} - {i['nameOfViewJob']} - {i['cost']}")
    languages_var.set(listofjob_Name)
    if 'languages_listbox_job' in globals():
        languages_listbox_job.delete(0, END)
        for item in listofjob_Name:
            languages_listbox_job.insert(END, item)


def update_listbox_component():
    rows = db.fetchall("SELECT idComponents, nameOfComponents, cost, manufacturer FROM listComponents")
    global components_Name
    components_Name = [f"{i['idComponents']} - {i['nameOfComponents']} - {i['cost']} - {i['manufacturer']}" for i in rows]
    languages_var_component.set(components_Name)


def viewOfJob_save():
    viewOfJob_add = viewOfJob_save1.get().strip()
    cost_value = cost.get().strip()

    if not viewOfJob_add or not cost_value:
        messagebox.showerror("Ошибка", "Введите название работы и ее стоимость!")
        return

    try:
        cost_value = int(cost_value)
    except ValueError:
        messagebox.showerror("Ошибка", "Стоимость должна быть числом.")
        return

    # Сохраняем новый вид работы
    sql = "INSERT INTO listOfJob (nameOfViewJob, cost) VALUES (?, ?)"
    db.execute(sql, (viewOfJob_add, cost_value))
    db.commit()

    new_job_id = db.lastrowid()

    # Привязываем выбранные комплектующие
    for item in selected_items_component:
        try:
            component_id = int(item.split(" - ")[0])
        except ValueError:
            print(f"Пропуск некорректного элемента: {item}")
            continue

        sql1 = "INSERT INTO components (idComponents, idListOfJob) VALUES (?, ?)"
        db.execute(sql1, (component_id, new_job_id))
        db.commit()

    update_listbox_job()

    # Очистка полей
    viewOfJob_save1.delete(0, END)
    cost.delete(0, END)
    languages_listbox_component.selection_clear(0, END)
    selected_items_component.clear()
    selection_label_component["text"] = "вы выбрали: "

    messagebox.showinfo("Успешно", f"Вид работы '{viewOfJob_add}' и комплектующие сохранены успешно!")


label2_viewOfJob = ttk.Label(viewOfJob, text="Название работ")
label2_viewOfJob.pack(anchor=NW, padx=6, pady=6)

viewOfJob_save1 = ttk.Entry(viewOfJob)
viewOfJob_save1.pack(anchor=NW, padx=6, pady=6)

label3_viewOfJob = ttk.Label(viewOfJob, text="Цена ремонта")
label3_viewOfJob.pack(anchor=NW, padx=6, pady=6)

cost = ttk.Entry(viewOfJob)
cost.pack(anchor=NW, padx=6, pady=6)

label_components = ttk.Label(viewOfJob, text="Выбор комплектующих")
label_components.pack(anchor=NW, padx=6, pady=6)


def selected1(event):
    global selected_items_component
    selected_indices_component = languages_listbox_component.curselection()
    selected_items_component = [languages_listbox_component.get(i) for i in selected_indices_component]
    msg = f"вы выбрали: {', '.join([item.split(' - ')[1] for item in selected_items_component])}"
    selection_label_component["text"] = msg

# Инициализация списка комплектующих
rows = db.fetchall("SELECT idComponents, nameOfComponents, cost, manufacturer FROM listComponents")
components_Name = [f"{i['idComponents']} - {i['nameOfComponents']} - {i['cost']} - {i['manufacturer']}" for i in rows]

selection_label_component = ttk.Label(viewOfJob, text="вы выбрали: ")
selection_label_component.pack(anchor=NW, fill=X, padx=5, pady=5)
languages_var_component = StringVar(value=components_Name)
languages_listbox_component = Listbox(viewOfJob, listvariable=languages_var_component, selectmode=EXTENDED, height=6)
languages_listbox_component.pack(anchor=NW, fill=X, padx=5, pady=5)
languages_listbox_component.bind("<<ListboxSelect>>", selected1)

btn = ttk.Button(viewOfJob, text="Добавить вид работы", command=viewOfJob_save)
btn.pack(anchor=NW, padx=6, pady=6)

# ------------------------
# Комплектующие + цена
# ------------------------

def accessories_save():
    name = entry2_viewOfJob_save.get().strip()
    manufacturer = entry3_viewOfJob_save.get().strip()
    cost_str = entry4_viewOfJob_save.get().strip()

    if not name or not manufacturer or not cost_str:
        messagebox.showerror("Ошибка", "Заполните все поля.")
        return

    try:
        cost_value = int(cost_str)
    except ValueError:
        messagebox.showerror("Ошибка", "Стоимость должна быть числом.")
        return

    sql = "INSERT INTO listComponents (nameOfComponents, cost, manufacturer) VALUES (?,?,?)"
    db.execute(sql, (name, cost_value, manufacturer))
    db.commit()

    # Получаем последнюю запись
    last = db.fetchone("SELECT idComponents, nameOfComponents, cost, manufacturer FROM listComponents ORDER BY idComponents DESC LIMIT 1")
    if last:
        new_item = f"{last['idComponents']} - {last['nameOfComponents']} - {last['cost']} - {last['manufacturer']}"
        languages_listbox_component.insert(END, new_item)

    entry2_viewOfJob_save.delete(0, END)
    entry3_viewOfJob_save.delete(0, END)
    entry4_viewOfJob_save.delete(0, END)

    messagebox.showinfo("Успешно", f"Комплектующее '{name}' сохранено успешно!")


label2_viewOfJob = ttk.Label(accessories, text="Название комплектующих")
label2_viewOfJob.pack(anchor=NW, padx=6, pady=6)

entry2_viewOfJob_save = ttk.Entry(accessories)
entry2_viewOfJob_save.pack(anchor=NW, padx=6, pady=6)

label3_viewOfJob = ttk.Label(accessories, text="Производитель")
label3_viewOfJob.pack(anchor=NW, padx=6, pady=6)

entry3_viewOfJob_save = ttk.Entry(accessories)
entry3_viewOfJob_save.pack(anchor=NW, padx=6, pady=6)

label4_viewOfJob = ttk.Label(accessories, text="Стоимость комплектующих")
label4_viewOfJob.pack(anchor=NW, padx=6, pady=6)

entry4_viewOfJob_save = ttk.Entry(accessories)
entry4_viewOfJob_save.pack(anchor=NW, padx=6, pady=6)

btn = ttk.Button(accessories, text="Сохранить", command=accessories_save)
btn.pack(anchor=NW, padx=6, pady=6)

# ----------------------------
#  Заказы + отчет
# -----------------------------

yesToOrder = ""
done = ""
payment = ""
took_order = ""
result_order = []
current_selected_client_text = ""
current_selected_master_id = ""
current_order_id = None
selected_order = []
initial_job_selection_msg = ""

# Инициализация списка работ
rows = db.fetchall("SELECT id_viewOfJob, nameOfViewJob, cost FROM listOfJob")
listofjob_Name = []
for i in rows:
    listofjob_Name.append(f"{i['id_viewOfJob']} - {i['nameOfViewJob']} - {i['cost']}")
languages_var = Variable(value=listofjob_Name)


def get_job_details(order_id):
    sql_select_viewofjob = "SELECT id_view FROM viewOfJob WHERE ordersForDiagnostics_id = ?"
    rows = db.fetchall(sql_select_viewofjob, (order_id,))
    all_select_sql = []
    for row in rows:
        job_id = row['id_view']
        result_sql = db.fetchone("SELECT id_viewOfJob, nameOfViewJob, cost FROM listOfJob WHERE id_viewOfJob = ?", (job_id,))
        if result_sql:
            all_select_sql.append(f"{result_sql['id_viewOfJob']} - {result_sql['nameOfViewJob']} - {result_sql['cost']}")
    return all_select_sql


def order_client(event):
    global yesToOrder, done, payment, took_order
    global result_order, current_selected_client_text, current_selected_master_id, current_order_id
    global selected_order, initial_job_selection_msg

    delete()

    current_selected_client_text = languages_var_client.get().strip()
    if not current_selected_client_text:
        return

    try:
        client_id_val = int(current_selected_client_text.split(" - ")[0])
    except ValueError:
        messagebox.showerror("Ошибка", "Ошибка форматирования ID клиента.")
        return

    sql1 = ("SELECT ordersForDiagnostics_id, yesOrNot, doneNotDone, payment, gotARepairOrder, master_id "
            "FROM ordersForDiagnostics WHERE client_id = ? ORDER BY ordersForDiagnostics_id DESC LIMIT 1")
    result_order = db.fetchone(sql1, (client_id_val,))

    if not result_order:
        messagebox.showinfo("Информация", "Для данного клиента нет заказов на диагностику.")
        selection_label["text"] = "Нет активных работ."
        return

    current_order_id = result_order['ordersForDiagnostics_id']
    yesToOrder = result_order['yesOrNot']
    done = result_order['doneNotDone']
    payment = result_order['payment']
    took_order = result_order['gotARepairOrder']
    current_selected_master_id = result_order['master_id']

    yesToOrder_client()
    done_client()
    payment_client()
    took_client()

    initial_jobs = get_job_details(current_order_id)
    initial_job_selection_msg = f"Уже выбрано: \n{', \n'.join(initial_jobs)}"
    selection_label["text"] = initial_job_selection_msg
    selected_order.clear()
    languages_listbox_job.selection_clear(0, END)

    reported()


def order_save():
    global yesToOrder, done, payment, took_order, current_order_id
    if not current_order_id:
        messagebox.showerror("Ошибка", "Сначала выберите клиента для загрузки заказа.")
        return

    sql = ("UPDATE ordersForDiagnostics SET yesOrNot = ?, doneNotDone = ?, payment = ?, gotARepairOrder = ? "
           "WHERE ordersForDiagnostics_id = ?")
    val = (yesToOrder, done, payment, took_order, current_order_id)
    db.execute(sql, val)
    db.commit()

    for i in selected_order:
        try:
            job_id = int(i.split(" - ")[0])
        except ValueError:
            print(f"Пропуск некорректного элемента: {i}")
            continue

        sql = "INSERT INTO viewOfJob (ordersForDiagnostics_id, id_view) VALUES (?, ?)"
        db.execute(sql, (current_order_id, job_id))
        db.commit()

    messagebox.showinfo("Успешно", "Данные заказа успешно обновлены!")
    order_client(None)


label2 = ttk.Label(order, text="Выбрать клиента")
label2.pack(anchor=NW, padx=6, pady=6)

languages_var_client = StringVar(value=client_Name[0] if client_Name else '')

label2l = ttk.Label(order, text="Выбранный клиент:", textvariable=languages_var_client)
label2l.pack(anchor=NW, padx=6, pady=6)

combobox_order = ttk.Combobox(order, textvariable=languages_var_client, values=client_Name, width=40)
combobox_order.pack(anchor=NW, padx=6, pady=6)
combobox_order.bind("<<ComboboxSelected>>", order_client)


def selected(event):
    global selected_order, initial_job_selection_msg
    selected_indices = languages_listbox_job.curselection()
    selected_order = [languages_listbox_job.get(i) for i in selected_indices]
    msg_new = f"\nНОВЫЕ ВЫБРАННЫЕ РАБОТЫ: \n{', \n'.join(selected_order)}" if selected_order else ""
    selection_label["text"] = initial_job_selection_msg + msg_new

selection_label = ttk.Label(order, text="Выберите клиента для загрузки заказа.")
selection_label.pack(anchor=NW, fill=X, padx=5, pady=5)

languages_listbox_job = Listbox(order, listvariable=languages_var, selectmode=EXTENDED, height=6)
languages_listbox_job.pack(anchor=NW, fill=X, padx=5, pady=5)
languages_listbox_job.bind("<<ListboxSelect>>", selected)

# ---------
# Чекбоксы
# ----------


def on_checkbox_clicked1():
    global yesToOrder
    yesToOrder = "true" if chk_state1.get() else "false"


def yesToOrder_client():
    if 'chk_state1' not in globals(): return
    chk_state1.set(yesToOrder == "true")
    checkbox1.pack(anchor=NW, padx=6, pady=6)


chk_state1 = IntVar(value=0)
checkbox1 = ttk.Checkbutton(order, text='Согласие на проведение работ', variable=chk_state1,
                            command=on_checkbox_clicked1)
checkbox1.pack_forget()


def on_checkbox_clicked2():
    global done
    done = "true" if chk_state2.get() else "false"


def done_client():
    if 'chk_state2' not in globals(): return
    chk_state2.set(done == "true")
    checkbox2.pack(anchor=NW, padx=6, pady=6)


chk_state2 = IntVar(value=0)
checkbox2 = ttk.Checkbutton(order, text='Выполнена работа', variable=chk_state2, command=on_checkbox_clicked2)
checkbox2.pack_forget()


def on_checkbox_clicked3():
    global payment
    payment = "true" if chk_state3.get() else "false"


def payment_client():
    if 'chk_state3' not in globals(): return
    chk_state3.set(payment == "true")
    checkbox3.pack(anchor=NW, padx=6, pady=6)


chk_state3 = IntVar(value=0)
checkbox3 = ttk.Checkbutton(order, text='Оплачено', variable=chk_state3, command=on_checkbox_clicked3)
checkbox3.pack_forget()


def on_checkbox_clicked4():
    global took_order
    took_order = "true" if chk_state4.get() else "false"


def took_client():
    if 'chk_state4' not in globals(): return
    chk_state4.set(took_order == "true")
    checkbox4.pack(anchor=NW, padx=6, pady=6)


chk_state4 = IntVar(value=0)
checkbox4 = ttk.Checkbutton(order, text='Клиент получил свой заказ', variable=chk_state4, command=on_checkbox_clicked4)
checkbox4.pack_forget()

btn = ttk.Button(order, text="Сохранить", command=order_save)
btn.pack(anchor=NW, padx=6, pady=6)

# -----
# Отчет
# -----

client_order = ttk.Label(report_work)
label_client = ttk.Label(report_work)
master_order = ttk.Label(report_work)
label_master1 = ttk.Label(report_work)
report_frame = tk.Frame(report_work)
job_frame = ttk.Label(report_work)
label_order = ttk.Label(report_work)
label_component = ttk.Label(report_work)
label_areal_cost = ttk.Label(report_work)
tree = ttk.Treeview(report_work)
label_choose_yesToOrder = ttk.Label(report_work)
label_choose_done = ttk.Label(report_work)
label_choose_payment = ttk.Label(report_work)
label_choose_took_order = ttk.Label(report_work)


def delete():
    for widget in report_work.winfo_children():
        widget.destroy()
    global client_order, label_client, master_order, label_master1, report_frame, tree
    global label_choose_yesToOrder, label_choose_done, label_choose_payment, label_choose_took_order
    client_order = ttk.Label(report_work)
    label_client = ttk.Label(report_work)
    master_order = ttk.Label(report_work)
    label_master1 = ttk.Label(report_work)
    report_frame = tk.Frame(report_work)
    tree = ttk.Treeview(report_work)
    label_choose_yesToOrder = ttk.Label(report_work)
    label_choose_done = ttk.Label(report_work)
    label_choose_payment = ttk.Label(report_work)
    label_choose_took_order = ttk.Label(report_work)


def reported():
    global client_order, label_client, master_order, label_master1, report_frame, tree
    global current_selected_client_text, current_selected_master_id, current_order_id
    global yesToOrder, done, payment, took_order
    global label_choose_yesToOrder, label_choose_done, label_choose_payment, label_choose_took_order

    if not current_order_id:
        ttk.Label(report_work, text="Выберите клиента во вкладке 'Заказ' для генерации отчета.").pack(padx=10, pady=10)
        return

    client_order = ttk.Label(report_work, text="Выбранный клиент: ")
    client_order.pack(anchor=tk.NW, padx=6, pady=6)

    label_client = ttk.Label(report_work, text=current_selected_client_text)
    label_client.pack(anchor=tk.NW, padx=6, pady=6)

    sql = "SELECT fullName FROM masters WHERE id = ?"
    master = db.fetchone(sql, (current_selected_master_id,))
    master_name = master['fullName'] if master else "Н/Д"

    master_order = ttk.Label(report_work, text="Прикрепленный мастер к заказу: ")
    master_order.pack(anchor=tk.NW, padx=6, pady=6)

    label_master1 = ttk.Label(report_work, text=f"{current_selected_master_id} - {master_name}")
    label_master1.pack(anchor=tk.NW, padx=6, pady=6)

    report_frame = tk.Frame(report_work, bg="white", bd=1, relief=tk.SOLID)
    report_frame.pack(fill=tk.BOTH, padx=10, pady=10)

    columns = ("name_of_job", "cost")
    tree = ttk.Treeview(report_frame, columns=columns, show="headings")
    tree.pack(fill=BOTH, expand=1)

    tree.heading("name_of_job", text="Название работ и комплектующих")
    tree.heading("cost", text="Стоимость (Руб.)")
    tree.column("cost", anchor='e', stretch=NO, width=120)

    sql_select_viewofjob = "SELECT id_view FROM viewOfJob WHERE ordersForDiagnostics_id = ?"
    result_job_ids = db.fetchall(sql_select_viewofjob, (current_order_id,))

    total_cost = 0

    for job_id_tuple in result_job_ids:
        job_id = job_id_tuple['id_view']
        sql_job = "SELECT id_viewOfJob, nameOfViewJob, cost FROM listOfJob WHERE id_viewOfJob = ?"
        result_job_info = db.fetchone(sql_job, (job_id,))
        if not result_job_info:
            continue

        job_cost = result_job_info['cost']
        areal_cost = job_cost
        job_name_display = f"{result_job_info['id_viewOfJob']} - {result_job_info['nameOfViewJob']}"
        tree.insert("", END, values=[job_name_display, str(job_cost)], tags=['job_title'])

        sql_comp_ids = "SELECT idComponents FROM components WHERE idListOfJob = ?"
        comp_id_list = db.fetchall(sql_comp_ids, (job_id,))

        for comp_id_tuple in comp_id_list:
            comp_id = comp_id_tuple['idComponents']
            sql_component = "SELECT idComponents, nameOfComponents, cost, manufacturer FROM listComponents WHERE idComponents = ?"
            result_component = db.fetchone(sql_component, (comp_id,))
            if result_component:
                comp_name_display = f"        {result_component['nameOfComponents']} ({result_component['manufacturer']})"
                comp_cost = result_component['cost']
                tree.insert("", END, values=[comp_name_display, str(comp_cost)], tags=['component'])
                areal_cost += comp_cost

        tree.insert("", END, values=["Итого по работе:", str(areal_cost)], tags=['subtotal'])
        total_cost += areal_cost

    tree.insert("", END, values=["ОБЩАЯ СТОИМОСТЬ ЗАКАЗА:", str(total_cost)], tags=['total'])

    tree.tag_configure('job_title', background='lightgray', font=('Arial', 10, 'bold'))
    tree.tag_configure('component', background='whitesmoke')
    tree.tag_configure('subtotal', background='lightpink', font=('Arial', 10, 'bold'))
    tree.tag_configure('total', background='cyan', font=('Arial', 11, 'bold'))

    if yesToOrder == "true":
        label_choose_yesToOrder = ttk.Label(report_work, text=" Клиент согласился на ремонт", bootstyle='success',
                                            font=("Arial", 10, "bold"))
    else:
        label_choose_yesToOrder = ttk.Label(report_work, text=" Клиент не согласился на ремонт", bootstyle='danger',
                                            font=("Arial", 10, "bold"))
    label_choose_yesToOrder.pack(anchor=tk.NW, padx=6, pady=6)

    if done == "true":
        label_choose_done = ttk.Label(report_work, text=" Ремонт завершён", bootstyle='success',
                                      font=("Arial", 10, "bold"))
    else:
        label_choose_done = ttk.Label(report_work, text=" Ремонт не завершён", bootstyle='warning',
                                      font=("Arial", 10, "bold"))
    label_choose_done.pack(anchor=tk.NW, padx=6, pady=6)

    if payment == "true":
        label_choose_payment = ttk.Label(report_work, text=" Клиент оплатил свой заказ", bootstyle='success',
                                         font=("Arial", 10, "bold"))
    else:
        label_choose_payment = ttk.Label(report_work, text=" Клиент не оплатил свой заказ", bootstyle='warning',
                                         font=("Arial", 10, "bold"))
    label_choose_payment.pack(anchor=tk.NW, padx=6, pady=6)

    if took_order == "true":
        label_choose_took_order = ttk.Label(report_work, text=" Клиент забрал свой заказ", bootstyle='success',
                                            font=("Arial", 10, "bold"))
    else:
        label_choose_took_order = ttk.Label(report_work, text=" Клиент не забрал свой заказ", bootstyle='warning',
                                            font=("Arial", 10, "bold"))
    label_choose_took_order.pack(anchor=tk.NW, padx=6, pady=6)


# Обновление списков при старте
update_client_lists()
update_master_lists()
update_listbox_component()
update_listbox_job()

root.mainloop()

db.close()


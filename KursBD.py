import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg
import subprocess
import time
import os
from PIL import Image, ImageTk

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Просмотр базы данных")
        self.root.geometry("1474x600")
        root.configure(bg="green")  # Установка цвета фона окна

        self.frame_controls = tk.Frame(self.root)
        self.frame_controls.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.frame_table = tk.Frame(self.root)
        self.frame_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.label_table = tk.Label(self.frame_controls, text="Выберите таблицу:")
        self.label_table.pack(side=tk.LEFT, padx=5)

        self.tables = [
            "ВариантРасписания",
            "ЖелезнаяДорога",
            "КалендарьДвиженияПоездов",
            "Маршрут",
            "Перевозчик",
            "Поезд",
            "СправочникСтанций",
            "СтанцияНаМаршруте"
        ]

        self.table_var = tk.StringVar(value=self.tables[0])
        self.table_menu = ttk.Combobox(self.frame_controls, textvariable=self.table_var, values=self.tables, state="readonly")
        self.table_menu.pack(side=tk.LEFT, padx=5)

        button_width = 13  # Задаём ширину кнопок

        self.button_load = tk.Button(self.frame_controls, text="Загрузить",  command=self.load_table, width=button_width)
        self.button_load.pack(side=tk.LEFT)

        self.button_edit = tk.Button(self.frame_controls, text="Редактировать", command=self.edit_record, width=button_width)
        self.button_edit.pack(side=tk.LEFT)

        self.button_delete = tk.Button(self.frame_controls, text="Удалить", command=self.delete_record, width=button_width)
        self.button_delete.pack(side=tk.LEFT)

        self.button_add = tk.Button(self.frame_controls, text="Добавить", command=self.add_record, width=button_width)
        self.button_add.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 1
        self.button_custom_query1 = tk.Button(self.frame_controls, text="1", command=self.display_custom_query_data1, width=5)
        self.button_custom_query1.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 2
        self.button_custom_query2 = tk.Button(self.frame_controls, text="2", command=self.open_query2_window, width=5)
        self.button_custom_query2.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 3
        self.button_custom_query3 = tk.Button(self.frame_controls, text="3", command=self.display_custom_query_data3, width=5)
        self.button_custom_query3.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 4
        self.button_custom_query4 = tk.Button(self.frame_controls, text="4", command=self.display_custom_query_data4, width=5)
        self.button_custom_query4.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 5
        self.button_custom_query5 = tk.Button(self.frame_controls, text="5", command=self.open_query5_window, width=5)
        self.button_custom_query5.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 6
        self.button_custom_query6 = tk.Button(self.frame_controls, text="6", command=self.open_query6_window, width=5)
        self.button_custom_query6.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 7
        self.button_custom_query7 = tk.Button(self.frame_controls, text="7", command=self.open_query7_window, width=5)
        self.button_custom_query7.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 8
        self.button_custom_query8 = tk.Button(self.frame_controls, text="8", command=self.open_query8_window, width=5)
        self.button_custom_query8.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 9
        self.button_custom_query9 = tk.Button(self.frame_controls, text="9", command=self.display_custom_query_data9, width=5)
        self.button_custom_query9.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 10
        self.button_custom_query10 = tk.Button(self.frame_controls, text="10", command=self.open_query10_window, width=5)
        self.button_custom_query10.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 11
        self.button_custom_query11 = tk.Button(self.frame_controls, text="11", command=self.open_query11_window, width=5)
        self.button_custom_query11.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 12
        self.button_custom_query12 = tk.Button(self.frame_controls, text="12", command=self.open_query12_window, width=5)
        self.button_custom_query12.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 13
        self.button_custom_query13 = tk.Button(self.frame_controls, text="13", command=self.open_query13_window, width=5)
        self.button_custom_query13.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 14
        self.button_custom_query14 = tk.Button(self.frame_controls, text="14", command=self.open_query14_window, width=5)
        self.button_custom_query14.pack(side=tk.LEFT)

        # Кнопка для выполнения запроса 14
        self.button_custom_query15 = tk.Button(self.frame_controls, text="15", command=self.execute_custom_query_from_file, width=5)
        self.button_custom_query15.pack(side=tk.LEFT)

        # Кнопка для выполнения информации
        self.info_button = tk.Button(self.frame_controls, text="Информация",command=self.show_info_window, width=button_width)
        self.info_button.pack(side=tk.LEFT)

    def connect_to_db(self):
        try:
            conn = psycopg.connect(
                dbname="BDNew",
                user="postgres",
                password="12345",
                host="localhost",
                port="5432"
            )
            return conn
        except psycopg.Error as e:
            messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных: {e}")
            return None

    def load_table_data(self, table_name):
        conn = self.connect_to_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM public.\"{table_name}\"")
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            return colnames, rows
        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные из таблицы {table_name}: {e}")
            return None, None
        finally:
            conn.close()

    def display_data(self, table_name):
        columns, rows = self.load_table_data(table_name)
        if columns is None or rows is None:
            return

        self.clear_table_frame()
        self.current_table = ttk.Treeview(self.frame_table, columns=columns, show="headings")
        self.current_table.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            self.current_table.heading(col, text=col)
            self.current_table.column(col, width=150, anchor = "center")

        for row in rows:
            self.current_table.insert("", tk.END, values=row)

        self.current_columns = columns  # Сохраняем список колонок

    def load_table(self):
        table_name = self.table_var.get()
        self.display_data(table_name)

    def edit_record(self):
        if not self.current_table or not self.current_table.selection():
            messagebox.showwarning("Выбор записи", "Пожалуйста, выберите запись для редактирования.")
            return

        selected_item = self.current_table.selection()[0]  # Получаем выбранный элемент
        record = self.current_table.item(selected_item)["values"]

        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Редактировать запись")

        entries = []
        for i, value in enumerate(record):
            label = tk.Label(edit_window, text=self.current_columns[i])
            label.grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)

        def save_record():
            new_values = [entry.get() for entry in entries]
            set_clause = ", ".join([f"{col} = %s" for col in self.current_columns])  # Обновляем все столбцы
            params = new_values + [record[0]]  # Добавляем первичный ключ в конец параметров

            try:
                conn = self.connect_to_db()
                if not conn:
                    return
                cursor = conn.cursor()
                query = f"UPDATE public.\"{self.table_var.get()}\" SET {set_clause} WHERE {self.current_columns[0]} = %s"
                cursor.execute(query, params)
                conn.commit()
                messagebox.showinfo("Успех", "Запись обновлена успешно")
                conn.close()
                edit_window.destroy()
                self.display_data(self.table_var.get())  # Перезагружаем данные после изменения
            except psycopg.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить запись: {e}")

        save_button = tk.Button(edit_window, text="Сохранить", command=save_record)
        save_button.grid(row=len(record), column=0, columnspan=2, pady=10)

    def delete_record(self):
        if not self.current_table or not self.current_table.selection():
            messagebox.showwarning("Выбор записи", "Пожалуйста, выберите запись для удаления.")
            return

        selected_item = self.current_table.selection()[0]
        record = self.current_table.item(selected_item)["values"]
        record_id = record[0]

        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить запись с ID {record_id}?")
        if confirm:
            try:
                conn = self.connect_to_db()
                if not conn:
                    return
                cursor = conn.cursor()
                query = f"DELETE FROM public.\"{self.table_var.get()}\" WHERE {self.current_columns[0]} = %s"
                cursor.execute(query, (record_id,))
                conn.commit()
                messagebox.showinfo("Успех", "Запись удалена успешно")
                conn.close()
                self.display_data(self.table_var.get())  # Перезагружаем данные после удаления
            except psycopg.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить запись: {e}")

    def add_record(self):
        if not self.current_columns:
            messagebox.showwarning("Ошибка", "Таблица не загружена. Пожалуйста, загрузите таблицу.")
            return

        add_window = tk.Toplevel(self.root)
        add_window.title(f"Добавить запись")

        entries = []
        for col in self.current_columns:
            label = tk.Label(add_window, text=col)
            label.grid(row=len(entries), column=0, padx=5, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=len(entries), column=1, padx=5, pady=5)
            entries.append(entry)

        def save_new_record():
            new_values = [entry.get() for entry in entries]
            placeholders = ", ".join(["%s"] * len(self.current_columns))
            query = f"INSERT INTO public.\"{self.table_var.get()}\" ({', '.join(self.current_columns)}) VALUES ({placeholders})"

            try:
                conn = self.connect_to_db()
                if not conn:
                    return
                cursor = conn.cursor()
                cursor.execute(query, new_values)
                conn.commit()
                messagebox.showinfo("Успех", "Запись добавлена успешно")
                conn.close()
                add_window.destroy()
                self.display_data(self.table_var.get())  # Перезагружаем данные после добавления
            except psycopg.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить запись: {e}")

        save_button = tk.Button(add_window, text="Добавить", command=save_new_record)
        save_button.grid(row=len(self.current_columns), column=0, columnspan=2, pady=10)

    def clear_table_frame(self):
        for widget in self.frame_table.winfo_children():
            widget.destroy()

    def display_custom_query_data1(self):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT "НазваниеСтанции", "ТипСтанции", "ЖелезнаяДорога"
        FROM public."СправочникСтанций"
        WHERE "ТипСтанции" = 'Платформа' AND "ЖелезнаяДорога" = 17;
        """

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def open_query2_window(self):
        query2_window = tk.Toplevel(self.root)
        query2_window.title("Введите код маршрута")

        label = tk.Label(query2_window, text="Введите код маршрута:")
        label.pack(padx=10, pady=10)

        entry = tk.Entry(query2_window)
        entry.pack(padx=10, pady=10)

        def execute_query():
            route_code = entry.get().strip()
            if not route_code.isdigit():
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректный код маршрута.")
                return

            # Передаем код маршрута в метод display_custom_query_data2
            self.display_custom_query_data2(route_code)
            query2_window.destroy()

        button = tk.Button(query2_window, text="Ввести", command=execute_query)
        button.pack(padx=10, pady=10)

    def display_custom_query_data2(self, route_code):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT s."НазваниеСтанции", m."КодМаршрута"
        FROM public."СправочникСтанций" s
        JOIN public."СтанцияНаМаршруте" sn ON s."КодСтанции" = sn."КодСтанции"
        JOIN public."Маршрут" m ON sn."ВариантРасписания" = m."ВариантРасписания"
        WHERE m."КодМаршрута" = %s;
        """

        try:
            cursor = conn.cursor()
            cursor.execute(query, (route_code,))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def display_custom_query_data3(self):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT 
            s."НазваниеСтанции", 
        COUNT(*) AS "Количество"
        FROM 
        public."СправочникСтанций" s
        JOIN 
        public."ЖелезнаяДорога" j ON s."ЖелезнаяДорога" = j."КодЖелезнойДороги"
        WHERE 
        j."ПолноеНазвание" LIKE '%Московская железная дорога%'  -- Фильтруем по названию железной дороги
        GROUP BY 
        s."НазваниеСтанции"
        HAVING 
            COUNT(*) > 1;  -- Выбираем только те станции, которые встречаются более одного раза
        """

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def display_custom_query_data4(self):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT 
            p."НомерПоезда",
            p."КатегорияПоезда",
            s."НазваниеСтанции" AS "НачальнаяСтанция",
            m."ВремяОтправления",
            m."ВремяПрибытия"
        FROM 
            public."Поезд" p
        JOIN 
            public."Маршрут" m ON p."Маршрут" = m."КодМаршрута"
        JOIN 
            public."СправочникСтанций" s ON m."НачальнаяСтанция" = s."КодСтанции"
        WHERE 
            p."НомерПоезда" % 2 = 0 -- Только четные номера поездов
        ORDER BY 
            p."НомерПоезда";
        """

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def open_query5_window(self):
        query5_window = tk.Toplevel(self.root)
        query5_window.title("Введите название станции:")

        label = tk.Label(query5_window, text="Введите название станции:")
        label.pack(padx=10, pady=10)

        entry = tk.Entry(query5_window)
        entry.pack(padx=10, pady=10)

        def execute_query():
            station_name = entry.get().strip()
            if not station_name:
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректный код маршрута.")
                return

            # Передаем код маршрута в метод display_custom_query_data2
            self.display_custom_query_data5(station_name)
            query5_window.destroy()

        button = tk.Button(query5_window, text="Ввести", command=execute_query)
        button.pack(padx=10, pady=10)

    def display_custom_query_data5(self, station_name):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT 
            p."НомерПоезда",                  
            p."КатегорияПоезда",              
            s."НазваниеСтанции",              
            snm."ВремяПрибытия",              
            snm."ВремяОтправления",    
            snm."ПризнакРазрешенияПосадкиВысадки"       
        FROM 
            public."Поезд" p                  
        JOIN 
            public."Маршрут" m                
            ON p."Маршрут" = m."КодМаршрута"  
        JOIN 
            public."СтанцияНаМаршруте" snm    
            ON m."ВариантРасписания" = snm."ВариантРасписания" 
        JOIN 
            public."СправочникСтанций" s      
            ON snm."КодСтанции" = s."КодСтанции" 
        WHERE 
            s."НазваниеСтанции" = %s         
            AND snm."ПризнакРазрешенияПосадкиВысадки" = TRUE 
        ORDER BY 
            p."НомерПоезда", snm."ВремяПрибытия";
        """

        try:
            cursor = conn.cursor()
            cursor.execute(query, (station_name,))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def open_query6_window(self):
        query6_window = tk.Toplevel(self.root)
        query6_window.title("Введите название станции:")

        label = tk.Label(query6_window, text="Введите название станции:")
        label.pack(padx=10, pady=10)

        entry = tk.Entry(query6_window)
        entry.pack(padx=10, pady=10)

        def execute_query():
            station_name1 = entry.get().strip()
            if not station_name1:
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректный код маршрута.")
                return

            # Передаем код маршрута в метод display_custom_query_data2
            self.display_custom_query_data6(station_name1)
            query6_window.destroy()

        button = tk.Button(query6_window, text="Ввести", command=execute_query)
        button.pack(padx=10, pady=10)

    def display_custom_query_data6(self, station_name1):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT 
            p."НомерПоезда",
            p."КатегорияПоезда",
            p."РегулярностьХождения",
            s."НазваниеСтанции",
            snm."ВремяПрибытия",
            snm."ВремяОтправления",
            snm."ПризнакТехническойОстановки",
            snm."ПризнакРазрешенияПосадкиВысадки"
        FROM 
            public."Поезд" p
        JOIN 
            public."Маршрут" m ON p."Маршрут" = m."КодМаршрута"
        JOIN 
            public."СтанцияНаМаршруте" snm ON m."ВариантРасписания" = snm."ВариантРасписания"
        JOIN 
            public."СправочникСтанций" s ON snm."КодСтанции" = s."КодСтанции"
        WHERE 
            s."НазваниеСтанции" = %s
            AND snm."ПризнакТехническойОстановки" = TRUE
            AND snm."ПризнакРазрешенияПосадкиВысадки" = FALSE;
        """

        try:
            cursor = conn.cursor()
            cursor.execute(query, (station_name1,))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def open_query7_window(self):
        query7_window = tk.Toplevel(self.root)  # Исправлено на query7_window
        query7_window.title("Введите коды начальной и конечной станций:")

        label = tk.Label(query7_window, text="Введите коды начальной и конечной станций:")
        label.pack(padx=10, pady=10)

        entry1 = tk.Entry(query7_window)
        entry1.pack(padx=10, pady=10)

        entry2 = tk.Entry(query7_window)
        entry2.pack(padx=10, pady=10)

        def execute_query():
            station_name1 = entry1.get().strip()
            station_name2 = entry2.get().strip()

            # Проверка на пустой ввод
            if not station_name1 or not station_name2:
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите начальную и конечную станции.")
                return

            # Передаем начальную и конечную станцию в метод display_custom_query_data7
            self.display_custom_query_data7(station_name1, station_name2)
            query7_window.destroy()

        button = tk.Button(query7_window, text="Ввести", command=execute_query)
        button.pack(padx=10, pady=10)

    def display_custom_query_data7(self, station_name1, station_name2):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT DISTINCT
            p."НомерПоезда",
            p."КатегорияПоезда",
            p."РегулярностьХождения",
            m."НачальнаяСтанция",
            m."КонечнаяСтанция"
        FROM 
            public."Поезд" p
        JOIN 
            public."Маршрут" m ON p."Маршрут" = m."КодМаршрута"
        WHERE 
            m."НачальнаяСтанция" = %s
            AND m."КонечнаяСтанция" = %s
        ORDER BY 
            p."НомерПоезда";
        """  # Исправлено на %s для обоих параметров

        try:
            cursor = conn.cursor()
            cursor.execute(query, (station_name1, station_name2))  # Все параметры передаем в одном кортеже
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def open_query8_window(self):
        # Создаем новое окно для ввода данных
        query8_window = tk.Toplevel(self.root)
        query8_window.title("Введите данные для поиска поездов:")

        # Место для ввода начальной станции
        label_station = tk.Label(query8_window, text="Введите название станции:")
        label_station.pack(padx=10, pady=5)

        entry_station = tk.Entry(query8_window)
        entry_station.pack(padx=10, pady=5)

        # Место для ввода даты
        label_date = tk.Label(query8_window, text="Введите год графика:")
        label_date.pack(padx=10, pady=5)

        entry_date = tk.Entry(query8_window)
        entry_date.pack(padx=10, pady=5)

        # Место для ввода времени начала и окончания
        label_time_start = tk.Label(query8_window, text="Введите время начала (YYYY-MM-DD HH:MM:SS):")
        label_time_start.pack(padx=10, pady=5)

        entry_time_start = tk.Entry(query8_window)
        entry_time_start.pack(padx=10, pady=5)

        label_time_end = tk.Label(query8_window, text="Введите время окончания (YYYY-MM-DD HH:MM:SS):")
        label_time_end.pack(padx=10, pady=5)

        entry_time_end = tk.Entry(query8_window)
        entry_time_end.pack(padx=10, pady=5)

        def execute_query():
            # Получаем данные из полей ввода
            station_name = entry_station.get().strip()
            date = entry_date.get().strip()
            time_start = entry_time_start.get().strip()
            time_end = entry_time_end.get().strip()

            # Проверяем корректность данных
            if not station_name:
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректную станцию.")
                return

            if not date.isdigit():
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректную дату (YYYY).")
                return

            if not time_start or not time_end:
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректное время.")
                return

            # Передаем данные в метод для выполнения запроса
            self.display_custom_query_data8(station_name, date, time_start, time_end)

            # Закрываем окно после выполнения запроса
            query8_window.destroy()

        # Кнопка для выполнения запроса
        button = tk.Button(query8_window, text="Показать поезда", command=execute_query)
        button.pack(padx=10, pady=10)

    def display_custom_query_data8(self, station_name, date, time_start, time_end):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT DISTINCT
            p."НомерПоезда",
            p."КатегорияПоезда",
            p."РегулярностьХождения",
            m."ВремяПрибытия",
            m."ВремяОтправления",
            cd."ГодГрафика",
            m."НачальнаяСтанция",
            m."КонечнаяСтанция"
        FROM 
            public."Поезд" p
        JOIN 
            public."Маршрут" m ON p."Маршрут" = m."КодМаршрута"
        JOIN 
            public."КалендарьДвиженияПоездов" cd ON p."ГодГрафика" = cd."ГодГрафика"
        JOIN 
            public."СправочникСтанций" s ON m."НачальнаяСтанция" = s."КодСтанции"
        WHERE 
            s."НазваниеСтанции" = %s
            AND cd."ГодГрафика" = %s
            AND m."ВремяПрибытия" BETWEEN %s AND %s
        ORDER BY 
            m."ВремяПрибытия";
        """

        try:
            cursor = conn.cursor()
            cursor.execute(query, (station_name, date, time_start, time_end))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def display_custom_query_data9(self):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT DISTINCT
            p."НомерПоезда",
            p."КатегорияПоезда",
            p."РегулярностьХождения",
            m."НачальнаяСтанция",
            m."КонечнаяСтанция",
            snm."ПризнакРазрешенияПосадкиВысадки"
        FROM 
            public."Поезд" p
        JOIN 
            public."Маршрут" m ON p."Маршрут" = m."КодМаршрута"
        JOIN 
            public."СтанцияНаМаршруте" snm ON m."ВариантРасписания" = snm."ВариантРасписания"
        WHERE 
            snm."ПризнакРазрешенияПосадкиВысадки" = TRUE
            AND NOT EXISTS (
                SELECT 1
                FROM public."СтанцияНаМаршруте" s
                WHERE s."ВариантРасписания" = snm."ВариантРасписания"
                  AND s."ПризнакРазрешенияПосадкиВысадки" = FALSE
            )
        ORDER BY 
            p."НомерПоезда";
        """

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def open_query10_window(self):
        query10_window = tk.Toplevel(self.root)  # Исправлено на query7_window
        query10_window.title("Введите коды начальной и конечной станций:")

        label = tk.Label(query10_window, text="Введите коды начальной и конечной станций:")
        label.pack(padx=10, pady=10)

        entry1 = tk.Entry(query10_window)
        entry1.pack(padx=10, pady=10)

        entry2 = tk.Entry(query10_window)
        entry2.pack(padx=10, pady=10)

        def execute_query():
            station_name1 = entry1.get().strip()
            station_name2 = entry2.get().strip()

            # Проверка на пустой ввод
            if not station_name1 or not station_name2:
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите начальную и конечную станции.")
                return

            # Передаем начальную и конечную станцию в метод display_custom_query_data7
            self.display_custom_query_data10(station_name1, station_name2)
            query10_window.destroy()

        button = tk.Button(query10_window, text="Ввести", command=execute_query)
        button.pack(padx=10, pady=10)

    def display_custom_query_data10(self, station_name1, station_name2):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT DISTINCT
            s."НазваниеСтанции" AS "Станция",
            p."НомерПоезда" AS "Номер поезда",
            p."КатегорияПоезда" AS "Категория поезда",
            sm."ВремяОтправления" AS "Время отправления"
        FROM 
            public."СтанцияНаМаршруте" sm
        JOIN 
            public."Маршрут" m ON sm."ВариантРасписания" = m."ВариантРасписания"
        JOIN 
            public."СправочникСтанций" s ON sm."КодСтанции" = s."КодСтанции"
        JOIN 
            public."Поезд" p ON p."Маршрут" = m."КодМаршрута"
        WHERE 
            m."НачальнаяСтанция" = (SELECT "КодСтанции" FROM public."СправочникСтанций" WHERE "КодСтанции" = %s)
            AND m."КонечнаяСтанция" = (SELECT "КодСтанции" FROM public."СправочникСтанций" WHERE "КодСтанции" = %s)
        ORDER BY 
            p."НомерПоезда", sm."ВремяОтправления";
        """  # Исправлено на %s для обоих параметров

        try:
            cursor = conn.cursor()
            cursor.execute(query, (station_name1, station_name2))  # Все параметры передаем в одном кортеже
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def open_query11_window(self):
        # Создаем новое окно для ввода данных
        query11_window = tk.Toplevel(self.root)
        query11_window.title("Введите данные для поиска поездов:")

        # Место для ввода начальной станции
        label_station1 = tk.Label(query11_window, text="Введите код начальной станции:")
        label_station1.pack(padx=10, pady=5)

        entry_station1 = tk.Entry(query11_window)
        entry_station1.pack(padx=10, pady=5)

        # Место для ввода начальной станции
        label_station2 = tk.Label(query11_window, text="Введите код конечной станции:")
        label_station2.pack(padx=10, pady=5)

        entry_station2 = tk.Entry(query11_window)
        entry_station2.pack(padx=10, pady=5)

        # Место для ввода времени начала и окончания
        label_time_start = tk.Label(query11_window, text="Введите время начала (YYYY-MM-DD HH:MM:SS):")
        label_time_start.pack(padx=10, pady=5)

        entry_time_start = tk.Entry(query11_window)
        entry_time_start.pack(padx=10, pady=5)

        label_time_end = tk.Label(query11_window, text="Введите время окончания (YYYY-MM-DD HH:MM:SS):")
        label_time_end.pack(padx=10, pady=5)

        entry_time_end = tk.Entry(query11_window)
        entry_time_end.pack(padx=10, pady=5)

        def execute_query():
            # Получаем данные из полей ввода
            station_name1 = entry_station1.get().strip()
            station_name2 = entry_station2.get().strip()
            time_start = entry_time_start.get().strip()
            time_end = entry_time_end.get().strip()

            # Проверяем корректность данных
            if not station_name1.isdigit():
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректную станцию.")
                return

            if not station_name2.isdigit():
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректную станцию.")
                return

            if not time_start or not time_end:
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректное время.")
                return

            # Передаем данные в метод для выполнения запроса
            self.display_custom_query_data11(station_name1, station_name2, time_start, time_end)

            # Закрываем окно после выполнения запроса
            query11_window.destroy()

        # Кнопка для выполнения запроса
        button = tk.Button(query11_window, text="Показать поезда", command=execute_query)
        button.pack(padx=10, pady=10)

    def display_custom_query_data11(self, station_name1, station_name2, time_start, time_end):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        SELECT 
            p."НомерПоезда" AS "Номер поезда",
            p."КатегорияПоезда" AS "Категория поезда",
            sm_start."ВремяОтправления" AS "Время отправления",
            sm_end."ВремяПрибытия" AS "Время прибытия",
            sm_start."ПройденныйКилометраж" AS "Километраж от А",
            sm_end."ПройденныйКилометраж" AS "Километраж до В"
        FROM 
            public."СтанцияНаМаршруте" sm_start
        JOIN 
            public."СтанцияНаМаршруте" sm_end ON sm_start."ВариантРасписания" = sm_end."ВариантРасписания"
        JOIN 
            public."Маршрут" m ON sm_start."ВариантРасписания" = m."ВариантРасписания"
        JOIN 
            public."Поезд" p ON p."Маршрут" = m."КодМаршрута"
        WHERE 
            sm_start."КодСтанции" = (SELECT "КодСтанции" FROM public."СправочникСтанций" WHERE "КодСтанции" = %s)
            AND sm_end."КодСтанции" = (SELECT "КодСтанции" FROM public."СправочникСтанций" WHERE "КодСтанции" = %s)
            AND sm_start."ПройденныйКилометраж" < sm_end."ПройденныйКилометраж"
            AND sm_start."ВремяОтправления" BETWEEN %s AND %s
        ORDER BY 
            sm_start."ВремяОтправления" ASC
        LIMIT 1;
        """

        try:
            cursor = conn.cursor()
            cursor.execute(query, (station_name1, station_name2, time_start, time_end))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def open_query12_window(self):
        query12_window = tk.Toplevel(self.root)  # Исправлено на query7_window
        query12_window.title("Введите тип станции и ее название:")

        label1 = tk.Label(query12_window, text="Введите новый тип станции:")
        label1.pack(padx=10, pady=10)

        entry1 = tk.Entry(query12_window)
        entry1.pack(padx=10, pady=10)

        label2 = tk.Label(query12_window, text="Введите название станции:")
        label2.pack(padx=10, pady=10)

        entry2 = tk.Entry(query12_window)
        entry2.pack(padx=10, pady=10)

        def execute_query():
            station_type = entry1.get().strip()
            station_name = entry2.get().strip()

            # Проверка на пустой ввод
            if not station_type or not station_name:
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите начальную и конечную станции.")
                return

            # Передаем начальную и конечную станцию в метод display_custom_query_data7
            self.display_custom_query_data12(station_type, station_name)
            query12_window.destroy()

        button = tk.Button(query12_window, text="Ввести", command=execute_query)
        button.pack(padx=10, pady=10)

    def display_custom_query_data12(self, station_type, station_name):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        UPDATE public."СправочникСтанций"
        SET "ТипСтанции" = %s
        WHERE "НазваниеСтанции" = %s
        RETURNING *;
        """  # Исправлено на %s для обоих параметров

        try:
            cursor = conn.cursor()
            cursor.execute(query, (station_type, station_name))  # Все параметры передаем в одном кортеже
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            # Фиксируем изменения в базе данных
            conn.commit()

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def open_query13_window(self):
        # Создаем новое окно для ввода данных
        query13_window = tk.Toplevel(self.root)
        query13_window.title("Введите данные для добавления нового перевозчика:")

        # Место для ввода начальной станции
        label_cod = tk.Label(query13_window, text="Введите код перевозчика:")
        label_cod.pack(padx=10, pady=5)

        entry_cod = tk.Entry(query13_window)
        entry_cod.pack(padx=10, pady=5)

        # Место для ввода начальной станции
        label_full_name = tk.Label(query13_window, text="Введите полное название:")
        label_full_name.pack(padx=10, pady=5)

        entry_full_name = tk.Entry(query13_window)
        entry_full_name.pack(padx=10, pady=5)

        # Место для ввода времени начала и окончания
        label_short_name = tk.Label(query13_window, text="Введите сокращенное название:")
        label_short_name.pack(padx=10, pady=5)

        entry_short_name = tk.Entry(query13_window)
        entry_short_name.pack(padx=10, pady=5)

        label_goverment = tk.Label(query13_window, text="Введите принадлежность государству:")
        label_goverment.pack(padx=10, pady=5)

        entry_goverment = tk.Entry(query13_window)
        entry_goverment.pack(padx=10, pady=5)

        def execute_query():
            # Получаем данные из полей ввода
            cod = entry_cod.get().strip()
            full_name = entry_full_name.get().strip()
            short_name = entry_short_name.get().strip()
            goverment = entry_goverment.get().strip()

            # Проверяем корректность данных
            if not cod.isdigit():
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректную станцию.")
                return

            if not full_name or not short_name:
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректное время.")
                return

            if not goverment:
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректную станцию.")
                return

            # Передаем данные в метод для выполнения запроса
            self.display_custom_query_data13(cod, full_name, short_name, goverment)

            # Закрываем окно после выполнения запроса
            query13_window.destroy()

        # Кнопка для выполнения запроса
        button = tk.Button(query13_window, text="Ввести", command=execute_query)
        button.pack(padx=10, pady=10)

    def display_custom_query_data13(self, cod, full_name, short_name, goverment):

        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        query = """
        INSERT INTO public."Перевозчик" ("КодПеревозчика", "ПолноеНазвание", "СокращенноеНазвание", "ПринадлежностьГосударству")
        VALUES (%s, %s, %s, %s)
        RETURNING *;
        """

        try:
            cursor = conn.cursor()
            cursor.execute(query, (cod, full_name, short_name, goverment))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            # Фиксируем изменения в базе данных
            conn.commit()

            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def open_query14_window(self):
        query14_window = tk.Toplevel(self.root)
        query14_window.title("Введите год графика:")

        label = tk.Label(query14_window, text="Введите год графика:")
        label.pack(padx=10, pady=10)

        entry = tk.Entry(query14_window)
        entry.pack(padx=10, pady=10)

        def execute_query():
            year = entry.get().strip()

            if not year.isdigit():
                messagebox.showwarning("Неверный ввод", "Пожалуйста, введите корректный год графика.")
                return

            # Передаем год графика в метод display_custom_query_data14
            self.display_custom_query_data14(year)
            query14_window.destroy()

        button = tk.Button(query14_window, text="Ввести", command=execute_query)
        button.pack(padx=10, pady=10)

    def display_custom_query_data14(self, year):
        self.clear_table_frame()

        conn = self.connect_to_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            # Удаляем записи из таблицы "Поезд"
            cursor.execute("""
            DELETE FROM public."Поезд"
            WHERE "ГодГрафика" = %s
            RETURNING *;
            """, (year,))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            # Удаляем записи из таблицы "КалендарьДвиженияПоездов"
            cursor.execute("""
            DELETE FROM public."КалендарьДвиженияПоездов"
            WHERE "ГодГрафика" = %s;
            """, (year,))

            # Фиксируем изменения в базе данных
            conn.commit()

            # Отображаем данные из удаленной таблицы "Поезд"
            tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", tk.END, values=row)

        except psycopg.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        finally:
            conn.close()

    def execute_custom_query_from_file(self):
        # Задаем фиксированный путь к файлу с SQL запросом
        file_path = "D:/BDfile.txt"  # Замените на нужный путь

        try:
            # Открытие файла в Notepad для редактирования
            process = subprocess.Popen(['notepad', file_path])

            # Ожидаем завершения процесса (закрытие Notepad)
            process.communicate()

            # После того как файл закрыт, считываем запрос
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    query = file.read().strip()

                # Если запрос не пуст, выполняем его
                if query:
                    self.execute_query(query)  # Выполнение запроса после закрытия файла

            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка при чтении файла: {e}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def execute_query(self, query):
        # Выполнение SQL запроса
        conn = self.connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                # Фиксируем изменения в базе данных
                conn.commit()

                self.clear_table_frame()

                tree = ttk.Treeview(self.frame_table, columns=columns, show="headings")
                tree.pack(fill=tk.BOTH, expand=True)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=150)

                for row in rows:
                    tree.insert("", tk.END, values=row)

            except psycopg.Error as e:
                messagebox.showerror("Ошибка выполнения запроса", f"Не удалось выполнить запрос: {e}")
            finally:
                conn.close()

    def show_info_window(self):
        # Создаем окно с информацией
        info_window = tk.Toplevel()
        info_window.title("Информация о кнопках")
        info_window.geometry("800x500")

        # Текст с информацией о кнопках
        info_text = (
            "Запросы программы:\n\n"
            "1. Выдать список наименований всех платформ (тип раздельного пункта - 7) Московской ж.д. (код дороги - 17)\n\n"
            "2. Выдать список наименований всех раздельных пунктов заданного варианта маршрута (по коду варианта)\n\n"
            "3. Выдать повторяющиеся имена раздельных пунктов на Московской дороге\n\n"
            "4. Выдать список всех поездов заданного направления (четность номера поезда) и начальной станции отправления поезда\n\n"
            "5. Выдать список всех поездов, останавливающихся для посадки/высадки пассажиров на заданной станции A\n\n"
            "6. Выдать список всех поездов, делающих техническую остановку (без посадки/высадки пассажиров) на заданной станции A\n\n"
            "7. Выдать список поездов, на которых можно проехать от станции А до станции B\n\n"
            "8. Выдать список поездов, прибывающих на станцию А, в заданном направлении в промежутке времени [t1, t2] в заданную дату\n\n"
            "9. Выдать поезда, которые следуют со всеми остановками для посадки/высадки\n\n"
            "10. Выдать расписание поездов для заданного маршрута\n\n"
            "11. Поиск оптимального по времени поезда, следующего от станции А к станции В в заданном промежутке времени [t1, t2]\n\n"
            "12. Изменить тип станции в классификаторе станций\n\n"
            "13. Добавить нового перевозчика\n\n"
            "14. Удалить из БД расписания всю устаревшую информацию прошедшего графика (по году графика)\n\n"
            "15. Пользовательский запрос\n"
        )

        # Вывод текста в окно
        info_label = tk.Label(info_window, text=info_text, justify=tk.LEFT, wraplength=750, anchor="nw")
        info_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Основная часть программы
if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
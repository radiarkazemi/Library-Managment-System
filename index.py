from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import mysql.connector
from xlrd import *
from xlsxwriter import *

from PyQt5.uic import loadUiType
import datetime
import database as database_db

ui, _ = loadUiType("library.ui")
login, _ = loadUiType("login.ui")


class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.login_pushButton.clicked.connect(self.handel_login)
        self.signup_pushButton.clicked.connect(self.add_new_user)
        style = open('themes/dark_orange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def add_new_user(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        user_name = self.username_signup_lineEdit.text()
        email = self.email_signup_lineEdit.text()
        password = self.password_signup_lineEdit.text()
        confirm_password = self.password_confirm_signup_lineEdit.text()

        if password == confirm_password:
            self.cur.execute('''
                INSERT INTO users(user_name , user_email , user_password)
                VALUES (%s , %s , %s)
            ''', (user_name, email, password))
            self.db.commit()
            MainApp.message_box(self, 'User Added!')
        else:
            self.wrong_password_label.setText('The Passwords Are Not Match!')

    def handel_login(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        username = self.user_name_lineEdit.text()
        password = self.password_lineEdit.text()

        sql = '''SELECT * FROM users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                MainApp.message_box(self, 'You Are In')
                self.window2 = MainApp()
                self.close()
                self.window2.show()
            else:
                self.sure_label.setText('Make Sure You Enter Your Username And Password Correctly')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.dark_orange_theme()
        self.handel_ui_changes()
        self.handel_buttons()
        self.create_database()

        self.show_category()
        self.show_author()
        self.show_publisher()

        self.show_categorise_combo()
        self.show_authors_combo()
        self.show_publishers_combo()

        self.show_all_books()
        self.show_all_client()
        self.show_all_operations()

        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.resizeColumnsToContents()

        self.all_books_tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.all_books_tableWidget.resizeColumnsToContents()

        self.all_clients_tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.all_clients_tableWidget.resizeColumnsToContents()

        self.tableWidget_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_2.resizeColumnsToContents()

        self.tableWidget_3.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_3.resizeColumnsToContents()

        self.tableWidget_4.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_4.resizeColumnsToContents()

    def handel_ui_changes(self):
        self.hiding_themes()
        self.tabWidget.tabBar().setVisible(False)

    def handel_buttons(self):
        self.themes_pushButton.clicked.connect(self.show_themes)
        self.hide_themes_pushButton.clicked.connect(self.hiding_themes)

        self.add_pushButton.clicked.connect(self.handel_day_operations)

        self.day_to_day_pushButton.clicked.connect(self.open_day_to_day_tab)
        self.books_pushButton.clicked.connect(self.open_book_tab)
        self.client_pushButton.clicked.connect(self.open_client_tab)
        self.users_pushButton.clicked.connect(self.open_users_tab)

        self.settings_pushButton.clicked.connect(self.open_setting_tab)
        self.save_pushButton.clicked.connect(self.add_new_book)
        self.add_new_category_pushButton.clicked.connect(self.add_category)
        self.add_new_author_pushButton.clicked.connect(self.add_author)
        self.add_new_publisher_pushButton.clicked.connect(self.add_publisher)

        self.search_pushButton.clicked.connect(self.search_books)
        self.save_pushButton_Edit.clicked.connect(self.edit_books)
        self.delete_pushButton.clicked.connect(self.delete_books)

        self.addUser_pushButton.clicked.connect(self.add_new_user)
        self.login_pushButton_Edit.clicked.connect(self.login)
        self.esitUser_pushButton.clicked.connect(self.edit_user)

        self.dark_blue_pushButton.clicked.connect(self.dark_blue_theme)
        self.dark_gray_pushButton.clicked.connect(self.dark_gray_theme)
        self.dark_orange_pushButton.clicked.connect(self.dark_orange_theme)
        self.qdark_pushButton.clicked.connect(self.qdark_theme)

        self.add_new_client_pushButton.clicked.connect(self.add_new_client)
        self.search_client_pushButton.clicked.connect(self.search_client)
        self.save_client_pushButton_Edit.clicked.connect(self.edit_client)
        self.delete_client_pushButton.clicked.connect(self.delete_client)

        self.export_operation_pushButton.clicked.connect(self.export_day_operations)
        self.expor_book_pushButton.clicked.connect(self.export_books)
        self.export_clients_pushButton_2.clicked.connect(self.export_clients)

    def show_themes(self):
        self.themes_groupBox.show()

    def hiding_themes(self):
        self.themes_groupBox.hide()

    def create_database(self):
        database_db

    # =============================================opening tabs================================================

    def open_day_to_day_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_book_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_client_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def open_setting_tab(self):
        self.tabWidget.setCurrentIndex(4)

    # ============================================= Day Operations========================================
    def handel_day_operations(self):
        book_title = self.bookName_lineEdit.text()
        client = self.clientName_lineEdit.text()
        operation_type = self.type_comboBox.currentText()
        days_number = self.days_comboBox.currentIndex() + 1
        today_date = datetime.date.today()
        to_day = today_date + datetime.timedelta(days=days_number)

        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO dayoperations(book_code , client_national_id , type , days , date , to_date)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (book_title, client, operation_type, days_number, today_date, to_day))

        self.db.commit()
        self.message_box('New Operation Added!')
        self.show_all_operations()

    def show_all_operations(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''
            SELECT book.book_name ,dayoperations.book_code , clients.client_name ,
            dayoperations.client_national_id , dayoperations.type ,
            dayoperations.date , dayoperations.to_date
            FROM library_b.dayoperations 
            join library_b.clients 
            on library_b.dayoperations.client_national_id = library_b.clients.client_national_id
            join library_b.book 
            on library_b.dayoperations.book_code = library_b.book.book_code
        ''')
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    # ============================================= books ================================================

    def show_all_books(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute(
            '''SELECT book_code,book_name,book_description,book_category,book_author,book_publisher,book_price FROM book''')
        data = self.cur.fetchall()

        self.all_books_tableWidget.setRowCount(0)
        self.all_books_tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.all_books_tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.all_books_tableWidget.rowCount()
            self.all_books_tableWidget.insertRow(row_position)
        self.db.close()

    def add_new_book(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        book_title = self.bookTitle_lineEdit.text()
        book_description = self.description_textEdit.toPlainText()
        book_code = self.bookCode_lineEdit.text()
        book_category = self.category_comboBox.currentText()
        book_author = self.author_comboBox.currentText()
        book_publisher = self.publisher_comboBox.currentText()
        book_price = self.bookPrice_lineEdit.text()

        self.cur.execute('''
            INSERT INTO book(book_name,book_description,book_code,book_category,book_author,book_publisher,book_price)
            VALUES (%s , %s , %s , %s , %s , %s , %s)
        ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price))

        self.db.commit()
        self.message_box('New Book Added')
        self.show_all_books()

        self.bookTitle_lineEdit.setText('')
        self.description_textEdit.setPlainText('')
        self.bookCode_lineEdit.setText('')
        self.category_comboBox.setCurrentIndex(0)
        self.author_comboBox.setCurrentIndex(0)
        self.publisher_comboBox.setCurrentIndex(0)
        self.bookPrice_lineEdit.setText('')

    def search_books(self):
        if self.bookTitle_lineEdit_search_Edit.text():
            self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
            self.cur = self.db.cursor()

            book_title = self.bookTitle_lineEdit_search_Edit.text()
            sql = '''SELECT * FROM book WHERE book_name=%s'''
            self.cur.execute(sql, [(book_title)])

            data = self.cur.fetchone()

            self.bookTitle_lineEdit_Edit.setText(data[1])
            self.description_textEdit_edit.setPlainText(data[2])
            self.bookCode_lineEdit_Edit.setText(data[3])
            self.category_comboBox_Edit.setCurrentText(data[4])
            self.author_comboBox_Edit.setCurrentText(data[5])
            self.publisher_comboBox_Edit.setCurrentText(data[6])
            self.bookPrice_lineEdit_Edit.setText(str(data[7]))
        else:
            self.message_box('Enter A Book Name For Editing!')

    def edit_books(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        book_title = self.bookTitle_lineEdit_Edit.text()
        book_description = self.description_textEdit_edit.toPlainText()
        book_code = self.bookCode_lineEdit_Edit.text()
        book_category = self.category_comboBox_Edit.currentText()
        book_author = self.author_comboBox_Edit.currentText()
        book_publisher = self.publisher_comboBox_Edit.currentText()
        book_price = self.bookPrice_lineEdit_Edit.text()

        search_book_title = self.bookTitle_lineEdit_search_Edit.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s ,book_description=%s ,book_code=%s 
                            ,book_category=%s ,book_author=%s ,book_publisher=%s ,book_price=%s
                            WHERE book_name=%s
        ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price,
              search_book_title))

        self.db.commit()
        self.message_box('Book Updated')
        self.show_all_books()

        self.bookTitle_lineEdit_search_Edit.setText(book_title)

    def delete_books(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        book_title = self.bookTitle_lineEdit_Edit.text()
        warning = QMessageBox.warning(self, 'Delete Book', 'Are You Sure You Want To Delete This Book',
                                      QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = ''' DELETE FROM book WHERE book_name=%s'''
            self.cur.execute(sql, ([book_title]))

            self.db.commit()
            self.message_box('Book Deleted!')

            self.bookTitle_lineEdit_Edit.setText('')
            self.description_textEdit_edit.setPlainText('')
            self.bookCode_lineEdit_Edit.setText('')
            self.category_comboBox_Edit.setCurrentIndex(0)
            self.author_comboBox_Edit.setCurrentIndex(0)
            self.publisher_comboBox_Edit.setCurrentIndex(0)
            self.bookPrice_lineEdit_Edit.setText('')
            self.bookTitle_lineEdit_search_Edit.setText('')
            self.show_all_books()

    # ============================================= client ===============================================
    def add_new_client(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        client_name = self.client_name_lineEdit.text()
        client_email = self.client_email_lineEdit.text()
        client_national_id = self.client_national_id_lineEdit.text()

        self.cur.execute('''
            INSERT INTO clients (client_name , client_email , client_national_id)
            VALUES (%s , %s , %s)
        ''', (client_name, client_email, client_national_id))
        self.db.commit()
        self.db.close()
        self.message_box('Client Added!')
        self.show_all_client()

    def show_all_client(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT client_name,client_email,client_national_id FROM clients''')
        data = self.cur.fetchall()

        self.all_clients_tableWidget.setRowCount(0)
        self.all_clients_tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.all_clients_tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.all_clients_tableWidget.rowCount()
            self.all_clients_tableWidget.insertRow(row_position)
        self.db.close()

    def search_client(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        client_national_id = self.client_national_id_edit_search_lineEdit.text()

        sql = ''' SELECT * FROM clients WHERE client_national_id = %s'''
        self.cur.execute(sql, [(client_national_id)])
        data = self.cur.fetchone()

        self.client_name_edit_lineEdit.setText(data[1])
        self.client_email_edit_lineEdit.setText(data[2])
        self.client_national_id_edit_lineEdit.setText(data[3])

    def edit_client(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        client_original_national_id = self.client_national_id_edit_search_lineEdit.text()

        client_name = self.client_name_edit_lineEdit.text()
        client_email = self.client_email_edit_lineEdit.text()
        client_national_id = self.client_national_id_edit_lineEdit.text()

        self.cur.execute('''
            UPDATE clients SET client_name = %s , client_email = %s , client_national_id = %s WHERE client_national_id = %s
        ''', (client_name, client_email, client_national_id, client_original_national_id))

        self.db.commit()
        self.db.close()
        self.message_box('Client Information Updated!')
        self.show_all_client()

    def delete_client(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        client_original_national_id = self.client_national_id_edit_search_lineEdit.text()

        warning = QMessageBox.warning(self, 'Delete Client', 'Are You Sure You Want To Delete This Client?',
                                      QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = '''DELETE FROM clients WHERE client_national_id = %s'''
            self.cur.execute(sql, [(client_original_national_id)])
            self.db.commit()
            self.db.close()
            self.message_box('Client Deleted!')

            self.client_national_id_edit_search_lineEdit.setText('')
            self.client_name_edit_lineEdit.setText('')
            self.client_email_edit_lineEdit.setText('')
            self.client_national_id_edit_lineEdit.setText('')
            self.show_all_client()

    # ============================================= users ================================================

    def add_new_user(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        user_name = self.username_lineEdit.text()
        email = self.email_lineEdit.text()
        password = self.password_lineEdit.text()
        confirm_password = self.passwordConfig_lineEdit.text()

        if password == confirm_password:
            self.cur.execute('''
                INSERT INTO users(user_name , user_email , user_password)
                VALUES (%s , %s , %s)
            ''', (user_name, email, password))
            self.db.commit()
            self.message_box('User Added!')
        else:
            self.wrong_password_label.setText('The Passwords Are Not Match!')

    def login(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        user_name = self.username_lineEdit_edit_login.text()
        password = self.password_lineEdit_edit_login.text()

        sql = '''SELECT * FROM users'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if user_name == row[1] and password == row[3]:
                self.message_box('You Are In!')
                self.editUser_groupBox.setEnabled(True)

                self.username_lineEdit_edit.setText(row[1])
                self.email_lineEdit_edit.setText(row[2])
                self.password_lineEdit_edit.setText(row[3])

    def edit_user(self):
        username = self.username_lineEdit_edit.text()
        email = self.email_lineEdit_edit.text()
        password = self.password_lineEdit_edit.text()
        confirm_password = self.passwordConfig_lineEdit_edit.text()

        if password == confirm_password:
            self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
            self.cur = self.db.cursor()

            original_name = self.username_lineEdit_edit_login.text()

            self.cur.execute('''
                UPDATE users SET user_name =%s ,user_email=%s ,user_password=%s WHERE user_name=%s
            ''', (username, email, password, original_name))
            self.db.commit()

            self.message_box('Data Updated Successfully!')

            self.username_lineEdit_edit.setText('')
            self.password_lineEdit_edit.setText('')
            self.email_lineEdit_edit.setText('')
            self.passwordConfig_lineEdit_edit.setText('')
            self.editUser_groupBox.setEnabled(False)

    # ============================================= settings ================================================
    def add_category(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        category_name = self.new_category_lineEdit.text()
        self.cur.execute("""
            INSERT INTO category (category_name) VALUES (%s)
        """, (category_name,))
        self.db.commit()
        self.message_box('new Category Added!')
        self.new_category_lineEdit.setText('')
        self.show_category()
        self.show_categorise_combo()

    def show_category(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

    def add_author(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        author_name = self.new_author_lineEdit.text()
        self.cur.execute("""
                    INSERT INTO authors (author_name) VALUES (%s)
                """, (author_name,))
        self.db.commit()
        self.message_box('new Author Added!')
        self.new_author_lineEdit.setText('')
        self.show_author()
        self.show_authors_combo()

    def show_author(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT author_name FROM authors''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    def add_publisher(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        publisher_name = self.new_publisher_lineEdit.text()
        self.cur.execute("""
                            INSERT INTO publisher (publisher_name) VALUES (%s)
                        """, (publisher_name,))
        self.db.commit()
        self.message_box('new Publisher Added!')
        self.new_publisher_lineEdit.setText('')
        self.show_publisher()
        self.show_publishers_combo()

    def show_publisher(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    # ============================================= show settings data in UI ==========================================
    def show_categorise_combo(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()

        self.category_comboBox.clear()
        for category in data:
            self.category_comboBox.addItem(category[0])
            self.category_comboBox_Edit.addItem(category[0])

    def show_authors_combo(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT author_name FROM authors''')
        data = self.cur.fetchall()

        self.author_comboBox.clear()
        for author in data:
            self.author_comboBox.addItem(author[0])
            self.author_comboBox_Edit.addItem(author[0])

    def show_publishers_combo(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        self.publisher_comboBox.clear()
        for publisher in data:
            self.publisher_comboBox.addItem(publisher[0])
            self.publisher_comboBox_Edit.addItem(publisher[0])

    # ============================================= Export Data ========================================
    def export_day_operations(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''
            SELECT book.book_name ,dayoperations.book_code , clients.client_name ,
            dayoperations.client_national_id , dayoperations.type ,
            dayoperations.date , dayoperations.to_date
            FROM library.dayoperations 
            join library.clients 
            on library.dayoperations.client_national_id = library.clients.client_national_id
            join library.book 
            on library.dayoperations.book_code = library.book.book_code
        ''')

        data = self.cur.fetchall()
        wb = Workbook('day_operation.xlsx')
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'Book Title')
        sheet1.write(0, 1, 'Book Code')
        sheet1.write(0, 2, 'Book Name')
        sheet1.write(0, 3, 'Client National Id')
        sheet1.write(0, 4, 'Type')
        sheet1.write(0, 5, 'From - Date')
        sheet1.write(0, 6, 'To - Date')

        row_num = 1
        for row in data:
            column_num = 0
            for item in row:
                sheet1.write(row_num, column_num, str(item))
                column_num += 1
            row_num += 1

        wb.close()
        self.message_box('Record Created Successfully')

    def export_books(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute(
            '''SELECT book_code,book_name,book_description,book_category,book_author,book_publisher,book_price FROM book''')
        data = self.cur.fetchall()

        wb = Workbook('all_books.xlsx')
        sheet1 = wb.add_worksheet()

        sheet1.write(0, 0, 'Book Code')
        sheet1.write(0, 1, 'Book Title')
        sheet1.write(0, 2, 'Book Book Description')
        sheet1.write(0, 3, 'Book Category')
        sheet1.write(0, 4, 'Book Author')
        sheet1.write(0, 5, 'Book Publisher')
        sheet1.write(0, 6, 'Book Price')

        row_num = 1
        for row in data:
            column_num = 0
            for item in row:
                sheet1.write(row_num, column_num, str(item))
                column_num += 1
            row_num += 1

        wb.close()
        self.message_box('Record Created Successfully')

    def export_clients(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='', db='library_b')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT client_name,client_email,client_national_id FROM clients''')
        data = self.cur.fetchall()

        wb = Workbook('all_clients.xlsx')
        sheet1 = wb.add_worksheet()

        sheet1.write(0, 0, 'Client Name')
        sheet1.write(0, 1, 'Client Email')
        sheet1.write(0, 2, 'Client National Id')

        row_num = 1
        for row in data:
            column_num = 0
            for item in row:
                sheet1.write(row_num, column_num, str(item))
                column_num += 1
            row_num += 1

        wb.close()
        self.message_box('Record Created Successfully')

    # ============================================= UI Themes ==========================================
    def dark_blue_theme(self):
        style = open('themes/dark_blue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_gray_theme(self):
        style = open('themes/darkgray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_orange_theme(self):
        style = open('themes/dark_orange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def qdark_theme(self):
        style = open('themes/darkstyle.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    # ============================================= Message box ==========================================

    def message_box(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)

        msg.exec()


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

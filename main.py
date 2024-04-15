import random

from PyQt6.QtCore import Qt, QSize, QDateTime
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox, QMainWindow, QVBoxLayout \
    , QHBoxLayout, QGridLayout, QWidget, QTableWidget, QStackedLayout, QTabWidget, QStackedWidget, QTableWidgetItem, \
    QFormLayout \
    , QRadioButton, QDateTimeEdit, QCalendarWidget, QComboBox

from PyQt6.QtGui import QAction, QFont, QPainter, QColor, QIcon
import sys
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

Style_Sheet = """
            QLabel#MainTitle {
                font-size: 20px;
                font-weight: bold;
                font-family: Bahnschrift;
                margin-bottom: 10px;
            }
            QLabel#subTitle {
                font-size: 16px;
                font-weight: bold;
                color: #0353A4;
                font-family: Bahnschrift;
            }
            QLabel#OptionTitle {
                font-size: 14px;
                font-weight: bold;
                font-family: Bahnschrift;
            }
            QLabel#StockTableData {
                font-size: 16px;
                font-weight: bold;
                font-family: Bahnschrift;
            }
            QLabel#signlogheader {
                font-size: 16px;
                font-weight: bold;
                font-family: Bahnschrift;
            }
            QLineEdit#InputBox {
                border-radius: 5px;
                border: 1px solid #000;
                padding: 5px;
                font-family: Bahnschrift;
            }
            QPushButton#delButton {
                border-radius: 5px;
                border: 1px solid #fff;
                height: 50px;
                background-color: #EF476F;
                color: #000;
                margin-top: 20px;
                font-weight: bold;
                font-size: 14px;
                font-family: Bahnschrift;
            }
            QPushButton#delButton:pressed {
                background-color: #fff;
                color: #000;
            }
            QPushButton#regButton {
                border-radius: 5px;
                border: 1px solid #fff;
                height: 50px;
                background-color: #26547C;
                color: #fff;
                margin-top: 20px;
                font-weight: bold;
                font-size: 14px;
                font-family: Bahnschrift;
            }
            QPushButton#regButton:pressed {
                background-color: #fff;
                color: #000;
            }
            QPushButton#upButton {
                border-radius: 5px;
                border: 1px solid #fff;
                height: 50px;
                background-color: #776274;
                color: #fff;
                margin-top: 20px;
                font-weight: bold;
                font-size: 14px;
                font-family: Bahnschrift;
            }
            QPushButton#upButton:pressed {
                background-color: #fff;
                color: #000;
            }
            QPushButton#adminMainButton {
                border-radius: 5px;
                border: 1px solid #fff;
                height: 50px;
                background-color: #48cae4;
                color: #fff;
                margin-top: 10px;
                margin-bottom: 10px;
                font-weight: bold;
                font-size: 14px;
                font-family: Bahnschrift;
            }
            QPushButton#adminMainButton:pressed {
                background-color: #fff;
                color: #000;
            }
            QPushButton#adminChangeButton {
                border-radius: 5px;
                border: 1px solid #fff;
                height: 50px;
                background-color: #52b788;
                color: #fff;
                margin-top: 10px;
                font-weight: bold;
                font-size: 14px;
                font-family: Bahnschrift;
            }
            QPushButton#adminChangeButton:pressed {
                background-color: #fff;
                color: #000;
            }
            QPushButton#signOutButton {
                border-radius: 10px;
                border: 1px solid #fff;
                height: 30px;
                background-color: #dad7cd;
                color: #000;
                margin-top: 60px;
                font-weight: bold;
                font-size: 12px;
                font-family: Bahnschrift;
            }
            QPushButton#signOutButton:pressed {
                background-color: #fff;
                color: #000;
            }
            QPushButton#addButton {
                border-radius: 5px;
                border: 1px solid #fff;
                height: 30px;
                background-color: #03045e;
                color: #fff;

                font-weight: bold;
                font-size: 14px;
                font-family: Bahnschrift;
            }
            QPushButton#addButton:pressed {
                background-color: #fff;
                color: #000;
            }
            QPushButton#sellButton {
                border-radius: 5px;
                border: 1px solid #fff;
                height: 30px;
                background-color: #52b788;
                color: #000;

                font-weight: bold;
                font-size: 14px;
                font-family: Bahnschrift;
            }
            QPushButton#sellButton:pressed {
                background-color: #fff;
                color: #000;
            }
            QPushButton#printButton {
                border-radius: 5px;
                border: 1px solid #fff;
                height: 30px;
                background-color: #219ebc;
                color: #fff;
                font-weight: bold;
                font-size: 14px;
                font-family: Bahnschrift;
            }
            QPushButton#printButton:pressed {
                background-color: #fff;
                color: #000;
            }

        """


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medicine Inventory System")
        self.setWindowIcon(QIcon('assets/inventoryLogo.png'))
        # Getting the dimension of screen
        self.screen_geometry = QApplication.primaryScreen().geometry()
        self.width = self.screen_geometry.width()
        self.height = self.screen_geometry.height()
        # print(width, height)

        self.setGeometry(0, 0, self.width, self.height)
        self.showMaximized()

        self.initGUI()

    def initGUI(self):
        self.tabWidget = QTabWidget()
        self.admin_tab = Administrator(self.tabWidget, self.width)
        self.register_tab = Register(self.width, self.height, self.tabWidget)
        self.sales_tab = Sales(self.width)
        self.dataAnalysis = DataAnalysis()
        self.salesDataAnalysis = SalesDataAnalysis()
        self.dashboard_tab = DashBoard(self.width, self.height, self.dataAnalysis, self.salesDataAnalysis)
        self.tabWidget.addTab(self.admin_tab, "ADMIN")
        self.tabWidget.addTab(self.register_tab, "REGISTER")
        self.tabWidget.addTab(self.sales_tab, "SALES")
        self.tabWidget.addTab(self.dashboard_tab, "DASHBOARD")
        self.tabWidget.setStyleSheet("QTabBar::tab { height: 35px; width: 100px; }"
                                     "QTabBar::tab:selected { background-color: #003049; font-family: Bahnschrift; font-weight: bold; color: #ffffff }"
                                     "QTabBar::tab:!selected { background-color: lightgray; font-family: Bahnschrift}")
        self.tabWidget.setTabEnabled(1, False)  # Change it later
        self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setTabEnabled(3, False)
        # self.tabWidget.setCurrentIndex(3)  # For development, delete it later

        self.setCentralWidget(self.tabWidget)
        DataAnalysis()
        SalesDataAnalysis()


# -------- ADMINISTRATION SECTION -------- #
class SignUp(QDialog):
    def __init__(self, stacked_widget, screenWidth):
        super().__init__()
        self.setFixedWidth(int(screenWidth * 0.65))
        self.setFixedHeight(400)
        self.setContentsMargins(500, 100, 0, 0)

        layout = QVBoxLayout()

        signUpLabel = QLabel("Sign Up", self)
        signUpLabel.setObjectName("signlogheader")
        # signUpLabel.setFixedSize(400, 20)
        signUpLabel.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(signUpLabel)
        self.enter_name_box = QLineEdit()
        self.enter_name_box.setPlaceholderText("Name")
        self.enter_name_box.setObjectName("InputBox")
        layout.addWidget(self.enter_name_box)

        self.enter_password_box = QLineEdit()
        self.enter_password_box.setPlaceholderText("Password")
        self.enter_password_box.setObjectName("InputBox")
        layout.addWidget(self.enter_password_box)

        self.enter_confirm_password_box = QLineEdit()
        self.enter_confirm_password_box.setPlaceholderText("Confirm Password")
        self.enter_confirm_password_box.setObjectName("InputBox")
        layout.addWidget(self.enter_confirm_password_box)

        self.register_button = QPushButton("Register", clicked=self.register)
        self.register_button.setObjectName("adminMainButton")
        layout.addWidget(self.register_button)

        not_login_question = QLabel("Already registered?")
        self.login_button = QPushButton("Log In", clicked=lambda: stacked_widget.setCurrentIndex(1))
        self.login_button.setObjectName("adminChangeButton")
        self.login_button.setFixedWidth(100)
        # self.login_button.pressed.connect(self.toLogInScreen)
        layout.addWidget(not_login_question)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def register(self):
        # print("I am pressed")
        name = self.enter_name_box.text()
        password = self.enter_password_box.text()
        confirm_password = self.enter_confirm_password_box.text()

        if name and password and confirm_password:
            if password == confirm_password:
                # print("here")
                try:
                    connection = sqlite3.connect("Database.db")
                    cursor = connection.cursor()

                    cursor.execute("INSERT INTO userData (name, pass_word) VALUES (?, ?)", (name, password))

                    connection.commit()
                    cursor.close()
                    connection.close()
                    successWindow = successfulRegister()
                    successWindow.exec()
                except:
                    # print("failed")
                    error_message = "Registration Failed, please try again."
                    warning_Box = WarningBox(error_message)
                    warning_Box.exec()
            else:
                error_message = "Your Password didn't Match"
                warningWindow = WarningBox(error_message)
                warningWindow.exec()
        else:
            error_message = "Please Fill Up All Required Field"
            warningWindow = WarningBox(error_message)
            warningWindow.exec()


class LogIn(QDialog):
    def __init__(self, stacked_widget, tabWidget, screenWidth):
        super().__init__()
        self.setFixedWidth(int(screenWidth * 0.65))
        self.setFixedHeight(400)
        self.setContentsMargins(500, 100, 0, 0)
        self.tabWidgetControl = tabWidget

        layout = QVBoxLayout()

        logInLabel = QLabel("Log In", self)
        logInLabel.setObjectName("signlogheader")
        # signUpLabel.setFixedSize(400, 20)
        logInLabel.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(logInLabel)
        self.enter_name_box = QLineEdit()
        self.enter_name_box.setPlaceholderText("Name")
        self.enter_name_box.setObjectName("InputBox")
        layout.addWidget(self.enter_name_box)

        self.enter_password_box = QLineEdit()
        self.enter_password_box.setPlaceholderText("Password")
        self.enter_password_box.setObjectName("InputBox")
        self.enter_password_box.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.enter_password_box)

        self.login_button = QPushButton("Log In", clicked=self.login)
        self.login_button.setObjectName("adminMainButton")
        layout.addWidget(self.login_button)
        # self.register_button.pressed.connect(self.register)

        not_login_question = QLabel("Not registered yet?")
        self.register_button = QPushButton("Register", clicked=lambda: stacked_widget.setCurrentIndex(0))
        self.register_button.setObjectName("adminChangeButton")
        self.register_button.setFixedWidth(100)
        layout.addWidget(not_login_question)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

    def login(self):
        loginSuccessful = False
        name = self.enter_name_box.text()
        password = self.enter_password_box.text()

        connection = sqlite3.connect("Database.db")
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM userData")
        userlist = list(result)
        # print(userlist)
        if name and password:
            for item in userlist:
                if name == item[0] and password == item[1]:
                    loginSuccessful = True
                    self.tabWidgetControl.setTabEnabled(1, True)
                    self.tabWidgetControl.setCurrentIndex(1)
                    self.tabWidgetControl.setTabEnabled(2, True)
                    self.tabWidgetControl.setTabEnabled(3, True)
                    self.tabWidgetControl.setTabEnabled(0, False)
                    break
            if loginSuccessful == False:
                errorMessage = "Failed, Wrong UserName and Password."
                self.errorMessage = WarningBox(errorMessage)
                self.errorMessage.exec()

        else:
            errorMessage = "Failed, Please FillUp The Required Fields."
            self.errorMessage = WarningBox(errorMessage)
            self.errorMessage.exec()


class Administrator(QWidget):
    def __init__(self, tabWidget, screenWidth):
        super().__init__()
        self.stacked_widget = QStackedLayout()
        self.signUpScreen = SignUp(self.stacked_widget, screenWidth)
        self.logInScreen = LogIn(self.stacked_widget, tabWidget, screenWidth)
        self.stacked_widget.addWidget(self.signUpScreen)
        self.stacked_widget.addWidget(self.logInScreen)

        self.setLayout(self.stacked_widget)


# -------- ADMINISTRATION SECTION END -------- #

# -------- REGISTER SECTION -------- #

class Register(QWidget):
    def __init__(self, screenWidth, screenHeight, tabWidget):
        super().__init__()
        self.tabWidget = tabWidget
        self.horizontalLayout = QHBoxLayout()

        self.salesTableInv = salesTableInv(screenWidth)
        self.tableSection = TableSection(screenWidth)
        self.formSection = FormSection(screenWidth, self.tableSection, self.tabWidget, self.salesTableInv)
        self.horizontalLayout.addWidget(self.formSection)
        self.horizontalLayout.addWidget(self.tableSection)

        self.setLayout(self.horizontalLayout)


class FormSection(QWidget):
    def __init__(self, screenWidth, insoftableSection, tabWidget, salesTableInventory):
        super().__init__()
        self.salesTableInv = salesTableInventory
        self.tabWidget = tabWidget
        self.max_id = self.gettingMedId()
        self.setFixedWidth(int(screenWidth * 0.29))
        self.tableSection = insoftableSection
        self.tableSection.invTable.cellClicked.connect(self.detectClick)
        self.registrationFailed = registrationFailed()
        self.failedToUpdate = failedToUpdate()
        self.updateCurrentStorage = updateCurrentStorage(self.tableSection)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(15)
        self.id_row = QHBoxLayout()

        self.form_layout = QFormLayout()

        self.title = QLabel("REGISTER MEDICINE", self)
        self.title.setObjectName("MainTitle")
        self.verticalLayout.addWidget(self.title)

        # ID Input section
        self.id = QLabel("ID", self)
        self.id.setObjectName("OptionTitle")
        self.id_input = QLineEdit()
        self.id_input.setText(str(self.max_id + 1))
        # self.id_input.setFixedWidth(295)
        self.id_input.setFixedHeight(25)
        self.id_input.setObjectName("InputBox")
        self.form_layout.addRow(self.id, self.id_input)
        # self.id_row.addWidget(self.id)
        # self.id_row.addWidget(self.id_input)
        # --------------- #

        # BRAND Input section
        self.brand = QLabel("Brand", self)
        self.brand.setObjectName("OptionTitle")
        self.brand_input = QLineEdit()
        self.brand_input.setObjectName("InputBox")
        self.form_layout.addRow(self.brand, self.brand_input)
        # --------------- #

        # Dosage Input section
        dosage_list = self.gettingDosageForm()
        self.dosage = QLabel("Dosage Form", self)
        self.dosage.setObjectName("OptionTitle")
        self.dosage_input = QComboBox()
        for item in dosage_list:
            self.dosage_input.addItem(item)
        self.dosage_input.setStyleSheet("font-size: 12px; font-family: Bahnschrift; padding: 5px")
        self.form_layout.addRow(self.dosage, self.dosage_input)
        # --------------- #

        # Strength Input Section
        self.strength = QLabel("Composition", self)
        self.strength.setObjectName("OptionTitle")
        self.strength_input = QLineEdit()
        self.strength_input.setObjectName("InputBox")
        self.form_layout.addRow(self.strength, self.strength_input)
        # --------------- #

        # Company Input section
        company_name = self.gettingCompanyName()
        self.company = QLabel("Company", self)
        self.company.setObjectName("OptionTitle")
        self.company_input = QComboBox()
        for item in company_name:
            self.company_input.addItem(item)
        self.company_input.setStyleSheet("font-size: 12px; font-family: Bahnschrift; padding: 5px;")
        self.form_layout.addRow(self.company, self.company_input)
        # --------------- #

        # Quantity section title
        self.qty_title = QLabel("", self)
        self.form_layout.addRow(self.qty_title)

        # Quantity Input Section
        self.stockQty = QLabel("Quantity", self)
        self.stockQty.setObjectName("OptionTitle")
        self.stockQty_input = QLineEdit()
        self.stockQty_input.setObjectName("InputBox")
        self.form_layout.addRow(self.stockQty, self.stockQty_input)

        self.fileQty = QLabel("File Qty", self)
        self.fileQty.setObjectName("OptionTitle")
        self.fileQty_input = QLineEdit()
        self.fileQty_input.setObjectName("InputBox")
        self.form_layout.addRow(self.fileQty, self.fileQty_input)

        self.pcsPerFile = QLabel("Pcs/File", self)
        self.pcsPerFile.setObjectName("OptionTitle")
        self.pcsPerFile_input = QLineEdit()
        self.pcsPerFile_input.setObjectName("InputBox")
        self.form_layout.addRow(self.pcsPerFile, self.pcsPerFile_input)
        # ------------------- #

        # Space between
        self.currency_title = QLabel("", self)
        self.form_layout.addRow(self.currency_title)
        # ------------------- #

        # Currency Input Section
        self.purchPrice = QLabel("Purchase Price", self)
        self.purchPrice.setObjectName("OptionTitle")
        self.purchPrice_input = QLineEdit()
        self.purchPrice_input.setObjectName("InputBox")
        self.form_layout.addRow(self.purchPrice, self.purchPrice_input)
        self.sellPrice = QLabel("Selling Price", self)
        self.sellPrice.setObjectName("OptionTitle")
        self.sellPrice_input = QLineEdit()
        self.sellPrice_input.setObjectName("InputBox")
        self.form_layout.addRow(self.sellPrice, self.sellPrice_input)

        self.verticalLayout.addLayout(self.form_layout)

        # Button Section
        self.buttonRow = QHBoxLayout()
        self.registerButton = QPushButton("REGISTER")
        self.registerButton.setObjectName("regButton")
        self.registerButton.clicked.connect(self.register)
        self.buttonRow.addWidget(self.registerButton)

        self.updateButton = QPushButton("UPDATE")
        self.updateButton.setObjectName("upButton")
        self.updateButton.clicked.connect(self.update)
        self.buttonRow.addWidget(self.updateButton)

        self.deleteButton = QPushButton("DELETE")
        self.deleteButton.setObjectName("delButton")
        self.deleteButton.clicked.connect(self.delete)
        self.buttonRow.addWidget(self.deleteButton)

        self.signOutButton = QPushButton("SIGN OUT")
        self.signOutButton.setObjectName("signOutButton")
        self.signOutButton.setFixedWidth(100)
        self.signOutButton.clicked.connect(self.signOut)

        self.verticalLayout.addLayout(self.buttonRow)
        self.verticalLayout.addWidget(self.signOutButton)
        self.verticalLayout.addStretch(1)
        self.setLayout(self.verticalLayout)

    def register(self):
        id = self.id_input.text()
        brand = self.brand_input.text()
        dosage_form = self.dosage_input.currentText()
        strength = self.strength_input.text()
        company = self.company_input.currentText()
        stockQuantity = self.stockQty_input.text()
        file_qty = self.fileQty_input.text()
        pcsPerFile = self.pcsPerFile_input.text()
        inboundPrice = self.purchPrice_input.text()
        outboundPrice = self.sellPrice_input.text()
        # print(dosage_form, company)

        if id and brand and dosage_form and strength and company and inboundPrice and outboundPrice:
            inboundPrice = float(self.purchPrice_input.text())
            outboundPrice = float(self.sellPrice_input.text())
            if not stockQuantity:
                file_qty = int(self.fileQty_input.text())
                pcsPerFile = int(self.pcsPerFile_input.text())
                stockQuantity = file_qty * pcsPerFile
                self.stockQty_input.setText(str(stockQuantity))
                # print("stock quantity empty")
            elif not file_qty or pcsPerFile:
                stockQuantity = float(self.stockQty_input.text())
                file_qty = 0
                pcsPerFile = 0
                # print("file qty and pcsperfile empty")
            else:
                stockQuantity = float(self.stockQty_input.text())
                file_qty = int(self.fileQty_input.text())
                pcsPerFile = int(self.pcsPerFile_input.text())
                # print("all exist")

            try:
                connection = sqlite3.connect("Database.db")
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO med_inventory (med_id, brand, dosage_form, strength, company, stock_qty, file_qty, pcs_per_file, inbound_price, outbound_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (id, brand, dosage_form, strength, company, stockQuantity, file_qty, pcsPerFile, inboundPrice,
                     outboundPrice))
                connection.commit()
                cursor.close()
                connection.close()

                self.tableSection.loadTableData()  # This is updating the storage data
                self.gettingMedId()
                # self.salesTableInv.loadStockTableData()      # This suppose to update the self.invTable
                self.id_input.setText(str(self.max_id + 1))
                self.brand_input.setText("")
                self.strength_input.setText("")
                self.stockQty_input.setText("")
                self.fileQty_input.setText("")
                self.pcsPerFile_input.setText("")
                self.purchPrice_input.setText("")
                self.sellPrice_input.setText("")
                # self.salesTableInv.loadStockTableData()

            except:
                self.registrationFailed.exec()

        else:
            errorMessage = "Please Fill Up Required Fields."
            errorBox = WarningBox(errorMessage)
            errorBox.exec()

    def detectClick(self):
        index = self.tableSection.invTable.currentRow()
        index_col = self.tableSection.invTable.currentColumn()
        if index_col == 5:
            self.updateCurrentStorage.exec()

        input_fields = [self.id_input, self.brand_input, self.dosage_input, self.strength_input, self.company_input,
                        self.stockQty_input,
                        self.fileQty_input, self.pcsPerFile_input, self.purchPrice_input, self.sellPrice_input]
        for i in range(len(input_fields)):
            if i == 2 or i == 4:
                # print(index, i)
                data = self.tableSection.invTable.item(index, i).text()
                # print(data)
                input_fields[i].setCurrentText(data)
            else:
                data = self.tableSection.invTable.item(index, i).text()
                input_fields[i].setText(data)

    def update(self):

        index = self.tableSection.invTable.currentRow()
        # print(index)
        if index != -1:
            input_fields = [self.id_input, self.brand_input, self.dosage_input, self.strength_input, self.company_input,
                            self.stockQty_input,
                            self.fileQty_input, self.pcsPerFile_input, self.purchPrice_input, self.sellPrice_input]
            extracted_data = []
            for i in range(len(input_fields)):
                if i == 5 or i == 8 or i == 9:
                    extracted_data.append(float(input_fields[i].text()))
                # input_fields[i].text()
                elif i == 6 or i == 7:
                    extracted_data.append(int(input_fields[i].text()))
                elif i == 2 or i == 4:
                    extracted_data.append(input_fields[i].currentText())
                else:
                    extracted_data.append(input_fields[i].text())

            update_data = list(extracted_data)
            try:
                connection = sqlite3.connect("database.db")
                cursor = connection.cursor()
                database_table_header = ["brand", "dosage_form", "strength", "company", "stock_qty", "file_qty",
                                         "pcs_per_file", "inbound_price", "outbound_price"]
                med_id = update_data[0]

                set_clause = ", ".join(f"{header} = ?" for header in database_table_header)
                update_quary = f"UPDATE med_inventory SET {set_clause} WHERE med_id=?"

                cursor.execute(update_quary, update_data[1:] + [med_id])
                connection.commit()
                cursor.close()
                connection.close()

                self.tableSection.loadTableData()

                self.id_input.setText("")
                self.brand_input.setText("")
                # self.dosage_input.setText("")
                # self.company_input.setText("")
                self.strength_input.setText("")
                self.stockQty_input.setText("")
                self.fileQty_input.setText("")
                self.pcsPerFile_input.setText("")
                self.purchPrice_input.setText("")
                self.sellPrice_input.setText("")

            except sqlite3.Error as e:
                self.failedToUpdate.exec()
        else:
            error_message = "Please select something to update"
            error_window = WarningBox(error_message)
            error_window.exec()

    def delete(self):
        try:
            index = self.tableSection.invTable.currentRow()
            # print(index)
            med_id = self.tableSection.invTable.item(index, 0).text()

            connection = sqlite3.connect("Database.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM med_inventory WHERE med_id=?", (med_id,))
            connection.commit()
            cursor.close()
            connection.close()

            self.tableSection.loadTableData()
        except:
            # print("Select an item to delete")
            warning_message = "Select an item to delete"
            warning_box = WarningBox(warning_message)
            warning_box.exec()

    def gettingMedId(self):
        try:
            connection = sqlite3.connect("Database.db")
            cursor = connection.cursor()
            cursor.execute("SELECT TRIM(med_id) from med_inventory")
            med_id = cursor.fetchall()
            med_id_list = [item[0] for item in med_id]
            # print(med_id_list)
            self.med_id_list_int = [int(item) for item in med_id_list]
            self.max_id = max(self.med_id_list_int)
            # print(self.max_id)
            connection.commit()
            cursor.close()
            connection.close()
            return self.max_id
        except:
            print("failed")

    def signOut(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setTabEnabled(3, False)

    def gettingDosageForm(self):
        try:
            connection = sqlite3.connect("Database.db")
            cursor = connection.cursor()
            cursor.execute("SELECT type_name FROM medicine_type")
            dosage_form_data = cursor.fetchall()
            dosage_form_list = [item[0] for item in dosage_form_data]
            return dosage_form_list
        except Exception as e:
            print(e)

    def gettingCompanyName(self):
        try:
            connection = sqlite3.connect("Database.db")
            cursor = connection.cursor()
            cursor.execute("SELECT company_name FROM company_list")
            company_name_data = cursor.fetchall()
            company_name_list = [item[0] for item in company_name_data]
            return company_name_list
        except Exception as e:
            print(e)


class TableSection(QWidget):
    def __init__(self, screenWidth):
        super().__init__()
        table_width = int(screenWidth * 0.69)
        self.setFixedWidth(int(screenWidth * 0.69))
        self.setStyleSheet("background-color: #f8f9fa")

        self.verticalLayout = QVBoxLayout()
        tableHeaders = (
        "ID", "BRAND", "DOSAGE FORM", "COMPOSITION", "COMPANY", "STOCK QTY", "FILE QTY", "Pcs/FILE", "INBOUND PRICE",
        "SELLING PRICE")
        tableWidth = (int(table_width * 0.06), int(table_width * 0.1), int(table_width * 0.1), int(table_width * 0.13),
                      int(table_width * 0.1),
                      int(table_width * 0.09), int(table_width * 0.085), int(table_width * 0.08),
                      int(table_width * 0.12), int(table_width * 0.12))
        # Designing the table
        self.invTable = QTableWidget()
        self.invTable.setColumnCount(10)
        self.invTable.setHorizontalHeaderLabels(tableHeaders)
        self.invTable.horizontalHeader().setStyleSheet("font-weight: bold")
        self.invTable.verticalHeader().setVisible(False)
        for i in range(len(tableHeaders)):
            self.invTable.setColumnWidth(i, tableWidth[i])
        self.verticalLayout.addWidget(self.invTable)

        self.setLayout(self.verticalLayout)
        # self.invTable.cellClicked.connect(self.detectCellClicked)
        self.loadTableData()

    def loadTableData(self):
        connection = sqlite3.connect("Database.db")
        result = connection.execute(
            "SELECT med_id, brand, dosage_form, strength, company, stock_qty, file_qty, pcs_per_file, inbound_price, outbound_price FROM med_inventory")
        self.invTable.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.invTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.invTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.commit()
        connection.close()


class updateCurrentStorage(QDialog):
    def __init__(self, insoftableSection):
        super().__init__()
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Update Storage")
        self.tableSection = insoftableSection
        self.verticalLayout = QVBoxLayout()

        self.stockQty = QLineEdit()
        self.stockQty.setPlaceholderText("Stock Quantity")
        self.stockQty.setObjectName("InputBox")
        self.verticalLayout.addWidget(self.stockQty)

        self.fileQty = QLineEdit()
        self.fileQty.setPlaceholderText("File Quantity")
        self.fileQty.setObjectName("InputBox")
        self.verticalLayout.addWidget(self.fileQty)

        self.pcsPerFile = QLineEdit()
        self.pcsPerFile.setPlaceholderText("Pcs / File")
        self.pcsPerFile.setObjectName("InputBox")
        self.verticalLayout.addWidget(self.pcsPerFile)

        self.addButton = QPushButton("ADD")
        self.addButton.setObjectName("adminChangeButton")
        self.addButton.clicked.connect(self.updateStorage)
        self.verticalLayout.addWidget(self.addButton)

        self.setLayout(self.verticalLayout)

    def updateStorage(self):
        index_row = self.tableSection.invTable.currentRow()
        index_col = self.tableSection.invTable.currentColumn()
        toupdateQuantity = self.stockQty.text()
        toupdateFile = self.fileQty.text()
        toupdatepcsPerFile = self.pcsPerFile.text()
        currentStockQty = self.tableSection.invTable.item(index_row, index_col).text()
        med_id = int(self.tableSection.invTable.item(index_row, 0).text())

        if not toupdateQuantity and not toupdateFile and not toupdatepcsPerFile:
            errorMessage = "Please fill up required field to update."
            warningBox = WarningBox(errorMessage)
            warningBox.exec()

        elif not toupdateQuantity:
            file_qty = int(toupdateFile)
            pcsPerFile = int(toupdatepcsPerFile)
            toupdateQuantity = float(file_qty * pcsPerFile)
            # print(toupdateQuantity)
        else:
            toupdateQuantity = float(self.stockQty.text())

        # print(index_row, index_col, toupdateQuantity, currentStockQty, med_id)
        newStock = float(currentStockQty) + float(toupdateQuantity)

        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            clause = "UPDATE med_inventory SET stock_qty = ? WHERE med_id = ?"
            cursor.execute(clause, (newStock, med_id))
            connection.commit()
            cursor.close()
            connection.close()

            self.tableSection.loadTableData()
            self.close()
        except:
            errorMessage = "Sorry, Failed to update. Try Again."
            self.warningBox = WarningBox(errorMessage)
            self.warningBox.exec()


# ------------ REGISTER SECTION END ------------- #

# ------------ SALES SECTION -------------- #

class Sales(QWidget):
    def __init__(self, width):
        super().__init__()
        self.salesTableInv = salesTableInv(width)
        self.receiptSection = receiptSection(width)
        self.salesDataEntry = salesDataEntry(width, self.salesTableInv, self.receiptSection)
        self.horizontalLayout = QHBoxLayout()
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.salesDataEntry)
        self.verticalLayout.addWidget(self.receiptSection)
        self.horizontalLayout.addWidget(self.salesTableInv)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.setLayout(self.horizontalLayout)


class salesTableInv(QWidget):
    def __init__(self, width):
        super().__init__()
        self.setFixedWidth(int(width * 0.5))
        table_width = int(width * 0.5)
        # self.setStyleSheet("background-color: lightblue")

        self.verticalLayout = QVBoxLayout()
        self.stock_data_label = QLabel("STOCK DATA", self)
        self.stock_data_label.setObjectName("StockTableData")
        self.verticalLayout.addWidget(self.stock_data_label)
        tableHeaders = (
            "ID", "BRAND", "COMPOSITION", "STOCK", "PRICE")
        tableWidth = (int(table_width * 0.18), int(table_width * 0.2), int(table_width * 0.2), int(table_width * 0.19),
                      int(table_width * 0.18))

        # Designing the table
        self.invTable = QTableWidget()
        self.invTable.setColumnCount(5)
        self.invTable.setHorizontalHeaderLabels(tableHeaders)
        self.invTable.horizontalHeader().setStyleSheet("font-weight: bold")
        self.invTable.verticalHeader().setVisible(False)
        for i in range(len(tableHeaders)):
            self.invTable.setColumnWidth(i, tableWidth[i])
        self.verticalLayout.addWidget(self.invTable)

        self.reloadButton = QPushButton("Reload")
        self.reloadButton.setFixedWidth(100)
        self.reloadButton.clicked.connect(self.loadStockTableData)
        self.verticalLayout.addWidget(self.reloadButton)

        self.setLayout(self.verticalLayout)
        # self.invTable.cellClicked.connect(self.detectCellClicked)
        self.loadStockTableData()

    def loadStockTableData(self):
        try:
            print("I am in load stock table data")
            connection = sqlite3.connect("Database.db")
            result = connection.execute(
                "SELECT med_id, brand, strength, stock_qty, outbound_price FROM med_inventory")
            self.invTable.clearContents()
            self.invTable.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.invTable.insertRow(row_number)
                print(row_number)
                for column_number, data in enumerate(row_data):
                    self.invTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    # print(data)

            connection.close()
        except Exception as e:
            print(e)


class salesDataEntry(QWidget):
    def __init__(self, width, salesTableInv, receiptSection):
        super().__init__()
        self.salesTableInv = salesTableInv
        self.receiptTable = receiptSection.receiptTable
        self.grandTotal = receiptSection.grandTotal
        self.receiptTable.itemDoubleClicked.connect(self.deletesellRow)
        self.updateGrandTotal = receiptSection.calculateGrandTotal
        self.disconnectSignal = False

        self.setFixedWidth(int(width * 0.48))
        # self.setStyleSheet("background-color: lightblue")

        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.searchBox = QLineEdit()
        self.searchBox.setPlaceholderText("Search By ID or Brand")
        self.searchBox.setObjectName("InputBox")
        self.searchBox.setFixedWidth(500)
        self.searchBox.textChanged.connect(self.filterTable)
        self.horizontalLayout.addWidget(self.searchBox)

        self.salesAddButton = QPushButton("ADD")
        self.salesAddButton.setObjectName("addButton")
        self.salesAddButton.pressed.connect(self.addtoReceiptTable)
        self.horizontalLayout.addWidget(self.salesAddButton)

        self.setLayout(self.verticalLayout)

    def filterTable(self, button):
        column_number = self.salesTableInv.invTable.currentColumn()
        print(column_number)
        if column_number == -1:
            filter_text = self.searchBox.text().lower()
            for rows in range(self.salesTableInv.invTable.rowCount()):
                item = self.salesTableInv.invTable.item(rows, 1)
                if item:
                    text = item.text().lower()
                    self.salesTableInv.invTable.setRowHidden(rows, filter_text not in text)
        else:
            filter_text = self.searchBox.text().lower()
            for rows in range(self.salesTableInv.invTable.rowCount()):
                item = self.salesTableInv.invTable.item(rows, column_number)
                if item:
                    text = item.text().lower()
                    self.salesTableInv.invTable.setRowHidden(rows, filter_text not in text)

    def addtoReceiptTable(self):
        try:
            if self.disconnectSignal:
                self.receiptTable.cellChanged.disconnect(self.calculateTotalOnQtyChange)
                self.disconnectSignal = False
                # print(self.disconnectSignal)

            self.salesTableInv.invTable.clearSelection()
            row_number = self.receiptTable.rowCount()
            add_row_number = row_number
            self.currentRowofInvTable = self.salesTableInv.invTable.currentRow()

            selection_model = self.salesTableInv.invTable.selectionModel()
            selected_indexes = selection_model.selectedIndexes()
            # print(selected_indexes)
            sold_id = []
            for i in range(row_number):
                sold_id.append(self.receiptTable.item(i, 1).text())
            # print(sold_id)

            if self.currentRowofInvTable != -1:
                # self.receiptTable.cellChanged.connect(self.calculateTotalOnQtyChange)
                self.rowNo = row_number + 1
                self.med_id = self.salesTableInv.invTable.item(self.currentRowofInvTable, 0).text()
                self.med_name = self.salesTableInv.invTable.item(self.currentRowofInvTable, 1).text()
                self.med_unit_price = self.salesTableInv.invTable.item(self.currentRowofInvTable, 4).text()
                self.med_sale_quantity = 1
                self.totalPrice = float(self.med_unit_price) * self.med_sale_quantity

                self.receipt_data = [self.rowNo, self.med_id, self.med_name, self.med_unit_price,
                                     self.med_sale_quantity, self.totalPrice]

                # print(self.receipt_data)
                # print(add_row_number)
                if self.med_id not in sold_id:
                    self.receiptTable.insertRow(add_row_number)

                    for column_num, data in enumerate(self.receipt_data):
                        item = QTableWidgetItem(str(data))
                        # print(add_row_number, column_num, str(data))
                        self.receiptTable.setItem(add_row_number, column_num, item)
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                        if column_num == 3:
                            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)

                    # self.receiptTable.cellChanged.connect(self.calculateTotalOnQtyChange)
                    # self.updateGrandTotal()
                else:
                    warning_message = "Item Already Added in the receipt"
                    warning_box = WarningBox(warning_message)
                    warning_box.exec()
            else:
                errorMessage = "Please Select Item to ADD in the receipt"
                message_box = WarningBox(errorMessage)
                message_box.exec()

        except Exception as e:
            print(e)
        finally:
            if not self.disconnectSignal:
                self.receiptTable.cellChanged.connect(self.calculateTotalOnQtyChange)
                self.disconnectSignal = True
                # print("I am here")
                self.updateGrandTotal()

    def calculateTotalOnQtyChange(self):
        try:
            selectedRowofReceiptTable = self.receiptTable.currentRow()
            self.receiptTable.cellChanged.disconnect(self.calculateTotalOnQtyChange)
            # print(selectedRowofReceiptTable)
            if selectedRowofReceiptTable != -1:
                self.newQty = self.receiptTable.item(selectedRowofReceiptTable, 4).text()
                med_unit_price = self.receiptTable.item(selectedRowofReceiptTable, 3).text()
                self.newTotal = float(self.newQty) * float(med_unit_price)
                # print(self.newQty, self.newTotal)
                item = QTableWidgetItem(str(round(self.newTotal, 2)))
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.receiptTable.setItem(selectedRowofReceiptTable, 5, item)
                self.updateGrandTotal()

        except Exception as e:
            print(e)

        finally:
            self.receiptTable.cellChanged.connect(self.calculateTotalOnQtyChange)

    def deletesellRow(self):
        current_row = self.receiptTable.currentRow()
        # print(current_row)
        if current_row >= 0:
            self.receiptTable.removeRow(current_row)
            currentRowCount = self.receiptTable.rowCount()
            # print(currentRowCount)
            if currentRowCount != 0:
                grandTotal = 0
                for i in range(currentRowCount):
                    grandTotal = grandTotal + float(self.receiptTable.item(i, 5).text())
                    item = QTableWidgetItem(str(i + 1))
                    self.receiptTable.setItem(i, 0, item)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.grandTotal.setText(f"Grand Total: {grandTotal} tk")
            elif currentRowCount == 0:
                self.grandTotal.setText(f"Grand Total: 0 tk")


class receiptSection(QWidget):
    def __init__(self, width):
        super().__init__()
        self.date_comp = datetime.now()
        self.current_date = self.date_comp.date()
        # Random Invoice Generation
        self.invoice_no = random.randint(100000, 1000000)

        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()

        self.title = QLabel("MED CENTER")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.title.setFixedHeight(20)
        self.title.setStyleSheet("font-weight: bold;"
                                 "font-size: 18px;"
                                 "font-family: Bahnschrift;")

        self.address = QLabel("Address")
        self.address.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.title.setFixedHeight(20)
        self.address.setStyleSheet("font-weight: bold;"
                                   "font-size: 16px;"
                                   "font-family: Bahnschrift;")

        self.todayDate = QLabel(f"Date           : {self.current_date}", self)
        self.todayDate.setStyleSheet("font-weight: bold;"
                                     "font-size: 15px;"
                                     "font-family: Bahnschrift;")
        self.voucherNo = QLabel(f"Invoice No : {self.invoice_no}", self)
        self.voucherNo.setStyleSheet("font-weight: bold;"
                                     "font-size: 15px;"
                                     "font-family: Bahnschrift;")

        tableHeaders = ["No", "ID", "Name", "Unit Price", "Quantity", "Total"]
        tableWidth = (int(600 * 0.08), int(600 * 0.1), int(600 * 0.3), int(600 * 0.2), int(600 * 0.18), int(600 * 0.18))

        self.receiptTable = QTableWidget()
        # self.receiptTable.setFixedHeight(400)
        self.receiptTable.setColumnCount(6)
        self.receiptTable.setHorizontalHeaderLabels(tableHeaders)
        for i in range(len(tableHeaders)):
            self.receiptTable.setColumnWidth(i, tableWidth[i])
        self.receiptTable.setShowGrid(False)
        self.receiptTable.horizontalHeader().setStyleSheet(
            "font-weight: bold; font-family: Bahnschrift; font-size: 14px")
        self.receiptTable.verticalHeader().setVisible(False)

        self.grandTotal = QLabel(f"Grand Total: 0 TK", self)
        self.grandTotal.setAlignment(Qt.AlignmentFlag.AlignRight)
        # self.grandTotal.setFixedHeight(50)
        self.grandTotal.setStyleSheet("font-weight: bold; font-size: 18px")

        self.calculateGrandTotal()

        self.salesButton = QPushButton("SELL")
        self.salesButton.setFixedWidth(100)
        self.salesButton.setObjectName("sellButton")
        self.salesButton.clicked.connect(self.updateSellWithDatabase)
        self.printButton = QPushButton("PRINT")
        self.printButton.setFixedWidth(100)
        self.printButton.setObjectName("printButton")

        self.horizontalLayout.addWidget(self.salesButton)
        self.horizontalLayout.addWidget(self.printButton)
        self.horizontalLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addWidget(self.address)
        self.verticalLayout.addWidget(self.todayDate)
        self.verticalLayout.addWidget(self.voucherNo)
        self.verticalLayout.addWidget(self.receiptTable)
        self.verticalLayout.addWidget(self.grandTotal)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.verticalLayout)

    def calculateGrandTotal(self):
        self.sumOfTotal = 0
        row_number = self.receiptTable.rowCount()
        # print(row_number)

        if row_number != 0:
            for item in range(row_number):
                value = float(self.receiptTable.item(item, 5).text())
                self.sumOfTotal = self.sumOfTotal + value
                self.grandTotal.setText(f"Grand Total: {round(self.sumOfTotal, 2)} TK")
            # print(self.sumOfTotal)
        else:
            return self.sumOfTotal

    def updateSellWithDatabase(self):
        row_number = self.receiptTable.rowCount()
        column_number = self.receiptTable.columnCount()

        if row_number != 0:
            connection = sqlite3.connect("Database.db")
            cursor = connection.cursor()
            cursor.execute("BEGIN TRANSACTION")
            for row in range(row_number):
                current_sell_data = []
                current_sell_data.append(self.receiptTable.item(row, 1).text())
                current_sell_data.append(self.receiptTable.item(row, 4).text())
                try:
                    result = cursor.execute(
                        "SELECT brand, dosage_form, strength, outbound_price FROM med_inventory WHERE med_id=?",
                        (current_sell_data[0],))
                    # cursor.close()
                    for row_number, row_data in enumerate(result):
                        current_sell_data.extend(row_data)
                        current_sell_data.extend((self.current_date, self.invoice_no))
                        print(current_sell_data)
                        try:
                            cursor = connection.cursor()
                            cursor.execute(
                                "INSERT INTO sales_data (Date, invoice_No, med_id, brand, dosage_form, composition, unit_price, sell_qty)"
                                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (current_sell_data[6], current_sell_data[7], current_sell_data[0],
                                 current_sell_data[2], current_sell_data[3], current_sell_data[4],
                                 current_sell_data[5], current_sell_data[1]))

                            # Need to put out of the loop
                            cursor.execute(
                                "UPDATE med_inventory SET stock_qty = stock_qty - ? WHERE med_id = ?",
                                (current_sell_data[1], current_sell_data[0]))

                            connection.commit()
                            # cursor.execute("END TRANSACTION")

                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)

            cursor.close()
            connection.close()
            message = "Items Are Sold"
            self.receiptTable.clearContents()
            self.receiptTable.setRowCount(0)
            sell_complete = WarningBox(message)
            sell_complete.exec()
            self.invoice_no = random.randint(100000, 1000000)
            new_invoice_no = f"Invoice No : {self.invoice_no}"
            self.voucherNo.setText(new_invoice_no)

            # print(current_sell_data)


# ------------ SALES SECTION END ------------- #

# ------------ DASHBOARD SECTION -------------- #

class DashBoard(QWidget):
    def __init__(self, width, height, DataAnalysis, salesDataAnalysis):
        super().__init__()
        self.dataAnalysis = DataAnalysis
        self.salesDataAnalysis = salesDataAnalysis
        self.addNewMed = addNewMedicineType(self)
        self.addNewCompanyName = addNewCompanyName(self)
        # print(data_for_dashboard)
        self.column_one_vertical = QVBoxLayout()
        self.column_two_vertical = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.dropdownsectionofTrendAnalysis = QHBoxLayout()
        self.column_section = QHBoxLayout()
        # print(self.dataAnalysis.totalStockQty)

        # Create a QDateTimeEdit for the calendar dropdown
        self.date_edit = QDateTimeEdit(self)
        self.date_edit.setFixedWidth(int(width * 0.1))
        self.date_edit.setFixedHeight(int(height * 0.04))
        self.date_edit.setStyleSheet('font-size: 18px')
        self.date_edit.setCalendarPopup(True)  # Enables the calendar popup
        # Create a custom QCalendarWidget
        current_date_time = QDateTime.currentDateTime()
        self.date_edit.setDateTime(current_date_time)
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.calendar_widget = QCalendarWidget(self.date_edit)
        self.date_edit.setCalendarWidget(self.calendar_widget)
        # Connect the selectionChanged signal to update the QDateTimeEdit text
        self.calendar_widget.selectionChanged.connect(self.update_date_edit)

        # Total medicine block
        self.totalMedQty = QLabel(f"Total Medicine\n   {self.dataAnalysis.totalStockQty:,} Pcs")
        self.totalMedQty.setFixedHeight(int(height * 0.13))
        self.totalMedQty.setFixedWidth(int(width * 0.15))
        self.totalMedQty.setStyleSheet('Background-color: #816E94;'
                                       'border-radius: 10px; '
                                       'font-size: 22px; color: #264653;'
                                       'font-family: Bahnschrift; '
                                       'font-weight: bold;'
                                       'padding-bottom: 20px;'
                                       'padding-left: 5px;'
                                       'color: #ffffff;')
        # Total stock value block
        self.totalStockValue = QLabel(f"Total Stock Value\n   {self.dataAnalysis.totalStockValue:,} ৳")
        self.totalStockValue.setFixedHeight(int(height * 0.13))
        self.totalStockValue.setFixedWidth(int(width * 0.15))
        self.totalStockValue.setStyleSheet('Background-color: #373F51;'
                                           'border-radius: 10px; '
                                           'font-size: 22px; color: #264653;'
                                           'font-family: Bahnschrift; '
                                           'font-weight: bold;'
                                           'padding-bottom: 20px;'
                                           'padding-left: 5px;'
                                           'color: #ffffff;')
        # Total sales value block
        self.totalSalesValue = QLabel(f"Total Sales Value\n   {self.dataAnalysis.totalSalesValue:,} ৳")
        self.totalSalesValue.setFixedHeight(int(height * 0.13))
        self.totalSalesValue.setFixedWidth(int(width * 0.15))
        self.totalSalesValue.setStyleSheet('Background-color: #642CA9;'
                                           'border-radius: 10px; '
                                           'font-size: 22px; color: #264653;'
                                           'font-family: Bahnschrift; '
                                           'font-weight: bold;'
                                           'padding-bottom: 20px;'
                                           'padding-left: 5px;'
                                           'color: #ffffff;')
        # Total Opportunity block
        self.totalOpportunity = QLabel(f"Opportunity\n   {self.dataAnalysis.opportunity:,} ৳")
        self.totalOpportunity.setFixedHeight(int(height * 0.13))
        self.totalOpportunity.setFixedWidth(int(width * 0.15))
        self.totalOpportunity.setStyleSheet('Background-color: #80A1D4;'
                                            'border-radius: 10px; '
                                            'font-size: 22px; color: #264653;'
                                            'font-family: Bahnschrift; '
                                            'font-weight: bold;'
                                            'padding-bottom: 20px;'
                                            'padding-left: 5px;'
                                            'color: #ffffff;')
        # Invoice Table Title
        self.tableTitle = QLabel("INVOICE TABLE")
        self.tableTitle.setStyleSheet('font-size: 18px;'
                                      'color: #264653;'
                                      'font-family: Bahnschrift; '
                                      'font-weight: bold;')
        # Invoice Table
        tableHeaders = ["Serial", "Invoice No.", "Sales Value"]
        tableWidth = (int(600 * 0.3), int(600 * 0.2), int(600 * 0.3))

        self.invoiceTable = QTableWidget()
        # self.invoiceTable.setFixedHeight(int(height * 0.3))
        self.invoiceTable.setColumnCount(3)
        self.invoiceTable.setHorizontalHeaderLabels(tableHeaders)
        for i in range(len(tableHeaders)):
            self.invoiceTable.setColumnWidth(i, tableWidth[i])
        self.invoiceTable.setShowGrid(False)
        self.invoiceTable.horizontalHeader().setStyleSheet(
            "font-weight: bold; font-family: Bahnschrift; font-size: 14px")
        self.invoiceTable.verticalHeader().setVisible(False)
        self.collect_Invoice_Data()

        # Company List Table Title
        self.companytableTitle = QLabel("COMPANY LIST")
        self.companytableTitle.setStyleSheet('font-size: 18px;'
                                             'color: #264653;'
                                             'font-family: Bahnschrift; '
                                             'font-weight: bold;')

        # Company List Table
        companyTableHeader = ["Serial", "Company Name"]
        tableWidth = (int(600 * 0.1), int(600 * 0.7))

        self.companyTable = QTableWidget()
        # self.companyTable.setFixedHeight(int(height * 0.3))
        self.companyTable.setColumnCount(2)
        self.companyTable.setHorizontalHeaderLabels(companyTableHeader)
        for i in range(len(companyTableHeader)):
            self.companyTable.setColumnWidth(i, tableWidth[i])
        self.companyTable.setShowGrid(False)
        self.companyTable.horizontalHeader().setStyleSheet(
            "font-weight: bold; font-family: Bahnschrift; font-size: 14px")
        self.companyTable.setStyleSheet("font-weight: bold; font-family: Bahnschrift; font-size: 14px")
        self.companyTable.verticalHeader().setVisible(False)
        self.collect_company_data()

        # Add company Name Button
        self.addCompanyName = QPushButton("ADD NEW COMPANY")
        self.addCompanyName.setObjectName("addButton")
        self.addCompanyName.pressed.connect(self.addNewCompanyName.exec)

        # Medicine Type Table Title
        self.medTypetableTitle = QLabel("MEDICINE TYPE LIST")
        self.medTypetableTitle.setStyleSheet('font-size: 18px;'
                                             'color: #264653;'
                                             'font-family: Bahnschrift; '
                                             'font-weight: bold;')

        # Dosage Form Table
        medTypeTableHeader = ["Serial", "Dosage Form"]
        tableWidth = (int(600 * 0.1), int(600 * 0.7))

        self.medTypeTable = QTableWidget()
        # self.medTypeTable.setFixedHeight(int(height * 0.3))
        self.medTypeTable.setColumnCount(2)
        self.medTypeTable.setHorizontalHeaderLabels(medTypeTableHeader)
        self.medTypeTable.setStyleSheet("font-weight: bold; font-family: Bahnschrift; font-size: 14px")
        for i in range(len(medTypeTableHeader)):
            self.medTypeTable.setColumnWidth(i, tableWidth[i])
        self.medTypeTable.setShowGrid(False)
        self.medTypeTable.horizontalHeader().setStyleSheet(
            "font-weight: bold; font-family: Bahnschrift; font-size: 14px")
        self.medTypeTable.verticalHeader().setVisible(False)
        self.collect_medType_data()

        # Add medicine Type Button
        self.addMedType = QPushButton("ADD DOSAGE FORM")
        self.addMedType.setObjectName("addButton")
        self.addMedType.pressed.connect(self.addNewMed.exec)

        self.reloadButton = QPushButton("Reload")
        self.reloadButton.setFixedWidth(100)

        self.column_two_vertical.addWidget(self.tableTitle)
        self.column_two_vertical.addWidget(self.invoiceTable)
        self.column_two_vertical.addWidget(self.companytableTitle)
        self.column_two_vertical.addWidget(self.companyTable)
        self.column_two_vertical.addWidget(self.addCompanyName)
        self.column_two_vertical.addWidget(self.medTypetableTitle)
        self.column_two_vertical.addWidget(self.medTypeTable)
        self.column_two_vertical.addWidget(self.addMedType)
        self.column_two_vertical.addWidget(self.reloadButton)
        self.column_two_vertical.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Trend Analysis title block
        self.trendAnalysistitle = QLabel("TREND ANALYSIS", self)
        self.trendAnalysistitle.setFixedHeight(int(height * 0.05))
        # self.trendAnalysistitle.setFixedWidth(int(width * 0.985))
        self.trendAnalysistitle.setStyleSheet(f'border-radius: 10px; '
                                              f'font-size: 20px; '
                                              f'color: #264653 ;'
                                              f'font-family: Bahnschrift;'
                                              f'font-weight: bold;')

        # Trend analysis dropdown section
        brandName = self.collect_brand_name()
        self.brandNameCombo = QComboBox()
        self.brandNameCombo.setStyleSheet(f'font-size: 16px; '
                                          f'font-family: Bahnschrift;'
                                          f'font-weight: bold;')
        self.brandNameCombo.setFixedWidth(int(width * 0.1))
        self.brandNameCombo.setFixedHeight(int(height * 0.04))
        for item in brandName:
            self.brandNameCombo.addItem(item)

        composition = ["130mg", "100ml", "100mg", "100mg"]
        self.compositionCombo = QComboBox()
        self.compositionCombo.setStyleSheet(f'font-size: 16px; '
                                            f'font-family: Bahnschrift;'
                                            f'font-weight: bold;')
        self.compositionCombo.setFixedWidth(int(width * 0.1))
        self.compositionCombo.setFixedHeight(int(height * 0.04))
        for item in composition:
            self.compositionCombo.addItem(item)

        chart_type = ["Stock Based on Medicine Type", "Value Based on Medicine Type", "Stock Based on Company",
                      "Value Based on Company"]
        self.chart_typeCombo = QComboBox()
        self.chart_typeCombo.setStyleSheet(f'font-size: 16px; '
                                           f'font-family: Bahnschrift;'
                                           f'font-weight: bold;')
        self.chart_typeCombo.setFixedWidth(int(width * 0.2))
        self.chart_typeCombo.setFixedHeight(int(height * 0.04))
        for item in chart_type:
            self.chart_typeCombo.addItem(item)

        self.chart_typeCombo.currentIndexChanged.connect(self.display_chart)

        trend_chart_type = ["Last 1 week", "Last 1 Month"]
        self.trend_chart_typeCombo = QComboBox()
        self.trend_chart_typeCombo.setStyleSheet(f'font-size: 16px; '
                                                 f'font-family: Bahnschrift;'
                                                 f'font-weight: bold;')
        self.trend_chart_typeCombo.setFixedWidth(int(width * 0.2))
        self.trend_chart_typeCombo.setFixedHeight(int(height * 0.04))
        for item in trend_chart_type:
            self.trend_chart_typeCombo.addItem(item)

        self.trend_chart_typeCombo.currentIndexChanged.connect(self.trend_chart)

        self.dropdownsectionofTrendAnalysis.addWidget(self.date_edit)
        self.dropdownsectionofTrendAnalysis.addWidget(self.brandNameCombo)
        self.dropdownsectionofTrendAnalysis.addWidget(self.compositionCombo)
        self.dropdownsectionofTrendAnalysis.addWidget(self.trend_chart_typeCombo)
        self.dropdownsectionofTrendAnalysis.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Graph section
        self.canvas = MplCanvas(width=4, height=4, dpi=70)
        self.canvas_trend = MplCanvas(width=4, height=4, dpi=70)
        self.display_chart()

        self.horizontalLayout.addWidget(self.totalMedQty)
        self.horizontalLayout.addWidget(self.totalStockValue)
        self.horizontalLayout.addWidget(self.totalSalesValue)
        self.horizontalLayout.addWidget(self.totalOpportunity)
        # self.horizontalLayout.addWidget(self.invoiceTable)
        self.horizontalLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # self.verticalLayout.addWidget(self.title)
        self.column_one_vertical.addLayout(self.horizontalLayout)
        self.column_one_vertical.addWidget(self.chart_typeCombo)
        self.column_one_vertical.addWidget(self.canvas)
        self.column_one_vertical.addWidget(self.trendAnalysistitle)
        self.column_one_vertical.addLayout(self.dropdownsectionofTrendAnalysis)
        self.column_one_vertical.addWidget(self.canvas_trend)
        self.column_one_vertical.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.column_section.addLayout(self.column_one_vertical)
        self.column_section.addLayout(self.column_two_vertical)

        self.setLayout(self.column_section)

    def update_date_edit(self):
        # Get the selected date from the calendar and update the QDateTimeEdit text
        try:
            selected_date = self.calendar_widget.selectedDate()
            formatted_date = selected_date.toString("yyyy-MM-dd")
            self.date_edit.setDisplayFormat("yyyy-MM-dd")
            self.date_edit.setDate(selected_date)
            self.date_edit.setDateTime(selected_date)
        except Exception as e:
            print(e)

    def collect_brand_name(self):
        try:
            connection = sqlite3.connect("Database.db")
            cursor = connection.cursor()
            cursor.execute("SELECT TRIM(brand) FROM med_inventory")
            brandNameData = cursor.fetchall()
            brandNameList = [item[0] for item in brandNameData]
            brandNameSortedList = list(set(brandNameList))
            return brandNameSortedList

        except Exception as e:
            print(e)

    def collect_company_data(self):
        try:
            connection = sqlite3.connect("Database.db")
            cursor = connection.cursor()
            cursor.execute("SELECT company_name FROM company_list")
            companyNameData = cursor.fetchall()
            companyNameList = [item[0] for item in companyNameData]

            self.companyTable.clearContents()
            self.companyTable.setRowCount(0)
            for row_number, row_data in enumerate(companyNameList):
                self.companyTable.insertRow(row_number)
                item_no = QTableWidgetItem(str(row_number + 1))
                item_company = QTableWidgetItem(str(row_data))
                self.companyTable.setItem(row_number, 0, item_no)
                self.companyTable.setItem(row_number, 1, item_company)
                item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_company.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            cursor.close()
            connection.close()

            return companyNameList

        except Exception as e:
            print(e)

    def collect_medType_data(self):
        try:
            connection = sqlite3.connect("Database.db")
            cursor = connection.cursor()
            cursor.execute("SELECT type_name FROM medicine_type")
            medicineNameData = cursor.fetchall()
            medicineNameList = [item[0] for item in medicineNameData]

            self.medTypeTable.clearContents()
            self.medTypeTable.setRowCount(0)
            for row_number, row_data in enumerate(medicineNameList):
                self.medTypeTable.insertRow(row_number)
                item_no = QTableWidgetItem(str(row_number + 1))
                item_med_type = QTableWidgetItem(str(row_data))
                self.medTypeTable.setItem(row_number, 0, item_no)
                self.medTypeTable.setItem(row_number, 1, item_med_type)
                item_no.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_med_type.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            cursor.close()
            connection.close()
            return medicineNameList

        except Exception as e:
            print(e)

    def collect_Invoice_Data(self):
        unique_sales_data = self.salesDataAnalysis.daywise_sales_data
        self.invoiceTable.clearContents()
        self.invoiceTable.setRowCount(0)
        for item in range(len(unique_sales_data)):
            self.invoiceTable.insertRow(item)
            date = QTableWidgetItem(str(unique_sales_data[item][0]))
            invoice_no = QTableWidgetItem(str(unique_sales_data[item][1]))
            sales_value = QTableWidgetItem(str(unique_sales_data[item][2]))
            self.invoiceTable.setItem(item, 0, date)
            self.invoiceTable.setItem(item, 1, invoice_no)
            self.invoiceTable.setItem(item, 2, sales_value)
            date.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            invoice_no.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            sales_value.setTextAlignment(Qt.AlignmentFlag.AlignLeft)

    def stockByMedTypeChart(self):
        # Example data
        self.canvas.axes.clear()
        dosage_form = self.dataAnalysis.dosage_form
        dosage_form_qty = self.dataAnalysis.dosage_form_qty

        # Example bar chart using Matplotlib pyplot
        self.canvas.axes.bar(dosage_form, dosage_form_qty, color='#219EBC')

        for i, value in enumerate(dosage_form_qty):
            self.canvas.axes.text(i, value + 0.5, str(value), ha='center', va='bottom')

        # Set labels and title
        self.canvas.axes.set_xlabel("Dosage Form")
        self.canvas.axes.set_ylabel("Stock Qty")
        self.canvas.axes.set_title("Stock Qty based on Dosage Form")

        # Refresh canvas
        self.canvas.draw()

    def stockValueByMedTypeChart(self):
        # Example data
        self.canvas.axes.clear()
        dosage_form = self.dataAnalysis.dosage_form
        dosage_form_stock_value = self.dataAnalysis.dosage_form_stock_value

        # Example bar chart using Matplotlib pyplot
        self.canvas.axes.bar(dosage_form, dosage_form_stock_value, color='#023E8A')

        for i, value in enumerate(dosage_form_stock_value):
            self.canvas.axes.text(i, value + 0.5, str(value), ha='center', va='bottom')

        # Set labels and title
        self.canvas.axes.set_xlabel("Dosage Form")
        self.canvas.axes.set_ylabel("Stock Value (TK)")
        self.canvas.axes.set_title("Stock Value based on Dosage Form")

        # Refresh canvas
        self.canvas.draw()

    def stockByCompanyChart(self):
        # Example data
        self.canvas.axes.clear()
        company_list = self.dataAnalysis.companyName
        company_wise_qty = self.dataAnalysis.qty_by_company

        # Example bar chart using Matplotlib pyplot
        self.canvas.axes.bar(company_list, company_wise_qty, color='#415A77')

        for i, value in enumerate(company_wise_qty):
            self.canvas.axes.text(i, value + 0.5, str(value), ha='center', va='bottom')

        # Set labels and title
        self.canvas.axes.set_xlabel("Company")
        self.canvas.axes.set_ylabel("Stock Qty")
        self.canvas.axes.set_title("Stock Qty based on Company")

        # Refresh canvas
        self.canvas.draw()

    def stockValueByCompanyChart(self):
        # Example data
        self.canvas.axes.clear()
        company_list = self.dataAnalysis.companyName
        company_wise_stock_value = self.dataAnalysis.stock_value_by_company

        # Example bar chart using Matplotlib pyplot
        self.canvas.axes.bar(company_list, company_wise_stock_value, color='#22577A')

        for i, value in enumerate(company_wise_stock_value):
            self.canvas.axes.text(i, value + 0.5, str(value), ha='center', va='bottom')

        # Set labels and title
        self.canvas.axes.set_xlabel("Company")
        self.canvas.axes.set_ylabel("Stock Value")
        self.canvas.axes.set_title("Stock Value based on Company")

        # Refresh canvas
        self.canvas.draw()

    def trend_chart(self):
        option = self.trend_chart_typeCombo.currentIndex()
        if option == 0:
            last_item = len(self.salesDataAnalysis.daywise_sales_data)
            first_item = last_item - 7
            trend_data = self.salesDataAnalysis.daywise_sales_data[first_item: last_item]

        if option == 1:
            last_item = len(self.salesDataAnalysis.daywise_sales_data)
            first_item = last_item - 30
            trend_data = self.salesDataAnalysis.daywise_sales_data[first_item: last_item]

        date = []
        sales_value = []
        for i in range(len(trend_data)):
            date.append(trend_data[i][0])
            sales_value.append(trend_data[i][2])

        self.canvas_trend.axes.clear()
        self.canvas_trend.axes.plot(date, sales_value, label="Trend", color="blue")
        self.canvas_trend.axes.set_title("Trend Analysis")
        self.canvas_trend.axes.tick_params(axis='x', rotation=90)

        # x_tick_position = np.arange(0, len(date), step=30)
        # print(x_tick_position)
        # self.canvas_trend.axes.set_xticks(date[x_tick_position])

        self.canvas_trend.draw()

    def display_chart(self):
        option = self.chart_typeCombo.currentIndex()
        if option == 0:
            self.stockByMedTypeChart()
        elif option == 1:
            self.stockValueByMedTypeChart()
        elif option == 2:
            self.stockByCompanyChart()
        elif option == 3:
            self.stockValueByCompanyChart()

        self.trend_chart()


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=4, height=4, dpi=90):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)


class addNewCompanyName(QDialog):
    def __init__(self, insofDashboard):
        super().__init__()
        self.dashboard = insofDashboard
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Add Company Name")
        self.verticalLayout = QVBoxLayout()

        self.addLabel = QLabel("Add New Company")
        self.addLabel.setStyleSheet("font-size: 18px; font-family: Bahnschrift; font-weight: bold")

        self.addTypeInput = QLineEdit()
        self.addTypeInput.setPlaceholderText("Company Name")
        self.addTypeInput.setObjectName("InputBox")

        self.addButton = QPushButton("ADD COMPANY")
        self.addButton.setObjectName("adminChangeButton")
        self.addButton.pressed.connect(self.updateCompanyDatabase)

        self.verticalLayout.addWidget(self.addLabel)
        self.verticalLayout.addWidget(self.addTypeInput)
        self.verticalLayout.addWidget(self.addButton)
        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.verticalLayout)

    def updateCompanyDatabase(self):
        companyName = self.addTypeInput.text()
        try:
            connection = sqlite3.connect("Database.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO company_list (company_name) VALUES (?)", (companyName,))

            connection.commit()
            cursor.close()
            connection.close()
            self.dashboard.collect_company_data()
            self.close()


        except Exception as e:
            print(e)


class addNewMedicineType(QDialog):
    def __init__(self, insofDashboard):
        super().__init__()
        self.dashboard = insofDashboard
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Update Medicine Type")
        self.verticalLayout = QVBoxLayout()

        self.addLabel = QLabel("Add New Type")
        self.addLabel.setStyleSheet("font-size: 18px; font-family: Bahnschrift; font-weight: bold")

        self.addTypeInput = QLineEdit()
        self.addTypeInput.setPlaceholderText("Medicine Type")
        self.addTypeInput.setObjectName("InputBox")

        self.addButton = QPushButton("ADD MED TYPE")
        self.addButton.setObjectName("adminChangeButton")
        self.addButton.pressed.connect(self.updateMedTypeDatabase)

        self.verticalLayout.addWidget(self.addLabel)
        self.verticalLayout.addWidget(self.addTypeInput)
        self.verticalLayout.addWidget(self.addButton)
        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.verticalLayout)

    def updateMedTypeDatabase(self):
        medType = self.addTypeInput.text()
        # print(medType)
        try:
            connection = sqlite3.connect("Database.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO medicine_type (type_name) VALUES (?)", (medType,))

            connection.commit()
            cursor.close()
            connection.close()
            self.dashboard.collect_medType_data()
            self.close()


        except Exception as e:
            print(e)


# ------------ SALES SECTION END ------------- #

class DataAnalysis:
    def __init__(self):
        super().__init__()
        try:
            self.connection = sqlite3.connect("Database.db")
            sql_query = "SELECT * FROM med_inventory"

            dataframe = pd.read_sql(sql_query, self.connection)

            self.connection.close()

            self.totalStockQty = dataframe["stock_qty"].sum()
            self.totalStockValue = (dataframe["stock_qty"] * dataframe["inbound_price"]).sum()
            self.totalSalesValue = round((dataframe["stock_qty"] * dataframe["outbound_price"]).sum(), 2)
            self.opportunity = round(self.totalSalesValue - self.totalStockValue, 2)

            self.dosage_form = dataframe["dosage_form"].unique()
            self.dosage_form_qty = []
            self.dosage_form_stock_value = []
            for i in self.dosage_form:
                self.dosage_form_qty.append(dataframe[dataframe["dosage_form"] == i]["stock_qty"].sum())
                dataframe_by_dosage = dataframe[dataframe["dosage_form"] == i]
                total_stock_value_by_dosage = (
                            dataframe_by_dosage["stock_qty"] * dataframe_by_dosage["inbound_price"]).sum()
                self.dosage_form_stock_value.append(round(total_stock_value_by_dosage))

            # print(self.dosage_form_stock_value)

            self.companyName = dataframe["company"].unique()
            self.qty_by_company = []
            self.stock_value_by_company = []
            for i in self.companyName:
                self.qty_by_company.append(dataframe[dataframe["company"] == i]["stock_qty"].sum())
                dataframe_by_company = dataframe[dataframe["company"] == i]
                total_stock_value_by_company = (
                            dataframe_by_company["stock_qty"] * dataframe_by_company["inbound_price"]).sum()
                self.stock_value_by_company.append(round(total_stock_value_by_company))
            # print(self.stock_value_by_company)

        except Exception as e:
            print(e)


class SalesDataAnalysis:
    def __init__(self):
        super().__init__()
        try:
            self.connection = sqlite3.connect("Database.db")
            sql_query = "SELECT * FROM sales_data"

            dataframe = pd.read_sql(sql_query, self.connection)

            self.connection.close()

            list_of_date = dataframe["Date"].unique()
            # print(list_of_date)
            list_of_invoice = dataframe["invoice_No"].unique()
            # print(list_of_invoice)

            self.daywise_sales_data = []
            for i in list_of_date:
                temp_list_of_invoice = dataframe[dataframe["Date"] == i]["invoice_No"].unique()
                for j in temp_list_of_invoice:
                    temp_dataframe = dataframe[(dataframe["Date"] == i) & (dataframe["invoice_No"] == j)]
                    total_sales_date_invoice = (temp_dataframe["unit_price"] * temp_dataframe["sell_qty"]).sum()
                    self.daywise_sales_data.append((i[:10], j, round(total_sales_date_invoice, 2)))

        except Exception as e:
            print(e)


# -------- POP UP WINDOWS -------- #

class WarningBox(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")
        content = message
        self.setText(content)


class successfulRegister(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Successful")
        content = "Successfully Registered"
        self.setText(content)


class failedLogin(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Not Successful")
        content = "Wrong User Name & Password!"
        self.setText(content)


class registrationFailed(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Not Successful")
        content = "Registration Failed, please try again!"
        self.setText(content)


class failedToUpdate(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Not Successful")
        content = "Failed to update, please try again!"
        self.setText(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Style_Sheet)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

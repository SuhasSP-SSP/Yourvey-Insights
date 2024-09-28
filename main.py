import mysql.connector
from mysql.connector import Error
from time import sleep
import json
import csv
import pickle
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from ui import *
import datetime
import icons
import sys
_translate = QtCore.QCoreApplication.translate

cwd = os.getcwd()
SettingsSaveCount = 0
ROOTpwd = "root"
ufolderPath = ""

class function(Ui_MainWindow):
    def gui_functions(self, MainWindow):

        self.submenus.setCurrentIndex(0)

####================ GUI =================####

        movie = QMovie(":/images/loader.gif") 
        self.loader.setMovie(movie)
        #QApplication.processEvents()

        def startAnimation(): 
            movie.start() 

        def stopAnimation(): 
            movie.stop() 


#### View Existing Survey ####
        self.get_data_button = self.refreshButton
        self.result_table = self.listSurveys
        self.listSurveys.setSortingEnabled(True) #Sorting table
        self.header = self.listSurveys.horizontalHeader() #Column Names Set
        self.header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents) #Survey ID and Date      
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch) #Strech only title
        self.listSurveys.verticalHeader().setVisible(False) #To remove count


        def show_context_menu(pos):
            context_menu = QMenu(self.result_table)
            view_action = context_menu.addAction("View Report")
            add_action = context_menu.addAction("Add Questions")
            remove_action = context_menu.addAction("Delete Survey")

            action = context_menu.exec_(self.result_table.mapToGlobal(pos))

            if action == add_action:
                add_questions()

            elif action == remove_action:
                delete_survey()
            elif action == view_action:
                view_report()


#### Add Questions ####
        def New_Survey():
            connection = connect_to_db()
            if connection:
                survey_name = self.input_projectname.text()
                try:
                    cursor = connection.cursor()
                    current_date = datetime.date.today().strftime("%Y-%m-%d")
                    cursor.execute("INSERT INTO Surveys (name, date_created) VALUES (%s, %s)", (survey_name, current_date))                    
                    survey_id = cursor.lastrowid
                    connection.commit()
                    cursor.close()
                    print("Survey created successfully with ID: {}".format(survey_id))
                    self.input_projectname.clear()
                    create_survey_table(connection, survey_id)
                    create_surveyee_view(connection, survey_id)
                    create_admin_view(connection, survey_id)

                except mysql.connector.Error as e:
                    print("Error:", e)
        self.continueButton.clicked.connect(New_Survey)


        def get_all_data_from_db():
            try:
                connection = connect_to_db()
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM surveys;"
                cursor.execute(query)
                result = cursor.fetchall()
                return result

            except Exception as e:
                print("get data fail")
                print(e)

            finally:
                connection = connect_to_db()
                if connection:
                    connection.close()

        def selectedSurveyID():
            try:
                selectedRowIndex = self.listSurveys.currentRow()
                item = self.listSurveys.item(selectedRowIndex, 0)
                return (item.text())
            except Exception as e:
                print(e)

        def selectedSurveyName():
            try:
                selectedRowIndex = self.listSurveys.currentRow()
                item = self.listSurveys.item(selectedRowIndex, 1)
                return (item.text())
            except Exception as e:
                print(e)

        def add_questions():
            self.submenus.setCurrentIndex(3)
            self.addQ.hide()
            self.finishB.hide()

            self.input_question.clear()

            self.mcqNOTE.hide()
            self.mcqBOX.hide()
            self.op1.clear()
            self.op2.clear()
            self.op3.clear()
            self.op4.clear()
            self.op5.clear()

            self.openendedRB.setChecked(False)
            self.mcqRB.setChecked(False)
            self.yrnRB.setChecked(False)

            self.addQuestions.update()
            
            def selectedQtype():
                L = [self.openendedRB.isChecked(), self.yrnRB.isChecked()]
                return any(L)
                    
            def insertOQ():
                connection = connect_to_db()
                if connection:
                    survey_id = selectedSurveyID()
                    question_text = self.input_question.toPlainText()
                    question_type = "OpenEnded"
                    add_question_to_survey(connection, survey_id, question_text, question_type)
                    
                    print("\nOpen-ended question added successfully.")

            def insertYNQ():
                connection = connect_to_db()
                if connection:
                    survey_id = selectedSurveyID()
                    question_text = self.input_question.toPlainText()
                    question_type = "(Yes/No)"
                    add_question_to_survey(connection, survey_id, question_text, question_type)
                    print("\nYes/No question added successfully.")

            def insertMCQ():
                connection = connect_to_db()
                if connection:
                    survey_id = selectedSurveyID()
                    question_text = self.input_question.toPlainText()
                    question_type = "MultipleChoice"
                    options = MCQdetails("data")
                    question_data = {"question_type": question_type, "options": options}
                    add_question_to_survey(connection, survey_id, question_text, question_data)
                    print("\nMCQ added successfully.")
            
            def disconnect_signals():
                self.addQ.disconnect()
                self.finishB.disconnect()

            def connect_signals():
                if self.openendedRB.isChecked():
                    self.addQ.clicked.connect(nextOQ)
                    self.finishB.clicked.connect(finishOQ)
                elif self.mcqRB.isChecked():
                    self.addQ.clicked.connect(nextMCQ)
                    self.finishB.clicked.connect(finishMCQ)
                elif self.yrnRB.isChecked():
                    self.addQ.clicked.connect(nextYNQ)
                    self.finishB.clicked.connect(finishYNQ)

            def finishOQ():
                insertOQ()
                self.submenus.setCurrentIndex(2)
                self.openendedRB.setChecked(False)
                self.mcqRB.setChecked(False)
                self.yrnRB.setChecked(False)
                self.addQuestions.update()

                connection = connect_to_db()
                survey_id = selectedSurveyID()
                filename = "survey_{}.py".format(survey_id)
                export_surveyee_code(connection, survey_id, filename)
                filename = "admin_view_{}.py".format(survey_id)
                

            def finishYNQ():
                insertYNQ()
                self.submenus.setCurrentIndex(2)
                self.openendedRB.setChecked(False)
                self.mcqRB.setChecked(False)
                self.yrnRB.setChecked(False)
                self.addQuestions.update()

                connection = connect_to_db()
                survey_id = selectedSurveyID()
                filename = "survey_{}.py".format(survey_id)
                export_surveyee_code(connection, survey_id, filename)
                filename = "admin_view_{}.py".format(survey_id)

            def finishMCQ():
                insertMCQ()
                self.submenus.setCurrentIndex(2)
                self.openendedRB.setChecked(False)
                self.mcqRB.setChecked(False)
                self.yrnRB.setChecked(False)

                self.addQuestions.update()
                connection = connect_to_db()
                survey_id = selectedSurveyID()
                filename = "survey_{}.py".format(survey_id)
                export_surveyee_code(connection, survey_id, filename)
                filename = "admin_view_{}.py".format(survey_id)

            def nextOQ():
                insertOQ()
                add_questions()
                self.openendedRB.setChecked(False)
                self.mcqRB.setChecked(False)
                self.yrnRB.setChecked(False)
                self.addQuestions.update()

            def nextMCQ():
                insertMCQ()
                add_questions()
                self.openendedRB.setChecked(False)
                self.mcqRB.setChecked(False)
                self.yrnRB.setChecked(False)
                self.addQuestions.update()

            def nextYNQ():
                insertYNQ()
                add_questions()
                self.openendedRB.setChecked(False)
                self.mcqRB.setChecked(False)
                self.yrnRB.setChecked(False)
                self.addQuestions.update()
            
            def MCQdetails(v):
                if self.mcqRB.isChecked():
                    self.mcqNOTE.show()
                    self.mcqBOX.show()
                    self.addQuestions.update()
                    options = []
                    opt = [self.op1.toPlainText(), self.op2.toPlainText(), self.op3.toPlainText(), self.op4.toPlainText(), self.op5.toPlainText()]
                    for i in opt:
                        if len(i) > 0:
                            options.append(i)
                    if len(options) >= 2 and v == "valid":
                        return True
                    elif v == "data":
                        return options
                else:
                    self.mcqNOTE.hide()
                    self.mcqBOX.hide()
                    self.addQuestions.update()  

            def text_change():
                current_length = len(self.input_question.toPlainText())
                v = "valid"
                if current_length > 1 and MCQdetails(v) == True:
                    self.addQ.show()
                    self.finishB.show()
                    self.addQuestions.update()
                    # Disconnect signals to avoid multiple connections
                    disconnect_signals()
                    # Connect signals
                    connect_signals()
                    
                elif current_length > 1 and selectedQtype():  # Show
                    self.addQ.show()
                    self.finishB.show()
                    self.addQuestions.update()
                    disconnect_signals()
                    connect_signals()


                elif current_length <= 1 or not selectedQtype():  # Hide
                    self.addQ.hide()
                    self.finishB.hide()

                    if self.mcqRB.isChecked() == False:
                        self.mcqNOTE.hide()
                        self.mcqBOX.hide()
                        
                    else:
                        self.mcqNOTE.show()
                        self.mcqBOX.show()

                    self.addQuestions.update()
                QApplication.processEvents()

            self.input_question.textChanged.connect(text_change)

            self.op1.textChanged.connect(text_change)
            self.op2.textChanged.connect(text_change)
            self.op3.textChanged.connect(text_change)
            self.op4.textChanged.connect(text_change)
            self.op5.textChanged.connect(text_change)

            self.openendedRB.clicked.connect(text_change)
            self.mcqRB.clicked.connect(text_change)
            self.yrnRB.clicked.connect(text_change)
                
        def delete_survey(): 
            connection = connect_to_db()
            if connection:
                try:
                    cursor = connection.cursor()
                    queries = [
                    'USE yourveyinsights;',    
                    'drop table survey_{};'.format(selectedSurveyID()), sleep(2),
                    'drop table questions_{};'.format(selectedSurveyID()), sleep(1),
                    'drop view surveyeeview_{}'.format(selectedSurveyID()), sleep(1),
                    'drop view adminview_{};'.format(selectedSurveyID()), sleep(1),
                    'delete from surveys where survey_id = {};'.format(selectedSurveyID())
                    ]
                    for i in queries:
                        cursor.execute(i)                    
                    connection.commit()
                    cursor.close()
                    print("Survey removed successfully with ID: {}".format(selectedSurveyID()))
                    on_get_data_btn_clicked()
                    self.listSurveys.update()
                except mysql.connector.Error as e:
                    print("Error:", e)

        def view_report():
            connection = connect_to_db()
            survey_id = selectedSurveyID()
            if not os.path.isdir("Result and Stats"):
                os.makedirs("Result and Stats")
            filename = "Report_{}.csv".format(survey_id)                
            filename = "{}\Result and Stats\{}".format(cwd, filename) 

            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT s.question_id, q.question_text, q.question_type, s.sessionID, s.answer FROM survey_{0} s JOIN questions_{0} q ON s.question_id = q.question_id ORDER BY s.sessionID;".format(survey_id))
                    rows = cursor.fetchall()
                    cursor.close()
                    SurveyNameTitle = ("Survey: "+ selectedSurveyName() + " ["+str(selectedSurveyID())+"]")
                    self.SurveyName.setText(SurveyNameTitle)
                    with open(filename, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow(['Question ID', 'Question Text', 'Question Type',' Session ID', 'Answer'])
                        x = None 
                        for row in rows:
                            question_id, question_text, question_type, session_id, answer = row
                            # Check if it's a new session
                            if session_id != x:
                                x = session_id  # Update the current session ID
                                printed_session_id = False  # Reset 
                            # Write to CSV
                            csv_writer.writerow([question_id, question_text, question_type, session_id, answer])

                    print(f"Data exported to {filename}")
                except Exception as e:
                    print(f"Error: {e}")  
            
            import pandas as pd
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
            from matplotlib.figure import Figure
            from matplotlib.ticker import AutoLocator # Import the AutoLocator class

            def graph():
                survey_id = selectedSurveyID()
                connection = connect_to_db()
                # Retrieve the data from the SQL query
                query = "SELECT question_id, COUNT(answer) AS count_answers FROM survey_{0} GROUP BY question_id;".format(survey_id)
                df = pd.read_sql(query, connection)

                # Get the survey name from the database
                query = "SELECT name FROM surveys WHERE id = {0};".format(survey_id)
                survey_name = selectedSurveyName()
                connection.close()

                # Create the figure and the axes
                fig, ax = plt.subplots(num=f"Survey {survey_id}: {survey_name}")

                # Create the bar graph
                plt.bar(df['question_id'], df['count_answers'])
                plt.xlabel('Question ID')
                plt.ylabel('Number of Answers')
                plt.title('Answers per Question ID')
                # Loop through the bars and add text labels
                for x, y in zip(df['question_id'], df['count_answers']):
                    plt.text(x, y + 0.1, int(x), ha='center', va='bottom')
                # Set both scales for whole numbers only using AutoLocator
                ax.xaxis.set_major_locator(AutoLocator())
                ax.yaxis.set_major_locator(AutoLocator())
                plt.show()


            def viewReport():
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor(dictionary=True)
                    query = "SELECT s.question_id, q.question_text, q.question_type, s.sessionID, s.answer FROM survey_{0} s JOIN questions_{0} q ON s.question_id = q.question_id ORDER BY s.sessionID;".format(survey_id)
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result

                except Exception as e:
                    print("Error:")
                    print(e)

                finally:
                    connection = connect_to_db()
                    if connection:
                        connection.close()

            result = viewReport()        
            if result:
                self.submenus.setCurrentIndex(6)
                self.reportTable.update()
                self.reportTable.setRowCount(len(result))
                for row, item in enumerate(result):
                    column_1_item = QTableWidgetItem(str(item['question_id']))
                    column_2_item = QTableWidgetItem(str(item['question_text']))
                    column_3_item = QTableWidgetItem(str(item['question_type']))
                    column_4_item = QTableWidgetItem(str(item['sessionID']))
                    column_5_item = QTableWidgetItem(str(item['answer']))
                    
                    self.reportTable.setItem(row, 0, column_1_item)
                    self.reportTable.setItem(row, 1, column_2_item)
                    self.reportTable.setItem(row, 2, column_3_item)
                    self.reportTable.setItem(row, 3, column_4_item)
                    self.reportTable.setItem(row, 4, column_5_item)

                self.reportTable.update()
                self.stats.clicked.connect(graph)
            else:
                print(Error)
                  

#### Settings ####
        # Checked = Close Eye = True
        def passwordEye_init():
            self.input_MySQL_admin_password_info.setEchoMode(QtWidgets.QLineEdit.Password)
            self.passwordEye.setChecked(True)
        self.settingsButton.clicked.connect(passwordEye_init)

        def passwordEye_Toggle():
            if self.passwordEye.isChecked():
                self.input_MySQL_admin_password_info.setEchoMode(QtWidgets.QLineEdit.Password)
            else:
                self.input_MySQL_admin_password_info.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.passwordEye.clicked.connect(passwordEye_Toggle)

        def save_settings_to_file(path, updated_ROOTpwd):
            global ROOTpwd
            ROOTpwd = updated_ROOTpwd
            file_name = 'settings.bin'
            file_path = os.path.join(cwd, file_name)
            try:
                with open(file_path, 'wb') as binary_file:
                    settings_data = {'ROOTpwd': ROOTpwd, 'path': path}
                    pickle.dump(settings_data, binary_file)
                print('Settings saved to', file_path)
            except Exception as e:
                print('Error saving settings:', e)

        def load_settings_from_file():
            file_name = 'settings.bin'
            file_path = os.path.join(cwd, file_name)
            try:
                with open(file_path, 'rb') as binary_file:
                    settings_data = pickle.load(binary_file)
                    return settings_data
            except Exception as e:
                print('Error loading settings:', e)
                return None

        def saveSettings():
            global SettingsSaveCount
            SettingsSaveCount += 1
            path = self.input_Custom_suvrey_location.text()
            updated_ROOTpwd = self.input_MySQL_admin_password_info.text()
            # Save the settings to a binary file
            save_settings_to_file(path, updated_ROOTpwd)

        def defaultSettings():
            last_saved_settings = load_settings_from_file()

            if last_saved_settings is not None:
                # Apply the last saved settings
                self.input_MySQL_admin_password_info.setText(last_saved_settings['ROOTpwd'])
                self.input_Custom_suvrey_location.setText(last_saved_settings['path'])
                global ROOTpwd
                ROOTpwd = last_saved_settings['ROOTpwd']
            else:
                # Use default settings if no saved settings are found
                self.input_MySQL_admin_password_info.setText("root")
                self.input_Custom_suvrey_location.setText(cwd)
                SettingsSaveCount = 0

        #Browse Folder Location
        def selectFolderPath():
            browse = QFileDialog.directory #Pops out the window to select folder
            global ufolderPath
            ufolderPath = QFileDialog.getExistingDirectory() #Gives path in text as the response from the above selected folder
            self.input_Custom_suvrey_location.setText(ufolderPath)

        def on_get_data_btn_clicked():
            result = get_all_data_from_db()
            if result:
                self.result_table.setRowCount(len(result))
                for row, item in enumerate(result):
                    column_1_item = QTableWidgetItem()
                    column_2_item = QTableWidgetItem(str(item['name']))
                    column_3_item = QTableWidgetItem(str(item['date_created']))
                    column_1_item.setData(Qt.EditRole, item['survey_id'])
                    self.result_table.setItem(row, 0, column_1_item)
                    self.result_table.setItem(row, 1, column_2_item)
                    self.result_table.setItem(row, 2, column_3_item)

                    # Connect the right click custom context menu to the table
                    self.result_table.setContextMenuPolicy(3)  
                    self.result_table.customContextMenuRequested.connect(show_context_menu)

            else:
                print(Error)


        def add_question_to_survey(connection, survey_id, question_text, question_data):
            question_table_name = "Questions_{}".format(survey_id)
            question_type = None
            options = None

            if isinstance(question_data, dict):
                if question_data["question_type"] == "MultipleChoice":
                    question_type = "MultipleChoice"
                    options = json.dumps(question_data.get("options", []))
            else:
                if question_data == "(Yes/No)":
                    question_type = "(Yes/No)"
                elif question_data == "OpenEnded":
                    question_type = "OpenEnded"

            query = """
            INSERT INTO {} (question_text, question_type, options)
            VALUES (%s, %s, %s)
            """.format(question_table_name)

            try:
                cursor = connection.cursor()
                cursor.execute(query, (question_text, question_type, options))
                connection.commit()
                cursor.close()
            except Error as e:
                print("Error:", e)

        def initialize(connection, queries):
            startAnimation()
            cursor = connection.cursor()
            for query in queries:
                cursor.execute(query)
            connection.commit()
            cursor.close()
            stopAnimation()
            
        def connect_to_db():
            try:
                connection = mysql.connector.connect(host='localhost', user='root', password=ROOTpwd, database='yourveyinsights')
                return connection
            except Error:
                print(Error)
                print("Initialising the Database...")
                connection = mysql.connector.connect(host='localhost', user='root', password=ROOTpwd)
                queries = [
                    'CREATE DATABASE yourveyinsights;', sleep(3),
                    'USE yourveyinsights;',
                    'CREATE TABLE Surveys (survey_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, date_created DATE);',
                    ]
                initialize(connection, queries)
                sleep(4)
                connection = mysql.connector.connect(host="localhost", user="root", password=ROOTpwd, database="yourveyinsights")
                return connection

        def create_survey_table(connection, survey_id):
            question_table_name = "Questions_{}".format(survey_id)
            survey_table_name = "Survey_{}".format(survey_id)

            query = """
            CREATE TABLE {} (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                question_text TEXT NOT NULL,
                question_type ENUM('(Yes/No)', 'OpenEnded', 'MultipleChoice') NOT NULL,
                options JSON
            )
            """.format(question_table_name)

            try:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                cursor.close()
            except Error as e:
                print("Error:", e)

            query = """
            CREATE TABLE {} (
                response_id INT AUTO_INCREMENT PRIMARY KEY,
                question_id INT,
                sessionID VARCHAR(255),
                answer TEXT,
                FOREIGN KEY (question_id) REFERENCES {}(question_id)
            )
            """.format(survey_table_name, question_table_name)

            try:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                cursor.close()
            except Error as e:
                print("Error:", e)

        def create_surveyee_view(connection, survey_id):
            question_table_name = "Questions_{}".format(survey_id)
            survey_table_name = "Survey_{}".format(survey_id)
            surveyee_view_name = "SurveyeeView_{}".format(survey_id)

            query = """
            CREATE OR REPLACE VIEW {} AS
            SELECT {}.question_text, {}.answer
            FROM {}
            LEFT JOIN {} ON {}.question_id = {}.question_id
            """.format(surveyee_view_name, question_table_name, survey_table_name, question_table_name, survey_table_name, question_table_name, survey_table_name)

            try:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                cursor.close()
            except Error as e:
                print("Error:", e)

        def create_admin_view(connection, survey_id):
            question_table_name = "Questions_{}".format(survey_id)
            survey_table_name = "Survey_{}".format(survey_id)
            admin_view_name = "AdminView_{}".format(survey_id)

            query = """
            CREATE OR REPLACE VIEW {} AS
            SELECT {}.question_text, COUNT(*) AS total_responses
            FROM {}
            LEFT JOIN {} ON {}.question_id = {}.question_id
            GROUP BY {}.question_id
            """.format(admin_view_name, question_table_name, survey_table_name, question_table_name, survey_table_name, question_table_name, survey_table_name)

            try:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                cursor.close()

            except Error as e:
                print("Error:", e)

        def export_surveyee_code(connection, survey_id, filename):
            question_table_name = "Questions_{}".format(survey_id)
            survey_table_name = "Survey_{}".format(survey_id)

            query = "SELECT question_text, question_type, options FROM {}".format(question_table_name)


            if len(ufolderPath) > 2:
                surveys_folder = os.path.join(ufolderPath, "Surveys")
                if not os.path.isdir(surveys_folder):
                    os.makedirs(surveys_folder)

            elif not os.path.isdir("Surveys"):
                os.makedirs("Surveys")
            filename = "{}\Surveys\{}".format(cwd, filename)

            try:
                cursor = connection.cursor()
                cursor.execute(query)
                questions = cursor.fetchall()
                cursor.close()

                with open(filename, "w+") as code_file:
                    code_file.write("# Python code for surveyee view:\n")
                    code_file.write("# Survey ID: {}\n\n".format(survey_id))

                    code_file.write("import mysql.connector\n")
                    code_file.write("from mysql.connector import Error\n")
                    code_file.write("import uuid\n\n")

                    code_file.write("def generate_session_id():\n")
                    code_file.write("    return uuid.uuid4().hex\n\n")

                    code_file.write("def take_survey(connection):\n")
                    code_file.write("    try:\n")
                    code_file.write("        session_id = generate_session_id()\n")

                    for i, (question_text, question_type, options) in enumerate(questions, start=1):
                        if question_type == "(Yes/No)":
                            code_file.write("        while True:\n")
                            code_file.write("            answer{} = input('{} (Yes/No): '.format('question_text'))\n".format(i, question_text))
                            code_file.write("            answer{} = answer{}.lower()\n".format(i, i))
                            code_file.write("            if answer{} in ['yes', 'no', 'y', 'n']:\n".format(i))
                            code_file.write("                break\n")
                            code_file.write("            else:\n")
                            code_file.write("                print('Invalid response. Please enter either Yes (y) or No (n).')\n")

                        elif question_type == "OpenEnded":
                            code_file.write("        while True:\n")
                            code_file.write("            answer{} = input('{}: '.format('question_text'))\n".format(i, question_text))
                            code_file.write("            if len(answer{}) > 0:\n".format(i))
                            code_file.write("                break\n")
                            code_file.write("            else:\n")
                            code_file.write("                print('Invalid response. Your response cannot be empty.')\n")

                        elif question_type == "MultipleChoice":
                            if options is not None:
                                options = json.loads(options)
                                code_file.write("        options{} = {}\n".format(i, options))
                                code_file.write("        print('{}')\n".format(question_text))
                                for option_index, option_text in enumerate(options, start=1):
                                    code_file.write("        print('{}. {}')\n".format(option_index, option_text))
                                code_file.write("        while True:\n")
                                code_file.write("            answer{} = input('(Enter the option number): ')\n".format(i))
                                code_file.write("            if answer{} in map(str, range(1, {num_options} + 1)):\n".format(i, num_options=len(options)))
                                code_file.write("                break\n")
                                code_file.write("            else:\n")
                                code_file.write("                print('Invalid response. Please select a valid option.')\n".format(i=i))

                    code_file.write("        query = 'INSERT INTO {survey_table_name} (question_id, sessionID, answer)'+'VALUES (%s, %s, %s)'\n".format(survey_table_name=survey_table_name))
                    code_file.write("        cursor = connection.cursor()\n")

                    for i, (_, question_type, _) in enumerate(questions, start=1):
                        code_file.write("        cursor.execute(query, ({}, session_id, answer{}))\n".format(i, i))

                    code_file.write("        connection.commit()\n")
                    code_file.write("        cursor.close()\n")
                    code_file.write("        print('Survey response saved successfully.')\n")
                    code_file.write("    except Error as e:\n")
                    code_file.write("        print('Error:', e)\n")
                    code_file.write("    except ValueError as ve:\n")
                    code_file.write("        print('ValueError:', ve)\n")

                    code_file.write("def main():\n")
                    code_file.write("    connection = mysql.connector.connect(\n")
                    code_file.write("        host='localhost',\n")
                    code_file.write("        user='root',\n")
                    code_file.write("        password='{}',\n".format(ROOTpwd))
                    code_file.write("        database='yourveyinsights'\n")
                    code_file.write("    )\n")
                    code_file.write("    if connection:\n")
                    code_file.write("        take_survey(connection)\n")
                    code_file.write("        connection.close()\n\n")

                    code_file.write("main()")

                print("{} exported successfully.".format(filename))
            except Error as e:
                print("Error:", e)
                                
        #Initial Triggers
        defaultSettings()

# ↑↑↑↑↑ GUI ↑↑↑↑↑ #

####################---- Push Buttons START ----####################

        # Navigation Buttons Home Screen for Different Screens 
        self.create_new_Button.clicked.connect(lambda : self.submenus.setCurrentIndex(1)) 
        self.open_existing_Button.clicked.connect(lambda : self.submenus.setCurrentIndex(2))
        self.settingsButton.clicked.connect(lambda : self.submenus.setCurrentIndex(4))
        self.About_Button.clicked.connect(lambda : self.submenus.setCurrentIndex(5))
        self.exit_Button.clicked.connect(MainWindow.close)

        # Home Buttons
        self.homeButtonList = [self.homeButton, self.homeButton_2, self.homeButton_3, self.homeButton_4, self.homeButton_5, self.homeButton_6]
        for self.homeButton in self.homeButtonList:
            self.homeButton.clicked.connect(lambda : self.submenus.setCurrentIndex(0))
        
        #Continue Buttons
        self.continueButton.clicked.connect(lambda : self.submenus.setCurrentIndex(2)) #New -> View Existing Surveys1

        #Get Data
        self.get_data_button.clicked.connect(on_get_data_btn_clicked)

        #Settings
        self.selectFolder.clicked.connect(selectFolderPath)
        self.input_MySQL_admin_password_info.setText(ROOTpwd)
        
        self.saveButton.clicked.connect(saveSettings)
        self.settingsButton.clicked.connect(defaultSettings)

####################---- Push Buttons END ----####################


# Invoking the Application
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = function()
ui.setupUi(MainWindow)
ui.gui_functions(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
# Yourvey Insights 📊

Yourvey Insights is an user-friendly survey creation and reporting application, designed for simplicity and insightful data analysis. Developed using Python, PyQt5 for a visually appealing desktop interface, and MySQL for robust data management, Yourvey Insights provides an invaluable tool for educators, students, researchers, and anyone needing to create, conduct, and analyze surveys with ease. Transform the survey process into a seamless and insightful experience with features including various question types, real-time data capture, CSV and potentially expanded report exporting (future PDF/Excel), visually engaging bar graphs for statistical insights, and enhanced security with password protection for MySQL admin access.

> Developed as a Computer Science Project for Class 12 CBSE Examinations (AISSCE 2023-2024).

## Features ✨

- **Quick Survey Creation:** Design surveys effortlessly with a visually driven user interface.
- **Versatile Question Types:**  Implement a variety of question formats to gather comprehensive data:
    - **Open-ended Questions:** Collect free-text responses for qualitative insights.
    - **Multiple Choice Questions (MCQ):** Offer pre-defined options with up to 5 choices for structured responses.
    - **Yes/No Questions:**  Gather binary responses for quick and decisive data.
- **MySQL Backend:** Utilizes a secure and reliable MySQL database to store survey definitions, responses, and settings, ensuring data integrity and efficient retrieval.
- **Comprehensive Reporting & Export:**
    - **CSV Report Exporting:** Easily export detailed survey responses into CSV format for in-depth analysis in spreadsheet software or other tools.
    - **Statistical Bar Graphs:** Visualize key survey statistics with dynamically generated bar graphs, offering insights into question response distributions (e.g., Questions Shown vs. Questions Answered).
    - *(Future Enhancement: Potential for expanded export formats like PDF and Excel, as mentioned in "Scope of Improvements" for enhanced compatibility.)*
- **Customizable Data Location:** Option to configure and customize the location where survey data and application settings are stored.
- **User-Friendly PyQt5 Interface:** Enjoy a visually appealing and easy-to-navigate desktop application interface built with PyQt5, ensuring a smooth user experience across platforms.
- **Cross-Platform Compatibility:** Runs seamlessly on Windows, macOS, and Linux operating systems, leveraging Python's cross-platform capabilities.

---
## Usage 📋

1. **Download or Clone from GitHub:**
   ```
   git clone https://github.com/SuhasSP-SSP/Yourvey-Insights
   ```
   
   ```
   cd Yourvey-Insights
   ```
   
2. **Database Setup (MySQL):**
   - Ensure you have MySQL server installed and running locally.
   - Configure database connection parameters: Host (`localhost` by default), User (`root` or your MySQL user), Password (`root` or your MySQL password - configurable within the app), and Database name (`yourveyinsights` - default, can be customized).  These settings can be adjusted within the application's "Settings" panel.

3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the Application:** Execute the main Python `main.py` to launch the Yourvey Insights application.
   ```
   python main.py
   ```

#### Main Workflows 🛠️
1. **Create a New Survey:**
    -  Launch Yourvey Insights and click "Create New Survey" from the Home screen.
    -  Enter a descriptive "Survey Name" for your new survey.
    -  Proceed to the "Add Questions" section.
2. **Add Questions to Your Survey:**
    -  Within the "Add Questions" interface, select the desired question type: "Open-ended", "MCQ", or "Yes/No".
    -  Enter your question text in the provided input area.
    -  For "MCQ" questions, input up to 5 answer choices in the designated option fields.
    -  Click the "+" button to add each question to the survey. Use the "Finish" button when done adding questions for the survey.
3. **View Existing Surveys & Reports:**
    -  From the Home screen, select "View Existing Surveys".
    -  The application will display a table listing created surveys with their IDs and creation dates. Click "Refresh" to update the list.
    -  Right-click on a survey in the list to access a context menu with options:
        -  **"View Report"**: Generate and display a detailed report of survey responses in a tabular format within the application.
        -  **"Add Questions"**: Return to the "Add Questions" interface to modify or add more questions to the selected survey.
        -  **"Delete Survey"**: Permanently remove the selected survey and associated data (use with caution!).
4. **Export Survey Data (CSV):**
    -  After viewing a survey report, use the export functionality (likely a button labeled "Export" or similar in the report view) to save the survey data as a CSV file.
5. **Visualize Survey Statistics (Bar Graphs):**
    -  From the survey report view, click the "Stats" button to generate a bar graph visualizing "Questions Shown vs. Questions Answered".
6. **Configure Settings:**
    -  Navigate to the "Settings" screen from the Home screen.
    -  **MySQL Admin Password:** Set or modify the password used to connect to the MySQL database.
    -  **Customize Data Location:** Specify a custom folder location for storing survey data and application settings if you wish to change the default location.
    -  Click "SAVE" to apply settings changes.

🚨 **DISCLAIMER:**  The application's UI is optimized for a screen resolution of **1366 ✕ 768**.  Responsiveness for other screen resolutions is not fully implemented as of now. For optimal viewing, use the recommended resolution.

---

For advanced customization or specific feature requests, further code modifications and adaptation may be necessary. While primarily developed for academic purposes, feedback, suggestions, and contributions to enhance Yourvey Insights are warmly welcomed!

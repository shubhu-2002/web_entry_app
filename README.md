# File Upload & Management Web App

This is a **Flask-based web application** where users can **register, log in, upload files, and download their own uploaded files**.  
Each user can only view and download the files they have uploaded.

## Features 🚀
- **User Authentication** (Register & Login)
- **File Upload with Validation** (Supports PDF, DOCX, XLSX)
- **User-Specific File Management** (Users only see their own uploaded files)
- **File Listing with Download Links**
- **Dashboard for Users**
- **MySQL Database Integration**
- **Bootstrap UI for Responsive Design**

---

## Installation & Setup 🛠️
### **1️⃣ Clone the Repository**
```
git clone https://github.com/shubhu-2002/web_entry_app.git
cd web_entry_app
```
2️⃣ Create a Virtual Environment
```bash

python -m venv venv
source venv\Scripts\activate.ps1
```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Configure MySQL Database
```Open MySQL and create a database:

CREATE DATABASE file_upload_db;
Create the users and files tables:

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    filetype VARCHAR(50),
    uploaddate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
Update the database connection in app.py:

app.config['MYSQL_DATABASE_USER'] = 'your_username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'your_password'
app.config['MYSQL_DATABASE_DB'] = 'file_upload_db'
```
5️⃣ Run the Application
```
python app.py
Visit: http://127.0.0.1:5000/ in your browser.
```

#Folder Structure 📂
```
📦 Project Folder
├── 📂 templates        # HTML files (Login, Register, Dashboard)
├── 📂 static           # CSS & JS files
├── 📂 uploads          # Uploaded files storage
├── 📜 app.py           # Main Flask application
├── 📜 requirements.txt # Dependencies
├── 📜 README.md        # Project documentation
```
#Technologies Used :
```
Backend: Flask (Python)
Frontend: HTML, Bootstrap, JavaScript
Database: MySQL
```

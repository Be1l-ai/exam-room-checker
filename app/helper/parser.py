import pdfplumber
import sqlite3
from pathlib import Path
from db import init_db, connect_db
import pandas as pd
import numpy as np

pdf = Path("/workspaces/exam-room-checker/storage/student_lists/2025_finals_setB/")
db_schema = "/workspaces/exam-room-checker/storage/schema.sql"
db_path = "/workspaces/exam-room-checker/storage/exam_assignments.db"

def find_text(text, keyword):
    lines = text.split('\n')
    for line in lines:
        if keyword in line:
            return line
    return f"'{keyword}' not found in text."

# get meta data (room num, date and time, course name and code)
def get_room_num(pdf_path, page_index: int = 0):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[page_index]
            text = page.extract_text()
            line = find_text(text, "Room Number")
            if line:
                # Assuming the format is "Room Number: XYZ"
                parts = line.split(":")
                if len(parts) > 1:
                        # add validation using pydantic here later
                        return parts[1].strip() # return the second part of the "Room Number: 7024"
            return None # return list of room numbers found
    except Exception as e:
        return None

def get_date_time(pdf_path, page_index: int = 0):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[page_index]
            # just get the first page since all time is the same for all rooms per subject 
            text = page.extract_text()
            line = find_text(text, "Date/Time")
            if line:
                parts = line.split("/")
                if len(parts) > 1:
                    date_time = parts[1].split("|")
                    date = date_time[0].split(":")[1].strip()
                    time = date_time[1].strip()
                    return date, time # return tuple of date and time
            return None, None
    except Exception as e:
        return None, None

def get_course(pdf_path, page_index: int = 0):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[page_index] # first page only same as date/time
            text = page.extract_text()
            line = find_text(text, "Course Title")
            if line:
                parts = line.split(":")
                if len(parts) > 1:
                    title_code_set = parts[1].split("(")
                    title, code, set = title_code_set[0], title_code_set[1].replace(")",""), title_code_set[2].replace(")", "") if len(title_code_set) > 2 else ""
                    return title.strip(), code.strip(), set.strip() # return tuple of course title, code
            return None, None, None
    except Exception as e:
        return None, None, None

# get table
def get_table(pdf_file, page_index: int = 0):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            page = pdf.pages[page_index]
            table = page.extract_table()
            if not table or len(table) < 2:
                return pd.DataFrame()  # Return empty DataFrame instead of string
            student_table = pd.DataFrame(table[1:], columns=table[0])
            return student_table
    except Exception as e:
        return pd.DataFrame()  # Return empty DataFrame on error

def get_student_data(pdf_file, page_index: int = 0):
    # get meta data
        # get course title, set and code (just get once)
    course_title, course_code, course_set = get_course(pdf_file, 0)
    if course_title is None or course_code is None or course_set is None:
        print(f"ERROR: Could not extract course information from {pdf_file}")
        return {}
    
    # get date and time (just get once)
    date, time = get_date_time(pdf_file, 0)
    if date is None or time is None:
        print(f"ERROR: Could not extract date and time from {pdf_file}")
        return {}
    
    # get room number (get per page)
    room_num = get_room_num(pdf_file, page_index)
    if room_num is None:
        print(f"ERROR: Could not extract room number from {pdf_file} page {page_index}")
        return {}
    
    # get student list (get per page)
    table = get_table(pdf_file, page_index)
    table.iloc[:, 1] = table.iloc[:, 1].replace("", np.nan) # Replace empty strings with NaN
    table = table[table.iloc[:,1].notna()]  # Clean rows with empty names
    if not isinstance(table, pd.DataFrame) or table.empty:
        print(f"ERROR: No valid student table from {pdf_file} page {page_index}")
        return {}
    
    # get the names, number and course section
    student_number = table.iloc[:, 0]
    student_name = table.iloc[:, 1]
    student_section = table.iloc[:, 2]

    # return all data
    return {
        "student_number": student_number.tolist(),
        "student_name": student_name.tolist(),
        "student_section": student_section.tolist(),
        "course_title": course_title,
        "course_code": course_code,
        "course_set": course_set,
        "date": date,
        "time": time,
        "room_number": room_num
    }

# put it on database
def put_on_db(db_path, db_schema, exam_name:str, pdf_dir:str):
    # loop through all pdf
    connection = None
    try:
        init_db(db_path=db_path, db_schema=db_schema) # initialize db once
        connection = connect_db(db_path=db_path)
        for file in pdf_dir.glob("*.pdf"):
            with pdfplumber.open(file) as pdf:
                for page in range(len(pdf.pages)):
                    student_data = get_student_data(file, page) # call get_student_data()
                    if not isinstance(student_data, dict) or not student_data:
                        print(f"Skipping {file} page {page}: invalid data")
                        continue
                    
                    for index, student in enumerate(student_data["student_name"]): # loop through student in student_data
                        student_number = student_data["student_number"][index]
                        student_section = student_data["student_section"][index]
                        try:
                            connection.execute( # insert student data to db
                                "INSERT INTO exam_assignments ("
                                "exam_name,"
                                "student_number,"
                                "student_name,"
                                "student_section,"
                                "course_title,"
                                "course_code,"
                                "course_set,"
                                "exam_date,"
                                "exam_time,"
                                "room_number)"
                                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                        (
                                        exam_name,
                                        student_number,
                                        student,
                                        student_section,
                                        student_data["course_title"],
                                        student_data["course_code"],
                                        student_data["course_set"],
                                        student_data["date"],
                                        student_data["time"],
                                        student_data["room_number"]
                                        )
                            )
                            connection.commit()
                        except sqlite3.Error as e:
                            print(f"Error inserting data into database: {e}")
    except Exception as e:
        print(f"Error processing PDF files: {e}")
    finally:
        if connection:
            connection.close()
            print("Scanning successful. Set A added to the database.")

if __name__ == "__main__":
    # put_on_db(db_path=db_path, db_schema=db_schema, exam_name="2025_Finals_1st_Sem", pdf_dir=pdf)
    # After put_on_db call
    connection = connect_db(db_path)
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM exam_assignments")
            rows = cursor.fetchall()
            print("Database contents:")
            with open("/workspaces/exam-room-checker/storage/database_log.txt", "w") as log_file:
                log_file.write("Database contents:\n")
                for row in rows:
                    log_file.write(str(row) + "\n")
                log_file.write(f"Total rows: {len(rows)}\n")
            print(f"Log written to /workspaces/exam-room-checker/storage/database_log.txt")
        except sqlite3.Error as e:
            print(f"Error querying database: {e}")
        finally:
            connection.close()
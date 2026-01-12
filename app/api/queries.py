import sqlite3
import sys
import pandas as pd
from pathlib import Path

# Add workspace root to path for absolute imports
sys.path.append('/workspaces/exam-room-checker')
from app.helper.db import connect_db

db_path = "/workspaces/exam-room-checker/storage/exam_assignments.db"

def search(search:str, column:str | None = None) -> list:
    # basic search, return list of tuple of matching entries (tuple converter to dict)
    if not search.strip(): # catch empty param
        return ["Search term must not be empty."]

    # connect to db
    keys = ["id", "exam_name", "course_title", "course_code", "course_set", "date", "time", "room_number", "student_number", "student_name", "student_section"]
    connection = connect_db(db_path)

    try:
        cursor = connection.cursor()
        connection.row_factory = sqlite3.Row
    # use Select and Where sql statements to search for the given parameter
        if column and column in keys: # search only for specific column on the table
            special_char ="!@#$%^&*()<>,./-_=+"
            cursor.execute("SELECT * FROM exam_assignments WHERE ? LIKE ?;", (column, search))

        else: # search all columns if theres no specific column or specified column doesnt exist
            cursor.execute(
                "SELECT * FROM exam_assignments WHERE "
                "exam_name LIKE ? OR "
                "student_number LIKE ? OR "
                "student_name LIKE ? OR "
                "student_section LIKE ? OR "
                "course_title LIKE ? OR "
                "course_code LIKE ? OR "
                "course_set LIKE ? OR "
                "exam_date LIKE ? OR "
                "exam_time LIKE ? OR "
                "room_number LIKE ?;",
                (f"%{search}%",)*10
            )
        result = cursor.fetchall()
    except sqlite3.Error as e:
        return [f"ERROR-sqlite.error: {e}"]
    finally:
        if connection:
            connection.close()

    if result:
        try: # catch schema change or any error on using dict(zip())
            return [dict(zip(keys, row)) for row in result]
        except (ValueError, TypeError, KeyError) as e:
            return [f"ERROR-{type(e).__name__}: {e}"]
    
    return [] # return empty if theres no result

def get_student(student_name:str) -> list: # only work on correct name format right now, need improvement
    # get all student with the same name

    # use search to get all student with the same name
    # try with fullname then if empty fall back to first or last name (eg. Cantiga[0], Ken Lester T. or Ken[0] Lester T. Cantiga)
    # else exit
    students = search(search=student_name, column="student_name")
    if not students or students == []:
        if len(student_name.split(" ")) < 2:
            return [f"No students found with name containing '{student_name}'"]
        students = search(student_name.split(" ")[0]) # this is a list of dict
    
    # filter to that one specific name (main name)
    specific_students = [entry for entry in students if entry["student_name"] == student_name] # returns a row
    if specific_students == []: # needs a better filtering algorithm
        return students

    # add the other might be similar name
    # other_students = students_df[students_df['student_name'] != student_name]
    # if other_students is None or other_students.empty:
    #     return [specific_students.to_dict('records'), {"message": "No similar students found"}]

    return specific_students #, other_students.to_dict()]

def get_course_by_exam(exam_name:str) -> list:
    # get all exam with the same name

    # use search() to get all the exam with the same name
    # remove duplicates course_title
    # list down all course_title under the exam_nam
    # return list of course_title
    pass

def get_course(course_code:str, course_title:str) -> str:
    # get course with the same code or title

    # get all course with the same code or title using search()
    # remove duplicates
    # return list of course_code and its course_title
    pass

def get_students_by_room(room_number:str) -> list:
    # get all student in the same room

    # use search() to get all student in the same room
    # group the student by course_code/title
    # put the group into their corresponding room_number
    # return the room_number with list of students
    pass

def get_student_room(student_name:str) -> list:
    # get the room number of a student

    # use search() to get the all matching student
    # filter to the specific student_name
    # return a list of all of the student's exams with their room numbers
    pass

def get_exam_by_date(exam_date:str) -> list:
    # get all exam on the same date
    pass

def get_exam_by_time(exam_time:str) -> list:
    # get all exam at the same time
    pass

if __name__ == "__main__":
    pass
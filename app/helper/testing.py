import pdfplumber
from parser import get_room_num, get_table, get_student_data
import pandas as pd
from pathlib import Path

def print_pdf_lines():
    pdf_path = "/workspaces/exam-room-checker/storage/student_lists/2025_finals_setA/CWTS 1 -Set A.pdf"
    lines = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            lines = text.split('\n')
            for index, line in enumerate(lines):
                if index < 10:
                    print(f"Line {index + 1}: {line}")
                    # prints 10 lines (room number, courese title, date and time line)
    except Exception as e:
        print(f"Error opening PDF: {e}")

def test_get_room_num():
    pdf_path = "/workspaces/exam-room-checker/storage/student_lists/2025_finals_setA/CWTS 1 -Set A.pdf"
    room_num = get_room_num(pdf_path)
    print(f"Extracted Room Numbers: {room_num}")

def test_get_table():
    pdf_path = "/workspaces/exam-room-checker/storage/student_lists/2025_finals_setA/CWTS 1 -Set A.pdf"
    table = get_table(pdf_path, page_index=0)
    print(table)

def test_dir_loop():
    pdf_dir = Path("/workspaces/exam-room-checker/storage/student_lists/2025_finals_setA/")
    for file in pdf_dir.glob("*.pdf"):
        print(file)
        print("counting")

def test_get_student_data():
    print("Testing get_student_data function:")
    pdf_path = "/workspaces/exam-room-checker/storage/student_lists/2025_finals_setA/CWTS 1 -Set A.pdf"
    student_data = get_student_data(pdf_path, page_index=0)
    print(student_data)

if __name__ == "__main__":
    # print_pdf_lines()
    # test_get_room_num()
    # test_get_table()
    test_get_student_data()
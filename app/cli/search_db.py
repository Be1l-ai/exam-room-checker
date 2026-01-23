import argparse
import sys
import pandas as pd

sys.path.append('/workspaces/exam-room-checker')
from app.helper.parser import get_student_data # to parse pdf files

def main():
    parser = argparse.ArgumentParser(description="Exam Room Checker CLI, Input a pdf file to parse it into csv or store on sqlite3 db.")

    parser.add_argument("seach", type=str, help="Read PDF and convert/store to csv/database")
    parser.add_argument("--term", action="store_true", help="Store the student data into csv")
    parser.add_argument("--column", action="store_true", help="Store the student data into the sqlite database")

    args = parser.parse_args()

    if args:
        if not args.term or not args.output:
            raise ValueError("Input and Output argument required")
        
        if args.to_csv:
            # get_student_data
            # store to db
            pass
        elif args.to_database:
            # get_student_data
            pass        
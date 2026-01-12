import argparse, sys, os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

sys.path.append('/workspaces/exam-room-checker') # appending the root dir to python path so app module can be recognize
# from app.helper.db import connect_db # db helpers to pass sql commands directly
from app.helper.parser import get_student_data, put_on_db, write_to_csv # to parse pdf files
from app.helper.models import ExamAssignment

load_dotenv()
db_path = os.getenv("DB_PATH") # hard coded but can be changed on .env
db_schema = os.getenv("DB_SCHEMA")

def main():
    parser = argparse.ArgumentParser(description="Exam Room Checker CLI, Input a pdf file to parse it into csv or store on sqlite3 db.")

    parser.add_argument("read", type=str, help="Read PDF and convert/store to csv/database, NOTE: store on db on default")
    parser.add_argument("input", type=str, help="File path of the pdf as input, NOTE: the directory of the pdf file, cause to not store on db")
    parser.add_argument("output", type=str, help="File path of the csv or database to store, NOTE: the exact file to write/save on to")
    parser.add_argument("--to_csv", action="store_true", help="Store the student data into csv")

    args = parser.parse_args()

    if args:
        if not args.to_csv:
            put_on_db(db_path=args.output, db_schema=db_schema, exam_name=args.read, pdf_dir=Path(args.input)) # has a built in error handling
            print("Succesfully parsed the pdf's")
            return 0

        if args.to_csv:
            write_to_csv(db_path=db_path, args_output=args.output)
            print(f"Student data written to: {args.output}")

if __name__ == "__main__":
    main()

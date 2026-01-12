# Exam Room Checker

A room checker for quarterly terms on Emilio Aguinaldo College-Cavite. Every term a new pdf file containing a list of student and their exam course and room is released. This simple parser of that pdf is made so that searching would be easier without the need to go to google drive to open pdf files.

## Features

- [x] Command Line Interface feature for directly parsing pdf file.
- [x] Export from database to csv file.
- [x] Search through the student data sets.
- [] Rest api implementation.
- [] Quick web search.
- [] Comprehensive filtering by rooms, course name, etc..

## How to install

1. Clone the repo:

```bash
git clone https://github.com/Be1l-ai/exam-room-checker.git
```

2. Set up environment:

```bash
cd exam-room-checker # enter the directory

python -m venv venv # make a virtual environment

pip install -r requirement.txt # install dependencies

cp .env.example .env # create .env config
```

3. CLI is now ready to use:

```bash
# Parse PDFs and export to CSV
python app/cli/read_pdf.py read storage/student_lists/2025_finals_setA storage/extra.csv --to_csv

```

## Usage

- **Parsing PDFs**: Use the CLI to extract student data from PDF files and store in database or export to CSV.
- **Searching**: Query the database for student information by name, number, or course.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make changes and test.
4. Submit a pull request.

# Others

Other documentations:

- [App Directory](app/readme.md)
- [Storage Directory](storage/readme.md)
- [CLI Scripts](app/cli/readme.md)
- [Helper Modules](app/helper/readme.md)
- [API Modules](app/api/readme.md)

CREATE TABLE IF NOT EXISTS exam_assignments (
    --All TEXT because im lazy, i hope it doesnt break
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    --Exam Details and Metadata
    exam_name TEXT NOT NULL, -- e.g., "Finals 1st Semester 2025"
    course_title TEXT NOT NULL, -- e.g., "CWTS 1"
    course_code TEXT NOT NULL, -- e.g., "AGE8 00"
    course_set TEXT NOT NULL, -- e.g., "Set A"
    exam_date TEXT NOT NULL, -- e.g., "December 10, 2025"
    exam_time TEXT NOT NULL, -- e.g., "3:00pm - 5:00pm"

    --Room Assignment Details
    room_number TEXT NOT NULL, -- e.g., "7034"
    student_number TEXT NOT NULL, -- e.g., "25 (number sa list not id)"
    student_name TEXT NOT NULL, -- e.g., "Ken Lester T. Cantiga"
    student_section TEXT NOT NULL -- e.g., "UCOS 1-1"

);

CREATE INDEX idx_exam_name ON exam_assignments (exam_name);
CREATE INDEX idx_course_code ON exam_assignments (course_code);
CREATE INDEX idx_room_number ON exam_assignments (room_number);
CREATE INDEX idx_student_section ON exam_assignments (student_section);
CREATE INDEX idx_student_name ON exam_assignments (student_name);
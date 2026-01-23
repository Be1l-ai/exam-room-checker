from queries import search, get_student, get_course_by_exam, get_course

def test_search():
    results = search("Ken")
    assert isinstance(results, list)
    print(results)
    # for entry in results:
    #     print(entry)
        # for item in entry:
        #     print(item)

def test_search_specific():
    results = search("7304")
    if results.isempty():
        print("no results found")
    #print(results)
    for entry in results:
        assert "7304" in entry["room_number"]
        print("Student room number:", entry["room_number"])
        print(f"Student: {entry["student_name"]} on Exam: {entry["exam_name"]}:{entry["course_title"]} at Date: {entry["date"]}")

def test_search_strict_name():
    results = search("Cant")
    if results == []:
        print("no results found")
    for entry in results:
        print(f"Student: {entry["student_name"]} - Exam: {entry["exam_name"]} - Section: {entry["student_section"]} - Room: {entry["room_number"]}")
        print(f"Subject: {entry["course_title"]}, Room: {entry["room_number"]}, Date: {entry["date"]}, Time: {entry["time"]}")

def test_search_no_results():
    results = search("NonExistentName123")
    assert isinstance(results, list)
    assert len(results) == 0

def test_search_special_characters():
    results = search("%_")
    result2 = search(" ") # test space character
    result3 = search("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") 
    assert isinstance(results, list)
    assert isinstance(result2, list)
    assert isinstance(result3, list)

def test_get_student():
    student1 = get_student("Ken Lester T. Cantiga")
    student2 = get_student("Cantiga, Ken lester T.")
    assert isinstance(student1, list)
    print(student1)
    print(student2)

def test_get_course_by_exam():
    final_exams = get_course_by_exam("2025_Finals_1st_Sem")
    midterm_exams = get_course_by_exam("Midterms")
    s2025_exam = get_course_by_exam("2025")
    assert final_exams != []
    assert isinstance(midterm_exams[0], str)
    assert isinstance(s2025_exam, list)
    print(final_exams)
    print(midterm_exams)
    print(s2025_exam)

def test_get_course():
    math = get_course(course_title="Math")
    code = get_course("age8 00")
    print(code)

if __name__ == "__main__":
    # test_search()
    # test_search_no_results()
    # test_search_special_characters()
    # test_search_specific()
    # test_search_strict_name()
    # test_get_student()
    # test_get_course_by_exam()
    test_get_course()
    print("All tests done.")
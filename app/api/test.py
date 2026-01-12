from queries import search, get_student

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


if __name__ == "__main__":
    #test_search()
    #test_search_no_results()
    #test_search_special_characters()
    #test_search_specific()
    #test_search_strict_name()
    test_get_student()
    print("All tests done.")
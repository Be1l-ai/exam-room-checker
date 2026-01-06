from pydantic import BaseModel, field_validator, model_validator

class ExamInfo(BaseModel):
    room_number: str
    date: str
    time: str
    course_title: str
    course_code: str
    course_set: str

    @field_validator('room_number')
    @classmethod
    def room_number_must_be_four_digit(cls, value:str) -> str:
        if len(value) < 4 or len(value) > 7:  # allow formats like "1234" or "1232-A1"
            raise ValueError('room_number must be a 4 to 7-digit string')
        return value
    
    @field_validator('course_set')
    @classmethod
    def course_set_must_be_valid(cls, value:str) -> str:
        if "Set" not in value and "set" not in value and "SET" not in value:
            raise ValueError('course_set must contain the word "Set"')
        if len(value) > 6:
            raise ValueError('course_set length usually does not exceed 6 characters')
        return value

    @field_validator('time')
    @classmethod
    def time_must_be_valid_format(cls, value:str) -> str:
        nums = ["0","1","2","3","4","5","6","7","8","9"]
        time = ["AM", "PM", "am", "pm"]
        if not any(num in value for num in nums):
            raise ValueError('time must contain a number')
        if not any(t in value for t in time):
            raise ValueError('time must have am or pm')
        if len(value) > 20:
            raise ValueError('time length usually does not exceed 20 characters')
        if ":" not in value:
            raise ValueError('time must be in valid format, e.g., "08:00 AM - 10:00 AM"')
        return value
    
    @field_validator('date')
    @classmethod
    def date_must_be_valid_format(cls, value:str) -> str:
        nums = ["0","1","2","3","4","5","6","7","8","9"]
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        if not any(num in value for num in nums):
            raise ValueError('date must have number')
        if not any(month in value for month in months):
            raise ValueError('date must have a month')
        if len(value) > 25:
            raise ValueError('date length usually does not exceed 25 characters')
        if "," not in value:
            raise ValueError('date must be in valid format, e.g., "March 15, 2023"')
        return value

class StudentInfo(BaseModel):
    student_number: list[str]
    student_name: list[str]
    student_section: list[str]

    @field_validator('student_section')
    @classmethod
    def student_section_must_be_valid(cls, value:list[str]) -> list[str]:
        for v in value:
            if len(v) > 4:
                raise ValueError('student_section length usually does not exceed 4 characters')
        return value

    @field_validator('student_number')
    @classmethod
    def student_number_valid_characters(cls, value:list[str]) -> list[str]:
        for v in value:
            if not v.isdigit():
                raise ValueError('student_number should only contain numeric characters')
        return value

class ExamAssignment(BaseModel):
    exam_info: ExamInfo
    student_info: StudentInfo
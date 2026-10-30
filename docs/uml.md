\# Smart Campus Management System — Class Diagram



\## Classes



\### Person «abstract»

\- `\_name` : str

\- `\_person\_id` : str  

\- `\_email` : str

\- `name` : str  «property»

\- `id` : str  «property»

\- `display\_info()` : str  «abstract»

\- `\_\_str\_\_()` : str



\### Student(Person, Payable, Reportable)

\- `\_program` : str

\- `\_year` : int

\- `\_courses` : list\[Course]

\- `TUITION\_PER\_CREDIT` : float = 150.0

\- `display\_info()` : str

\- `calculate\_payment()` : float

\- `enroll(course)` : None

\- `generate\_report()` : str



\### Lecturer(Person, Payable)

\- `\_department` : str

\- `\_base\_salary` : float

\- `\_courses\_taught` : list\[Course]

\- `BONUS\_PER\_COURSE` : float = 500.0

\- `display\_info()` : str

\- `assign\_course(course)` : None

\- `calculate\_payment()` : float



\### AdminStaff(Person)

\- `\_role` : str

\- `display\_info()` : str



\### Course

\- `code`, `title`, `credits`, `capacity` : public

\- `lecturer` : Lecturer

\- `\_students` : list\[Student]

\- `assign\_lecturer(lecturer)` : None

\- `add\_student(student)` : None  «raises CourseFullError»

\- `enrolled\_count` : int  «property»

\- `\_\_str\_\_()` : str



\### Department(Reportable)

\- `name` : str

\- `\_courses` : list\[Course]

\- `\_lecturers` : list\[Lecturer]

\- `add\_course(course)` : None

\- `add\_lecturer(lecturer)` : None

\- `generate\_report()` : str



\## Interfaces



\- `Payable` : `calculate\_payment() -> float`  «abstract»

\- `Reportable` : `generate\_report() -> str`  «abstract»



\## Relationships



\- Person ← Student, Lecturer, AdminStaff (inheritance)

\- Student → Payable, Reportable (implements)

\- Lecturer → Payable (implements)

\- Course → Lecturer (has-a)

\- Course → Student\[] (has-a, capacity-limited)

\- Department → Course\[], Lecturer\[] (has-a)

\- Department → Reportable (implements)



\## Exceptions



\- CourseFullError(Exception)

\- DuplicateEnrollmentError(Exception)


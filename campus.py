from abc import ABC, abstractmethod


# ============================================================
# EXCEPTIONS
# ============================================================
class CourseFullError(Exception):
    """Raised when a course has reached its maximum capacity."""
    pass


class DuplicateEnrollmentError(Exception):
    """Raised when a student tries to enroll in the same course twice."""
    pass


# ============================================================
# PHASE 1: Abstract identity
# ============================================================
class Person(ABC):
    def __init__(self, name, person_id, email):
        self._name = name
        self._person_id = person_id
        self._email = email

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._person_id

    @abstractmethod
    def display_info(self):
        """Return a formatted description of this person."""

    def __str__(self):
        return f"{self.__class__.__name__}({self._name}, {self._person_id})"


# ============================================================
# PHASE 3: Capability interfaces
# ============================================================
class Payable(ABC):
    @abstractmethod
    def calculate_payment(self) -> float:
        """Return money owed (student) or earned (lecturer)."""


class Reportable(ABC):
    @abstractmethod
    def generate_report(self) -> str:
        """Return a multi-line human-readable report."""


# ============================================================
# PHASE 2 + 3: Subclasses of Person
# ============================================================
class Student(Person, Payable, Reportable):
    TUITION_PER_CREDIT = 150.0

    def __init__(self, name, pid, email, program, year):
        super().__init__(name, pid, email)
        self._program = program
        self._year = year
        self._courses = []

    def display_info(self):
        return (f"Student: {self.name} | Program: {self._program} "
                f"| Year: {self._year}")

    def _total_credits(self):
        return sum(c.credits for c in self._courses)

    def calculate_payment(self) -> float:
        return self._total_credits() * self.TUITION_PER_CREDIT

    def enroll(self, course):
        if course in self._courses:
            raise DuplicateEnrollmentError(
                f"{self.name} is already enrolled in {course.title}")
        course.add_student(self)      # may raise CourseFullError
        self._courses.append(course)

    def generate_report(self) -> str:
        courses = ", ".join(c.title for c in self._courses) or "None"
        return (f"[STUDENT REPORT] {self.name} ({self._program}, Year {self._year})\n"
                f"  Courses: {courses}\n"
                f"  Total credits: {self._total_credits()}\n"
                f"  Tuition owed: UGX{self.calculate_payment():,.2f}")


class Lecturer(Person, Payable):
    BONUS_PER_COURSE = 500.0

    def __init__(self, name, pid, email, department, base_salary):
        super().__init__(name, pid, email)
        self._department = department
        self._base_salary = base_salary
        self._courses_taught = []

    def display_info(self):
        return (f"Lecturer: {self.name} | Dept: {self._department} "
                f"| Salary: UGX{self._base_salary}")

    def assign_course(self, course):
        """Called by Course.assign_lecturer to keep the link bidirectional."""
        self._courses_taught.append(course)

    def calculate_payment(self) -> float:
        return self._base_salary + (len(self._courses_taught) * self.BONUS_PER_COURSE)


class AdminStaff(Person):
    def __init__(self, name, pid, email, role):
        super().__init__(name, pid, email)
        self._role = role

    def display_info(self):
        return f"Admin: {self.name} | Role: {self._role}"


# ============================================================
# PHASE 4: Composition — Course & Department
# ============================================================
class Course:
    def __init__(self, code, title, credits, capacity=30):
        self.code = code
        self.title = title
        self.credits = credits
        self.capacity = capacity
        self.lecturer = None
        self._students = []

    def assign_lecturer(self, lecturer):
        self.lecturer = lecturer
        lecturer.assign_course(self)         # keep the link bidirectional

    def add_student(self, student):
        if len(self._students) >= self.capacity:
            raise CourseFullError(
                f"{self.title} ({self.code}) is full (capacity {self.capacity}).")
        self._students.append(student)

    @property
    def enrolled_count(self):
        return len(self._students)

    def __str__(self):
        return f"{self.code} - {self.title} ({self.credits} cr)"


class Department(Reportable):
    def __init__(self, name):
        self.name = name
        self._courses = []
        self._lecturers = []

    def add_course(self, course):
        self._courses.append(course)

    def add_lecturer(self, lecturer):
        self._lecturers.append(lecturer)

    def generate_report(self) -> str:
        lines = [f"=== Department: {self.name} ==="]
        lines.append(f"Lecturers ({len(self._lecturers)}):")
        for l in self._lecturers:
            lines.append(f"  - {l.display_info()}")
        lines.append(f"Courses ({len(self._courses)}):")
        for c in self._courses:
            lines.append(f"  - {c} | Enrolled: {c.enrolled_count}/{c.capacity}")
        return "\n".join(lines)


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    # ---- build the world ----
    cs = Department("Computer Science")

    dr_jones = Lecturer("Dr. Jones", "L001", "jones@x.com", "CS", 3000)
    cs.add_lecturer(dr_jones)

    oop = Course("CS201", "OOP", 3, capacity=2)
    oop.assign_lecturer(dr_jones)
    cs.add_course(oop)

    algo = Course("CS301", "Algorithms", 4)
    algo.assign_lecturer(dr_jones)
    cs.add_course(algo)

    alice = Student("Alice", "S001", "a@x.com", "CS", 2)
    bob = Student("Bob", "S002", "b@x.com", "CS", 2)
    carol = Student("Carol", "S003", "c@x.com", "CS", 1)

    # ---- enroll ----
    alice.enroll(oop)
    alice.enroll(algo)
    bob.enroll(oop)

    # ---- over-fill test ----
    try:
        carol.enroll(oop)
    except CourseFullError as e:
        print(f"[handled] {e}")

    # ---- duplicate test ----
    try:
        alice.enroll(oop)
    except DuplicateEnrollmentError as e:
        print(f"[handled] {e}")

    # ---- polymorphic payment loop ----
    print("\n=== Payment Processing ===")
    for p in [alice, bob, carol, dr_jones]:
        verb = "Earns" if isinstance(p, Lecturer) else "Owes"
        print(f"  {p.name:<10} {verb}: UGX{p.calculate_payment():,.2f}")

    # ---- reports ----
    print("\n" + alice.generate_report())
    print("\n" + cs.generate_report())

        # ---- AdminStaff is NOT payable (demo of interface filtering) ----
    print("\n=== Mixed list — only payable objects get paid ===")
    admin = AdminStaff("Mary", "A001", "mary@x.com", "Registrar")
    everyone = [alice, bob, carol, dr_jones, admin]

    for p in everyone:
        if isinstance(p, Payable):
            verb = "Earns" if isinstance(p, Lecturer) else "Owes"
            print(f"  {p.name:<10} {verb}: UGX{p.calculate_payment():,.2f}")
        else:
            print(f"  {p.name:<10} (not payable — skipped)")
\# Smart Campus Management System



A Python Object-Oriented Programming project demonstrating the four OOP pillars —

abstraction, encapsulation, inheritance, and polymorphism — with custom exceptions

and composition.



\*\*Author:\*\* \[YOUR FULL NAME]

\*\*Student ID:\*\* \[YOUR ID]

\*\*Course:\*\* Object-Oriented Programming — Project-Based Exam

\*\*Date:\*\* \[TODAY'S DATE]



\---



\## Table of Contents



1\. \[Features](#features)

2\. \[How to Run](#how-to-run)

3\. \[Project Structure](#project-structure)

4\. \[Class Design](#class-design)

5\. \[OOP Pillars Demonstrated](#oop-pillars-demonstrated)

6\. \[Sample Output](#sample-output)

7\. \[Future Work](#future-work)



\---



\## Features



\- \*\*People hierarchy:\*\* `Person` (abstract) → `Student`, `Lecturer`, `AdminStaff`

\- \*\*Capability interfaces:\*\* `Payable` (`calculate\_payment`), `Reportable` (`generate\_report`)

\- \*\*Academic structure:\*\* `Course` (has-a `Lecturer`, has-a list of `Student`s), `Department` (has-a `Course`s, has-a `Lecturer`s)

\- \*\*Business rules enforced via exceptions:\*\*

&#x20; - `CourseFullError` — prevents enrolling past capacity

&#x20; - `DuplicateEnrollmentError` — prevents double enrollment

\- \*\*Polymorphic payment processing\*\* — one loop pays all payable objects with \*\*no `if/else` on type\*\*

\- \*\*Automatic reporting\*\* — student and department reports generated from live data

\- \*\*Extensible\*\* — adding a new payable type requires \*\*zero changes\*\* to existing code



\---



\## How to Run



Requires \*\*Python 3.8+\*\*. No external dependencies — pure standard library.



```bash

python campus.py


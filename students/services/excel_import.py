import pandas as pd
import re

from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from ..models import Student

REQUIRED_COLUMNS = [
    "Name",
    "Enrollment No",
    "Semester",
    "Email",
    "Mobile",
    "Course",
    "Department",
    "Admission Date",
]

def read_excel_file(excel_file):
    df = pd.read_excel(excel_file)
    return df

def validate_excel(df):
    """
    Validate uploaded Excel file.

    Returns:
        errors -> list of error messages
    """

    errors = []

    # -----------------------------------
    # Validate Required Columns
    # -----------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            "Missing Columns: "
            + ", ".join(missing_columns)
        )
        return errors

    # -----------------------------------
    # Duplicate inside Excel
    # -----------------------------------

    duplicate_enrollment = df[
        df["Enrollment No"].duplicated()
    ]

    for _, row in duplicate_enrollment.iterrows():
        errors.append(
            f"Duplicate Enrollment No in Excel: {row['Enrollment No']}"
        )

    duplicate_email = df[
        df["Email"].duplicated()
    ]

    for _, row in duplicate_email.iterrows():
        errors.append(
            f"Duplicate Email in Excel: {row['Email']}"
        )

    # -----------------------------------
    # Validate Every Row
    # -----------------------------------

    for index, row in df.iterrows():

        row_no = index + 2  # Excel row number

        # ---------------------------
        # Empty Fields
        # ---------------------------

        for column in REQUIRED_COLUMNS:

            value = row[column]

            if pd.isna(value) or str(value).strip() == "":
                errors.append(
                    f"Row {row_no}: {column} cannot be empty."
                )

        # ---------------------------
        # Semester
        # ---------------------------

        try:
            semester = int(row["Semester"])

            if semester not in range(1, 9):
                errors.append(
                    f"Row {row_no}: Semester must be between 1 and 8."
                )

        except:
            errors.append(
                f"Row {row_no}: Invalid Semester."
            )

        # ---------------------------
        # Email
        # ---------------------------

        try:
            validate_email(str(row["Email"]))
        except ValidationError:
            errors.append(
                f"Row {row_no}: Invalid Email."
            )

        # ---------------------------
        # Mobile
        # ---------------------------

        mobile = str(row["Mobile"]).strip()

        if not re.fullmatch(r"\d{10}", mobile):
            errors.append(
                f"Row {row_no}: Mobile must contain exactly 10 digits."
            )

        # ---------------------------
        # Enrollment Exists
        # ---------------------------

        enrollment = str(row["Enrollment No"]).strip()

        if Student.objects.filter(
            enrollment_no=enrollment
        ).exists():

            errors.append(
                f"Row {row_no}: Enrollment '{enrollment}' already exists."
            )

        # ---------------------------
        # Email Exists
        # ---------------------------

        email = str(row["Email"]).strip()

        if Student.objects.filter(
            email=email
        ).exists():

            errors.append(
                f"Row {row_no}: Email '{email}' already exists."
            )

        # ---------------------------
        # Admission Date
        # ---------------------------

        try:
            pd.to_datetime(
                row["Admission Date"]
            )

        except:

            errors.append(
                f"Row {row_no}: Invalid Admission Date."
            )

    return errors


def import_students_data(df, college):
    """
    Import validated students into the database.
    """

    students = []

    for _, row in df.iterrows():

        student = Student(
            college=college,
            name=str(row["Name"]).strip(),
            enrollment_no=str(row["Enrollment No"]).strip(),
            semester=int(row["Semester"]),
            email=str(row["Email"]).strip(),
            mobile=str(row["Mobile"]).strip(),
            course=str(row["Course"]).strip(),
            department=str(row["Department"]).strip(),
            admission_date=pd.to_datetime(
                row["Admission Date"]
            ).date(),
        )

        students.append(student)

    with transaction.atomic():
        Student.objects.bulk_create(students)

    return len(students)
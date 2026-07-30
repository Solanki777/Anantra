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
    file_name = excel_file.name.lower()

    if file_name.endswith(".xlsx"):
        return pd.read_excel(excel_file, engine="openpyxl")
    elif file_name.endswith(".xls"):
        return pd.read_ewexcel(excel_file, engine="xlrd")
    else:
        raise ValueError("Only .xlsx and .xls files are supported.")

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

    valid_students = []
    errors = []

    for index, row in df.iterrows():

        row_no = index + 2
        row_errors = []

        # -----------------------------
        # Name
        # -----------------------------
        name = str(row["Name"]).strip()

        if not name:
            row_errors.append("Name cannot be empty")

        # -----------------------------
        # Enrollment
        # -----------------------------
        enrollment = str(row["Enrollment No"]).strip()

        if Student.objects.filter(
            college=college,
            enrollment_no=enrollment
        ).exists():
            row_errors.append("Enrollment Number already exists")

        # -----------------------------
        # Semester
        # -----------------------------
        try:
            semester = int(row["Semester"])

            if semester not in range(1, 9):
                row_errors.append("Semester must be between 1 and 8")

        except:
            row_errors.append("Invalid Semester")

        # -----------------------------
        # Email
        # -----------------------------
        email = str(row["Email"]).strip()

        try:
            validate_email(email)
        except ValidationError:
            row_errors.append("Invalid Email")

        if Student.objects.filter(
            college=college,
            email=email
        ).exists():
            row_errors.append("Email already exists")

        # -----------------------------
        # Mobile
        # -----------------------------
        mobile = str(row["Mobile"]).strip()

        if not re.fullmatch(r"\d{10}", mobile):
            row_errors.append("Mobile must contain exactly 10 digits")

        # -----------------------------
        # Course
        # -----------------------------
        course = str(row["Course"]).strip()

        if not course:
            row_errors.append("Course cannot be empty")

        # -----------------------------
        # Department
        # -----------------------------
        department = str(row["Department"]).strip()

        if not department:
            row_errors.append("Department cannot be empty")

        # -----------------------------
        # Admission Date
        # -----------------------------
        try:
            admission_date = pd.to_datetime(
                row["Admission Date"]
            ).date()

        except:
            row_errors.append("Invalid Admission Date")

        # -----------------------------
        # Save Error or Student
        # -----------------------------
        if row_errors:

            errors.append({
                "row": row_no,
                "message": ", ".join(row_errors)
            })

        else:

            valid_students.append(
                Student(
                    college=college,
                    name=name,
                    enrollment_no=enrollment,
                    semester=semester,
                    email=email,
                    mobile=mobile,
                    course=course,
                    department=department,
                    admission_date=admission_date,
                )
            )

    # Bulk Insert
    with transaction.atomic():

        Student.objects.bulk_create(valid_students)

    # Summary
    return {

        "total_rows": len(df),

        "imported": len(valid_students),

        "failed": len(errors),

        "errors": errors,

    }
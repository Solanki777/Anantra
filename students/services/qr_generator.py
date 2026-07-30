import os
import qrcode

from django.conf import settings


def generate_student_qr(student):
    """
    Generate a QR code for a student verification page.
    Returns the relative path of the generated QR image.
    """

    # Folder to save QR codes
    qr_folder = os.path.join(settings.MEDIA_ROOT, "qr_codes")
    os.makedirs(qr_folder, exist_ok=True)

    # Verification URL
    verification_url = (
        f"http://127.0.0.1:8000/verify/{student.enrollment_no}/"
    )

    # Generate QR
    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=4,
    )

    qr.add_data(verification_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # File name
    file_name = f"{student.enrollment_no}.png"

    file_path = os.path.join(qr_folder, file_name)

    img.save(file_path)

    return os.path.join("qr_codes", file_name)
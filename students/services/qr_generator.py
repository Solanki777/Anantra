import os
import qrcode

from django.conf import settings


def generate_student_qr(student):

    qr_folder = os.path.join(
        settings.MEDIA_ROOT,
        "qr_codes"
    )

    os.makedirs(qr_folder, exist_ok=True)

    verification_url = (
        f"{settings.SITE_URL}/verify/{student.enrollment_no}/"
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=4,
    )

    qr.add_data(verification_url)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    file_name = f"{student.enrollment_no}.png"

    file_path = os.path.join(
        qr_folder,
        file_name
    )

    img.save(file_path)

    return f"qr_codes/{file_name}"
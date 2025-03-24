import qrcode
from pyzbar.pyzbar import decode
from PIL import Image


# Simple creation of QR Code

# Data to be encoded
data = 'Don\'t forget to subscribe'

# Make the QR code
img = qrcode.make(data)

# Save the QR code
img.save('qrcode.png')

img.save('F:/Python Practice/Python Web Apps/python-projects/14-qr-generator/qrcode.png')

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill='blue', back_color='white')
img.save('qrcode1.png')

img.save('F:/Python Practice/Python Web Apps/python-projects/14-qr-generator/qrcode1.png')


# Decode QR Code

image = Image.open('qrcode1.png')

decoded = decode(image)

print(decoded)


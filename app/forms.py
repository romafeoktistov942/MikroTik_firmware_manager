from django import forms


class FirmwareUploadForm(forms.Form):
    ip_address = forms.GenericIPAddressField(label="IP адрес устройства")
    firmware_file = forms.FileField(label="Файл прошивки")

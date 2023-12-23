

from join.models import Contact


def create_first_contact(user):
    # Überprüfe, ob der Vorname vorhanden ist
    if user.first_name:
        first_letter = user.first_name[0].upper()
    else:
        # Falls nicht, nimm die ersten beiden Buchstaben des Nachnamens (sofern vorhanden)
        first_letter = user.last_name[:2].upper() if user.last_name else ""

    # Überprüfe, ob der Nachname vorhanden ist
    if user.last_name:
        second_letter = user.last_name[0].upper()
    else:
        # Falls nicht, nimm die ersten beiden Buchstaben des Vornamens (sofern vorhanden)
        second_letter = user.first_name[:2].upper() if user.first_name else ""

    # Erstelle das Logogramm aus den extrahierten Buchstaben
    logogram = first_letter + second_letter

    # Erstelle den Kontakt in der Datenbank
    contact = Contact.objects.create(
        name=user.first_name + " " + user.last_name + ' (me)',
        email=user.email,
        logogram=logogram,
        hex_color='#994a00',
        author=user,  # Setze den Benutzer als Autor
        receiver=user  # Setze den Benutzer als Empfänger
    )
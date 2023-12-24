from join.models import Contact

def create_first_contact(user):
    """
    Create a database contact using the user's initials as a logogram.
    :param user: User object with first_name, last_name, and email attributes.
    :return: Created Contact object in the database.
    """
    first_letter = user.first_name[0].upper() if user.first_name else ""
    second_letter = user.last_name[0].upper() if user.last_name else ""

    logogram = first_letter + second_letter

    contact = Contact.objects.create(
        name=user.first_name + " " + user.last_name if user.last_name else user.first_name,
        email=user.email,
        logogram=logogram,
        hex_color='#994a00',
        author=user,
        receiver=user
    )

    return contact
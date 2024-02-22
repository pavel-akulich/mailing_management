from django.core.exceptions import ValidationError


def validate_even(value):
    """
    Validator function to check for prohibited words in a text.

    Args:
        value (str): The text to be validated.

    Raises:
        ValidationError: If a prohibited word is found in the text.

    Returns:
        None
    """
    prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                        'радар', 'попа', 'развод', 'не мошенник']

    for word in prohibited_words:
        if word in value.lower():
            raise ValidationError(f"Вы используете запрещенное слово '{word}' в тексте")

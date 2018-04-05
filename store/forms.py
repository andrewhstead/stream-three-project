from django import forms

SIZE_OPTIONS = (
    ('XS', "XS"),
    ('S', "S"),
    ('M', "M"),
    ('L', "L"),
    ('XL', "XL"),
    ('XXL', "XXL"),
)

QUANTITY_OPTIONS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


class AddToCartForm(forms.Form):
    size = forms.ChoiceField(choices=SIZE_OPTIONS)
    quantity = forms.ChoiceField(choices=QUANTITY_OPTIONS)

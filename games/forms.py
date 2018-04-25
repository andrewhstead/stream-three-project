from django import forms
from datetime import datetime


# Form to select a season when viewing the league standings. Just a simple select field to choose a year.
class SeasonSelectForm(forms.Form):

    SEASON_OPTIONS = (
        (year, year) for year in range(2000, datetime.now().year+1)
    )

    season = forms.ChoiceField(initial=datetime.now().year, choices=SEASON_OPTIONS)

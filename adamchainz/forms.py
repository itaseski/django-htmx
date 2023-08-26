from __future__ import annotations

from django import forms


class OddNumberForm(forms.Form):
    number = forms.IntegerField()


class FilmForm(forms.Form):
    name = forms.CharField()
    content = forms.TimeField()

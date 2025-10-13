from django import forms
from colorfield.forms import ColorField, ColorWidget

from .models import Color, Letter, Icon, AppMenuItem, AppEntityOption

class EditColor(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    value = ColorField(widget=ColorWidget(), required=True)
    modification = forms.DateTimeField(widget=forms.HiddenInput(), required=False,)

    class Meta:
        model = Color
        fields = ('name', 'value', 'modification')

class EditLetter(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    value = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    modification = forms.DateTimeField(widget=forms.HiddenInput(), required=False,)

    class Meta:
        model = Letter
        fields = ('name', 'value', 'modification')

class EditIcon(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    value = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    modification = forms.DateTimeField(widget=forms.HiddenInput(), required=False,)

    class Meta:
        model = Icon
        fields = ('name', 'value', 'modification')

class EditMenuItem(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    label = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    icon = forms.ModelChoiceField(
        queryset=Icon.objects.all().order_by('name'), 
        widget=forms.widgets.Select(attrs={'class':'form-select'}),
        empty_label="")
    option = forms.ModelChoiceField(
        queryset=AppEntityOption.objects.all().order_by('option'), 
        widget=forms.widgets.Select(attrs={'class':'form-select'}),
        empty_label="")
    modification = forms.DateTimeField(widget=forms.HiddenInput(), required=False,)

    class Meta:
        model = AppMenuItem
        fields = ('name', 'label', 'icon', 'option', 'modification')

class EditMenuTree(forms.ModelForm):
    parent = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    child = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    order = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    modification = forms.DateTimeField(widget=forms.HiddenInput(), required=False,)

    class Meta:
        model = AppMenuItem
        fields = ('parent', 'child', 'order', 'modification')

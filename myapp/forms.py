from django import forms
from myapp.models import Order, Student, Topic


class OrderForm(forms.ModelForm):
    """ based on the Order model to create the form """
    class Meta:
        model = Order
        fields = ('student', 'course', 'levels', 'order_date')
        widgets = {
            #'student': forms.RadioSelect(attrs={'class': 'radio'}),
            'order_date': forms.SelectDateWidget(attrs={'class': 'years=date.today()'}),
        }
        Labels = {
            'student': 'Student Name',
            'order_date': 'Order Date',
        }


class InterestForm(forms.Form):
    CHOICES = (
        ('1', 'Yes'),
        ('0', 'No'),
    )

    interested = forms.CharField(widget=forms.RadioSelect(choices=CHOICES))
    levels = forms.IntegerField(initial=1)
    comments = forms.CharField(widget=forms.Textarea(), required=False, label="Additional Comments")


class RegisterForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('username', 'pwd')
    username = forms.CharField(label='Username', min_length=2, max_length=128, error_messages={"required": "invalid username"})
    pwd = forms.CharField(label="Password")
    firstname = forms.CharField(label='First name', min_length=2, max_length=128, error_messages={"required": "invalid input"})
    lastname = forms.CharField(label='Last name', min_length=2, max_length=128, error_messages={"required": "invalid input"})
    city = forms.CharField(label='City', min_length=2, max_length=128, error_messages={"required": "invalid input"})
    addr = forms.CharField(label='Address', min_length=2, max_length=128, error_messages={"required": "invalid input"})
    interested_in = forms.ModelMultipleChoiceField(label='Interested in', queryset=Topic.objects.all(), required=True,
                                                   widget=forms.CheckboxSelectMultiple)

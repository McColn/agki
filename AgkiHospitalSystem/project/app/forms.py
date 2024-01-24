from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'age', 'username', 'password1', 'password2', 'phone']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Username already exists. Please choose a different one.")

        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # Check if the password is strong (you can customize this condition)
        if len(password1) < 8:
            raise ValidationError("Password should be at least 8 characters long.")

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Add additional password confirmation check if needed
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match. Please enter them again.")

        return cleaned_data
    
class UserEditForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label=None)

    
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','age','location','phone','image','position','department','is_doctor','is_laboratorist','is_receptionist','is_patient','is_pharmacist','district','ward','street']

class UserEditForm2(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['district','ward','street','phone']
    
    def clean(self):
        cleaned_data = super().clean()
        district = cleaned_data.get('district')
        ward = cleaned_data.get('ward')
        street = cleaned_data.get('street')
        phone = cleaned_data.get('phone')

        if not district or not ward or not street or not phone:
            raise forms.ValidationError('All fields must be filled.')

        return cleaned_data

class SickInfoForm(forms.ModelForm):

    class Meta:
        model = SickInfoModel
        fields = ['mtaa','kata','wilaya','maelezo','service','hospital']

class SickInfoEditForm(forms.ModelForm):
    
    class Meta:
        model = SickInfoModel
        fields = ['hospital']

class HospitalRegistrationForm(forms.ModelForm):
    # service = forms.ModelChoiceField(queryset=HospitalServices.objects.all(), empty_label=None)
    
    class Meta:
        model = HospitalRegistrationModel
        fields = ['name','level','region','district','ward','street']

class HospitalEditForm(forms.ModelForm):
    
    class Meta:
        model = HospitalRegistrationModel
        fields = ['name','level','location']

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = ContactModel
        fields = ['jina','phone','ujumbe']

class PatientSearchForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['fullname']

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['fullname','age','address','gender','height','pressure','weight']

class ReceptionForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['fullname','age','address','gender','height','pressure','weight']   

class DoctorFirstSessionForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['dalili','possibleDiseases']   

class LaboratoryForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['labResults','testConducted']  

class DoctorSecondSessionForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['actualDiseases','otherRecomendation']  

class PharmacyForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['cost']  

class MedicineAddForm(forms.ModelForm):

    class Meta:
        model = Medicine
        fields = ['medicineName','amount','unitCost','expireDate']  

class MedicineEditForm(forms.ModelForm):

    class Meta:
        model = Medicine
        fields = ['medicineName','amount','unitCost','expireDate']  

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['name','descrption']   

class PrescriptionForm(forms.Form):
    # patient = forms.ModelChoiceField(queryset=Patient.objects.all(), label='Patient')
    medicines = forms.ModelMultipleChoiceField(queryset=Medicine.objects.all(), widget=forms.CheckboxSelectMultiple, label='Medicine')
    
    # dosage = forms.CharField(max_length=100, label='Dosage')
    # amount = forms.IntegerField(min_value=1, label='Amount')
    # cost = forms.IntegerField(min_value=1, label='Cost')
    # prescription_date = forms.DateField(label='prescription_date')

class FaqsForm(forms.ModelForm):
    class Meta:
        model = Faqs
        fields = ['question','answer']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['header','body','image']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['image1','image2','image3','image4','image5','image6']

class IntroVideoForm(forms.ModelForm):
    class Meta:
        model = IntroVideo
        fields = ['title','video_file']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name','username','image','body','time_posted',
                  'views','likes','comments','share']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['header','body']

class FrontPageForm(forms.ModelForm):
    class Meta:
        model = FrontPage
        fields = ['header','body','image']

class WhyUseAgkiForm(forms.ModelForm):
    class Meta:
        model = WhyUseAgki
        fields = ['header','body','image']


    
class ThreadForm(forms.Form):
    username = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Select a user",
    )

    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        
        # Customize the choices with a tuple of (value, label) pairs
        doctors = CustomUser.objects.exclude(is_patient=True)
        choices = [(doctor.username, f"{doctor.username}-{doctor.department.name}") for doctor in doctors]
        self.fields['username'].choices = [("", "Select a user")] + choices

class MessageForm(forms.ModelForm):

	class Meta:
		model = MessageModel
		fields = ['body','image']

# ///////////////////////////////////////

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','slug','description']
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        slug = cleaned_data.get('slug')

        # Add additional password confirmation check if needed
        if name and slug and name != slug:
            raise ValidationError("name and slug do not match. Please enter them again.")

        return cleaned_data
    
class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Item
        fields = ['title','slug','category','price','discount_price','description','image','manufactured_date','expire_date']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['ordered'] 

class BookDoctorForm(forms.ModelForm):
    class Meta:
        model = BookDoctor
        fields = ['district','ward','street','department']

class BookDoctorTimeForm(forms.ModelForm):
    period = forms.DateTimeField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        input_formats=['%Y-%m-%d %H:%M:%S'],  # Specify the desired datetime input format
    )

    class Meta:
        model = BookDoctor
        fields = ['period']
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from app.forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from django.urls import reverse
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
from django.views import View
from django.db.models import Q
from django.http import JsonResponse


# Create your views here.
def home(request):


    today = date.today()
    today_total_patients = Patient.objects.filter(date__date=today).count()
    overall_total_patients = Patient.objects.all().count()

    registered = CustomUser.objects.all()
    registered_total = registered.count()

    newsick = SickInfoModel.objects.exclude(hospital__isnull=False)
    newsick_total = newsick.count()

    hospitals = HospitalRegistrationModel.objects.all()
    hospital_total = hospitals.count()

    jumbe = ContactModel.objects.all()
    jumbe_total = jumbe.count()

    # Get total cost per day
    day_total_cost = Prescription.objects.filter(prescription_date=timezone.now().date()).aggregate(Sum('totalCost'))['totalCost__sum']

    # Get total cost per week
    current_week_number = timezone.now().isocalendar()[1]
    week_total_cost = Prescription.objects.filter(prescription_date__week=current_week_number).aggregate(Sum('totalCost'))['totalCost__sum']

    # Get total cost per month
    current_month = timezone.now().month
    month_total_cost = Prescription.objects.filter(prescription_date__month=current_month).aggregate(Sum('totalCost'))['totalCost__sum']

    # Get total cost per year
    current_year = timezone.now().year
    year_total_cost = Prescription.objects.filter(prescription_date__year=current_year).aggregate(Sum('totalCost'))['totalCost__sum']

    
    x = CustomUser.objects.exclude(is_patient=True)
    form = ContactForm()
    if request.method=='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"message submitted successfully")
            return redirect('home')
        
    context = {
        'registered':registered,
        'registered_total':registered_total,
        'newsick':newsick,
        'newsick_total':newsick_total,
        'hospitals':hospitals,
        'hospital_total':hospital_total,
        'jumbe':jumbe,
        'jumbe_total':jumbe_total,
        'today_total_patients': today_total_patients,
        'overall_total_patients': overall_total_patients,
        'form':form,
        'x':x,
        'day_total_cost': day_total_cost,
        'week_total_cost': week_total_cost,
        'month_total_cost': month_total_cost,
        'year_total_cost': year_total_cost,

      
    }
    return render(request,'app/home.html',context)

def base2(request):
    return render(request,'app/base2.html')

def base(request):
    footer = FooterContact.objects.all()
    total_cart = 0
    if request.user.is_authenticated:
        # Retrieve the total_cart only if the user is authenticated
        total_cart = Order.objects.filter(user=request.user).count()
    context = {
        'total_cart': total_cart,
        'footer':footer,
    }
    return render(request, 'app/base.html', context)

def purpose(request):
    x = PurposeTop.objects.all()
    purposes = Purpose.objects.all()
    success = Success.objects.all()
    footer = FooterContact.objects.all()
    context = {
        'x':x,
        'purposes':purposes,
        'success':success,
        'footer':footer
    }
    return render(request,'app/purpose.html',context)

def index(request):
    total_cart = 0
    user = request.user
    faqs = Faqs.objects.all()
    teams = CustomUser.objects.exclude(is_patient=True)
    news = News.objects.all()
    portfolios = Portfolio.objects.all()
    videos = IntroVideo.objects.all()
    reviews = Review.objects.all()
    services = Service.objects.all()
    frontpages = FrontPage.objects.all()
    whyuseagkis = WhyUseAgki.objects.all()
    footer = FooterContact.objects.all()
    team = Team.objects.all()
    featured = FeaturedPage.objects.all()
    if request.user.is_authenticated:
        # Retrieve the total_cart only if the user is authenticated
        total_cart = Order.objects.filter(user=request.user).count()
        
    context = {
        'faqs':faqs,
        'teams':teams,
        'user':user,
        'news':news,
        'portfolios':portfolios,
        'videos':videos,
        'reviews':reviews,
        'services':services,
        'frontpages':frontpages,
        'whyuseagkis':whyuseagkis,
        'total_cart':total_cart,
        'footer':footer,
        'team':team,
        'featured':featured,
    }
    return render(request,'app/index.html',context)

def faqdelete(request,id):
    x = get_object_or_404(Faqs,id=id)
    x.delete()
    return redirect('index')

def faqedit(request,pk):
    s = Faqs.objects.get(pk=pk)
    form = FaqsForm(instance=s)
    if request.method=='POST':
        form = FaqsForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
            'form':form,
            's':s
         }
    return render(request, 'app/faqedit.html',context)

def faqadd(request):
    if request.method=='POST':
        form = FaqsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FaqsForm()
    
    return render(request, 'app/faqadd.html',{'form':form})

def news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added hospital successfully")
            return redirect('news')
    else:
        form = NewsForm()
    context = {
        'form': form,
    }
    return render(request,'app/news.html',context)

def newsedit(request,pk):
    s = News.objects.get(pk=pk)
    form = NewsForm(instance=s)
    if request.method=='POST':
        form = NewsForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/newsedit.html',context)

def newsdelete(request,pk):
    x = get_object_or_404(News,pk=pk)
    x.delete()
    return redirect('index')

def portfolioedit(request,pk):
    s = Portfolio.objects.get(pk=pk)
    form = PortfolioForm(instance=s)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES,instance=s)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added image successfully")
            return redirect('index')
    else:
        form = PortfolioForm()
    context = {
        'form': form,
        's': s,
    }
    return render(request,'app/portfolioedit.html',context)

def videoedit(request,pk):
    s = IntroVideo.objects.get(pk=pk)
    form = IntroVideoForm(instance=s)
    if request.method=='POST':
        form = IntroVideoForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/videoedit.html',context)

def reviewadd(request):
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added image successfully")
            return redirect('reviewadd')
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request,'app/reviewadd.html',context)

def reviewedit(request,pk):
    s = Review.objects.get(pk=pk)
    form = ReviewForm(instance=s)
    if request.method=='POST':
        form = ReviewForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/reviewedit.html',context)

def serviceadd(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added image successfully")
            return redirect('serviceadd')
    else:
        form = ServiceForm()
    context = {
        'form': form,
    }
    return render(request,'app/serviceadd.html',context)

def serviceedit(request,pk):
    s = Service.objects.get(pk=pk)
    form = ServiceForm(instance=s)
    if request.method=='POST':
        form = ServiceForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/serviceedit.html',context)

def servicedelete(request,pk):
    x = get_object_or_404(Service,pk=pk)
    x.delete()
    return redirect('index')


def whyuseagkiadd(request):
    form = WhyUseAgkiForm()
    if request.method == 'POST':
        form = WhyUseAgkiForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added  successfully")
            return redirect('whyuseagkiadd')
    else:
        form = WhyUseAgkiForm()
    context = {
        'form': form,
    }
    return render(request,'app/whyuseagkiadd.html',context)

def whyuseagkiedit(request,pk):
    s = WhyUseAgki.objects.get(pk=pk)
    form = WhyUseAgkiForm(instance=s)
    if request.method=='POST':
        form = WhyUseAgkiForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/whyuseagkiedit.html',context)

def whyuseagkidelete(request,pk):
    x = get_object_or_404(WhyUseAgki,pk=pk)
    x.delete()
    return redirect('index')


def frontPageedit(request,pk):
    s = FrontPage.objects.get(pk=pk)
    form = FrontPageForm(instance=s)
    if request.method=='POST':
        form = FrontPageForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/frontPageedit.html',context)

def reviewdelete(request,pk):
    x = get_object_or_404(Review,pk=pk)
    x.delete()
    return redirect('index')


def registration(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('signin')
        else:
            # Form is not valid, errors will be displayed in the template
            pass

    context = {
        'form': form
    }
    return render(request,'app/registration.html',context)

def userlist(request):
    x = CustomUser.objects.all().order_by('-id')
    context = {
        'x':x
    }
    return render(request,'app/userlist.html',context)

def useredit(request, id):
    s = CustomUser.objects.get(id=id)
    departments = Department.objects.all()

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=s)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added user successfully")
            return redirect('userlist')
    else:
        form = UserEditForm(instance=s)
    context = {
        'form': form,
        's': s,
        'departments':departments,
    }
    return render(request, 'app/useredit.html', context)


def userdelete(request,id):
    x = get_object_or_404(CustomUser,id=id)
    x.delete()
    return redirect('userlist')

def profile(request):
    user = request.user
    return render(request, 'app/profile.html',{'user':user})

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']

        user = authenticate(username=username, password=password1)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Check specific scenarios for error messages
            try:
                existing_user = CustomUser.objects.get(username=username)
                # User exists, but password is incorrect
                messages.error(request, 'Incorrect password for the provided username')
            except CustomUser.DoesNotExist:
                # User with provided username does not exist
                messages.error(request, 'User with the provided username does not exist')

            return redirect('signin')

    return render(request, 'app/signin.html')


def signout(request):
    logout(request)
    return redirect ('index')
    return render(request,'app/signout.html')

@login_required
def sickinfo(request):
    suggested_hospital = None  # Initialize suggested_hospital as None
    
    # form = SickInfoForm()
    if request.method=='POST':
        form = SickInfoForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)

            # Custom logic to suggest a nearby hospital
            suggested_hospital = suggest_nearby_hospital(report)
            
            # If a suggested hospital is found, assign it to the report
            if suggested_hospital:
                report.hospital = suggested_hospital
                report.hospital_assigned = True

            report.user=request.user
            report.save()
            # return redirect('home')
    else:
        form = SickInfoForm()

    context = {
            'form':form, 'suggested_hospital':suggested_hospital,
         }

    return render(request,'app/sickinfo.html',context)

from django.db.models import Q

def suggest_nearby_hospital(report):
    # Compare mtaa, street, kata, ward, wilaya, and district
    hospitals = HospitalRegistrationModel.objects.filter(
        Q(street__iexact=report.mtaa) |  # Compare mtaa to street
        Q(ward__iexact=report.kata) |    # Compare kata to ward
        Q(district__iexact=report.wilaya) ,  # Compare wilaya to district
        Q(service__iexact=report.service)   # Compare wilaya to district

    ).first()

    return hospitals


def sickinfoEdit(request,pk):
    s = SickInfoModel.objects.get(pk=pk)
    form = SickInfoEditForm(instance=s)
    if request.method=='POST':
        form = SickInfoEditForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('sickinfolist')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/sickinfoEdit.html',context)

def sickinfoDelete(request,id):
    x = get_object_or_404(SickInfoModel,id=id)
    x.delete()
    return redirect('sickinfolist')


def sickinfolist(request):
    x = SickInfoModel.objects.all().order_by('-id')
    context = {
        'x':x
    }
    return render(request,'app/sickinfolist.html',context)

def sickinfolistprocesed(request):
    x = SickInfoModel.objects.exclude(hospital__isnull=True)
    context = {
        'x':x
    }
    return render(request,'app/sickinfolistprocesed.html',context)


def sickinfolistunprocesed(request):
    x = SickInfoModel.objects.exclude(hospital__isnull=False)
    context = {
        'x':x
    }
    return render(request,'app/sickinfolistunprocesed.html',context)
def hospitalRegistration(request):
    
    form = HospitalRegistrationForm()
    if request.method=='POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"you added hospital successfully")
            return redirect('hospitalRegistration')
    context = {
            'form':ModelForm
        }
    return render(request,'app/hospitalRegistration.html',context)


def registeredHosptal(request):
    x = HospitalRegistrationModel.objects.all().order_by('-id')
    
    context = {
            'x':x
        }
    return render(request,'app/registeredHosptal.html',context)

def hospitalDelete(request,id):
    x = get_object_or_404(HospitalRegistrationModel,id=id)
    x.delete()
    return redirect('registeredHosptal')

def hospitalEdit(request,id):
    s = HospitalRegistrationModel.objects.get(id=id)
    form = HospitalEditForm(instance=s)
    if request.method=='POST':
        form = HospitalEditForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('registeredHosptal')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/hospitalEdit.html',context)

def contact_list(request):
    x = ContactModel.objects.all()
    
    context = {
            'x':x
        }
    
    return render(request,'app/contact_list.html',context)

def contactDelete(request,id):
    x = get_object_or_404(ContactModel,id=id)
    x.delete()
    return redirect('contact_list')

def detailedUser(request,id):
    detaileduser = CustomUser.objects.get(id=id)
    context = {
        'detaileduser':detaileduser
    }
    return render(request,'app/detailedUser.html',context)
    
def patient(request):
    form = PatientForm()
    if request.method=='POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"patient added successfully")
            return redirect('patientList')
    context = {
            'form':form
        }
    return render(request,'app/patient.html',context)
    
def patientList(request):
    form = PatientSearchForm(request.POST or None)
    x = Patient.objects.all().order_by('-id')
    patients = Patient.objects.all()

    if request.method == 'POST':
        patients = Patient.objects.filter(fullname__icontains=form['fullname'].value())
    context = {
            'x':x,
            'form':form,
            'patients':patients
            
        }
    return render(request,'app/patientList.html',context)

def patientDetail(request,id):
    x = Patient.objects.get(id=id)
    prescriptions = Prescription.objects.filter(patient=x)

    # Calculate the total cost for the patient
    sum_total_cost = sum([prescription.totalCost for prescription in prescriptions])


    context = {
        'x':x,
        'prescriptions':prescriptions,
        'sum_total_cost':sum_total_cost,
    }
    return render(request,'app/patientDetail.html',context)

def patientDelete(request,id):
    x = get_object_or_404(Patient,id=id)
    x.delete()
    return redirect('patientList')

def reception(request,id):
    s = Patient.objects.get(id=id)
    form = ReceptionForm(instance=s)
    if request.method=='POST':
        form = ReceptionForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('patientDetail', args=[id]))
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/reception.html',context)

def doctorFirstSession(request,id):
    s = Patient.objects.get(id=id)
    form = DoctorFirstSessionForm(instance=s)
    if request.method=='POST':
        form = DoctorFirstSessionForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('patientDetail', args=[id]))
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/doctorFirstSession.html',context)

def laboratory(request,id):
    s = Patient.objects.get(id=id)
    form = LaboratoryForm(instance=s)
    if request.method=='POST':
        form = LaboratoryForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('patientDetail', args=[id]))
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/laboratory.html',context)

def doctorSecondSession(request,id):
    s = Patient.objects.get(id=id)
    form = DoctorSecondSessionForm(instance=s)
    
    if request.method=='POST':
        form = DoctorSecondSessionForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('patientDetail', args=[id]))
    context = {
            'form':form,
            's':s,
            
         }

    return render(request,'app/doctorSecondSession.html',context)

def pharmacy(request,id):
    s = Patient.objects.get(id=id)
    form = PharmacyForm(instance=s)
    if request.method=='POST':
        form = PharmacyForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('patientDetail', args=[id]))
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/pharmacy.html',context)

def medicine(request):
    medicines = Medicine.objects.all()
    return render(request, 'app/medicine.html', {'medicines': medicines})

def medicineAdd(request):
    form = MedicineAddForm()
    if request.method=='POST':
        form = MedicineAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"medicine added successfully")
            return redirect('medicineAdd')
    context = {
            'form':form
        }
    return render(request,'app/medicineAdd.html',context)

def medicineEdit(request,id):
    s = Medicine.objects.get(id=id)
    form = MedicineEditForm(instance=s)
    if request.method=='POST':
        form = MedicineEditForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('medicine')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/medicineEdit.html',context)

def invoice(request,id):
    x = Patient.objects.get(id=id)
    prescriptions = Prescription.objects.filter(patient=x)
    # Calculate the total cost for the patient
    sum_total_cost = sum([prescription.totalCost for prescription in prescriptions])


    context = {
        'x':x,
        'prescriptions':prescriptions,
        'sum_total_cost':sum_total_cost,
    }
    return render(request,'app/invoice.html',context)

def department(request):
    x = Department.objects.all()
    context = {
        'x':x,
    }
    return render(request,'app/department.html',context)

def departmentAdd(request):
    form = DepartmentForm()
    if request.method=='POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"department added successfully")
            return redirect('department')
    context = {
            'form':form,
        }
    return render(request,'app/departmentAdd.html',context)

def departmentEdit(request,id):
    s = Department.objects.get(id=id)
    form = DepartmentForm(instance=s)
    if request.method=='POST':
        form = DepartmentForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('department')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/departmentEdit.html',context)

def prescription_form(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            medicines = form.cleaned_data['medicines']
            dosage = form.cleaned_data['dosage']
            amount = form.cleaned_data['amount']
            prescription_date = form.cleaned_data['prescription_date']

            for medicine in medicines:
                # Save prescription data to the database for each selected medicine
                prescription = Prescription.objects.create(
                    medicine=medicine,
                    patient=patient,
                    dosage=dosage,
                    amount=amount,
                    prescription_date=prescription_date,
                )
                prescription.save()

            # Redirect to a success page or display a success message
            # return HttpResponseRedirect('/success/')
    else:
        form = PrescriptionForm()

    return render(request, 'app/prescription_form.html', {'form': form})

def prescription_list(request):
    prescriptions = Prescription.objects.select_related('medicine', 'patient').order_by('patient__fullname')

    grouped_prescriptions = {}
    for prescription in prescriptions:
        patient_name = prescription.patient.fullname
        if patient_name not in grouped_prescriptions:
            grouped_prescriptions[patient_name] = []
        grouped_prescriptions[patient_name].append({
            'medicine': prescription.medicine.medicineName,
            'dosage': prescription.dosage,
            'amount': prescription.amount
        })

    return render(request, 'app/prescription_list.html', {'prescriptions': grouped_prescriptions})

def edit_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    prescription = Prescription.objects.get(patient_id=x.id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            # Redirect to a success page or display a success message
            return redirect('patientDetail', id=prescription.patient.id)
    else:
        form = PrescriptionForm(instance=prescription)

    context = {
        'form': form,
        'prescription': prescription,
    }
    return render(request, 'app/edit_prescription.html', context)

def process_prescription(request, patient_id):
    patient = Patient.objects.get(id=patient_id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            selected_medicines = form.cleaned_data['medicines']
            # Process selected medicines, create PrescriptionDetail objects here
            for medicine in selected_medicines:
                dosage = request.POST.get(f'dosage_{medicine.id}')  # Assuming you have inputs with names like 'dosage_1', 'dosage_2', etc.
                cost = request.POST.get(f'cost_{medicine.id}')  # Similarly, inputs for cost
                amount = request.POST.get(f'amount_{medicine.id}')  # Similarly, inputs for cost
                totalCost = request.POST.get(f'totalCost_{medicine.id}')  # Similarly, inputs for cost

                # Create PrescriptionDetail objects with selected medicine, dosage, and cost
                Prescription.objects.create(medicine=medicine, patient=patient, dosage=dosage, cost=cost,amount=amount,totalCost=totalCost)

                # Decrease remainAmount of associated Medicine
                # if amount is not None and medicine.remainAmount >= int(amount):
                #     medicine.remainAmount -= int(amount)
                #     medicine.save()

            # Redirect or show success message
            # return HttpResponseRedirect('/success/')
    else:
        form = PrescriptionForm()

    return render(request, 'app/process_prescription.html', {'form': form, 'patient': patient})

def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)

    if request.method == 'POST':
        # Get the prescription details before deletion
        medicine = prescription.medicine
        patient = prescription.patient
        amount_given = prescription.amount

        # Restore the remainAmount of the medicine
        if medicine:
            medicine.remainAmount += amount_given
            medicine.save()

        # Delete the prescription
        prescription.delete()
        messages.success(request, 'Prescription deleted successfully.')

        # Redirect to the patientDetail page with the appropriate patient id
        return redirect('patientDetail', id=patient.id)

    # Redirect to the patientDetail page with a default patient id if not a POST request
    
    return redirect('patientDetail', id=prescription.patient.id)

def patient_count_per_period(request):
    # Get the current day of the week
    current_day = datetime.now().strftime('%A')
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_year = datetime.now().year


    # Assuming your Patient model has a field named 'date'
    # Replace 'date' with the actual field name in your model
    patients_per_day = Patient.objects.values('date').annotate(patient_count=models.Count('id'))
    patients_per_month = Patient.objects.filter(date__month=current_month, date__year=current_year)
    patients_per_year = Patient.objects.filter(date__year=current_year)


    # Make current_date offset-aware
    current_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Prepare data for each week of the month
    weeks_data = []
    months_data = []

    # Calculate the start and end dates for each week
    while current_date.month == current_month:
        week_start = current_date
        week_end = current_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
        week_data = {
            'week_start': week_start,
            'week_end': week_end,
            'patient_count': patients_per_month.filter(date__range=(week_start, week_end)).count()
        }
        weeks_data.append(week_data)
        current_date = week_end + timedelta(days=1)


    # Prepare data for each day of the week (Monday to Sunday)
    days_data = [
        {'day_name': 'Monday', 'patient_count': 0},
        {'day_name': 'Tuesday', 'patient_count': 0},
        {'day_name': 'Wednesday', 'patient_count': 0},
        {'day_name': 'Thursday', 'patient_count': 0},
        {'day_name': 'Friday', 'patient_count': 0},
        {'day_name': 'Saturday', 'patient_count': 0},
        {'day_name': 'Sunday', 'patient_count': 0}
    ]


    # Calculate the start and end dates for each month
    for month in range(1, 13):
        month_start = timezone.now().replace(year=current_year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = month_start + timedelta(days=31)  # Assuming the maximum number of days in a month
        month_data = {
            'month_name': month_start.strftime('%B'),  # Get the month name
            'patient_count': patients_per_year.filter(date__range=(month_start, month_end)).count()
        }
        months_data.append(month_data)


    # Update data with actual patient counts
    for day_data in days_data:
        day_number = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}[day_data['day_name']]
        day_data['patient_count'] = sum(1 for item in patients_per_day if item['date'].weekday() == day_number)

    # for week_data in weeks_data:
    #     week_data['patient_count'] = sum(1 for item in patients_per_month if week_data['week_start'] <= item['date'] <= week_data['week_end'])

    context = {
        'days_data': days_data, 
        'current_day': current_day,
        'weeks_data': weeks_data, 'current_month': current_month, 'current_year': current_year,
        'months_data': months_data, 'current_year': current_year,
        }
    
    
    return render(request, 'app/patient_count_per_period.html', context)

def total_cost_per_period(request):
    # Assuming Prescription model has a 'prescription_date' field
    prescriptions = Prescription.objects.all()

    # Calculate the start and end dates for each week of the month
    current_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    weeks_data = []

    while current_date.month == timezone.now().month:
        week_start = current_date
        week_end = current_date + timedelta(days=6, hours=23, minutes=59, seconds=59)

        # Aggregate total cost for prescriptions within the week
        total_cost = prescriptions.filter(prescription_date__range=(week_start, week_end)).aggregate(Sum('totalCost'))['totalCost__sum'] or 0

        week_data = {
            'week_start': week_start,
            'week_end': week_end,
            'total_cost': total_cost
        }

        weeks_data.append(week_data)
        current_date = week_end + timedelta(days=1)

    
     # Get the current date
    current_date = timezone.now().date()

    # Calculate the start and end dates of the current week (Monday to Sunday)
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Query the Prescription model for entries within the current week
    prescriptions_in_week = Prescription.objects.filter(
        prescription_date__range=[start_of_week, end_of_week]
    )

    # Prepare data for each day of the week (Monday to Sunday)
    days_data = [
        {'day_name': 'Sunday', 'total_cost': 0},
        {'day_name': 'Monday', 'total_cost': 0},
        {'day_name': 'Tuesday', 'total_cost': 0},
        {'day_name': 'Wednesday', 'total_cost': 0},
        {'day_name': 'Thursday', 'total_cost': 0},
        {'day_name': 'Friday', 'total_cost': 0},
        {'day_name': 'Saturday', 'total_cost': 0},
        
    ]

    # Calculate the total cost for each day of the week
    for day_entry in days_data:
        day_name = day_entry['day_name']
        total_cost_for_day = prescriptions_in_week.filter(prescription_date__week_day=days_data.index(day_entry) + 1).aggregate(Sum('totalCost'))['totalCost__sum']

        # If there are no prescriptions for a particular day, set the total cost to 0
        day_entry['total_cost'] = total_cost_for_day if total_cost_for_day is not None else 0



    # Calculate the start and end dates of the current year (January 1st to December 31st)
    start_of_year = current_date.replace(month=1, day=1)
    end_of_year = current_date.replace(month=12, day=31)

    # Query the Prescription model for entries within the current year
    prescriptions_in_year = Prescription.objects.filter(
        prescription_date__range=[start_of_year, end_of_year]
    )

    # Prepare data for each month of the year (January to December)
    months_data = [
        {'month_name': 'January', 'total_cost': 0},
        {'month_name': 'February', 'total_cost': 0},
        {'month_name': 'March', 'total_cost': 0},
        {'month_name': 'April', 'total_cost': 0},
        {'month_name': 'May', 'total_cost': 0},
        {'month_name': 'June', 'total_cost': 0},
        {'month_name': 'July', 'total_cost': 0},
        {'month_name': 'August', 'total_cost': 0},
        {'month_name': 'September', 'total_cost': 0},
        {'month_name': 'October', 'total_cost': 0},
        {'month_name': 'November', 'total_cost': 0},
        {'month_name': 'December', 'total_cost': 0},
    ]

    # Calculate the total cost for each month of the year
    for month_entry in months_data:
        month_name = month_entry['month_name']
        total_cost_for_month = prescriptions_in_year.filter(prescription_date__month=months_data.index(month_entry) + 1).aggregate(Sum('totalCost'))['totalCost__sum']

        # If there are no prescriptions for a particular month, set the total cost to 0
        month_entry['total_cost'] = total_cost_for_month if total_cost_for_month is not None else 0


    context = {
        'weeks_data': weeks_data,'days_data':days_data,'months_data':months_data,
    }

    return render(request, 'app/total_cost_per_period.html', context)
    

# //////////////////////////////chatting with doctor//////



class ListThreads(View):
    def get(self, request, *args, **kwargs):
        if request.user.payment_status:  # Check payment_status
            threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
            context = {'threads': threads}
            return render(request, 'app/inbox.html', context)
        else:
            return HttpResponse("PAY IN ORDER TO CHAT")

class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        chatpay = ChatPay.objects.all()  # Proper indentation here

        context = {
            'form': form,
            'chatpay': chatpay
        }
        return render(request, 'app/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = CustomUser.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            messages.error(request, 'Invalid username')
            return redirect('create-thread')


class ThreadView(View):
	def get(self, request, pk, *args, **kwargs):
		form = MessageForm()
		thread = ThreadModel.objects.get(pk=pk)
		message_list = MessageModel.objects.filter(thread__pk__contains=pk)
		context = {
			'thread':thread,
			'form':form,
			'message_list':message_list,
		}
		return render(request, 'app/thread.html', context)

class CreateMessage(View):
	def post(self, request, pk, *args, **kwargs):
		#add image
		form = MessageForm(request.POST,request.FILES)
		##############
		thread = ThreadModel.objects.get(pk=pk)

		if thread.receiver == request.user:
			receiver = thread.user
		else:
			receiver = thread.receiver

		#add image
		if form.is_valid():
			message = form.save(commit=False)
			message.thread = thread
			message.sender_user = request.user
			message.receiver_user = receiver
			message.save()
		##########################

		return redirect('thread', pk=pk)

# ////////////////////////////////////////////////////////////////////////

def medicineCategory(request):
    x = Category.objects.all()
    context = {
        'x':x
    }
    return render(request,'app/medicineCategory.html',context)

def addCategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'category added successfully')
            return redirect('addCategory')
        else:
            pass
    context = {
        'form':form
    }
    
    return render(request,'app/addCategory.html',context)

def editCategory(request,id):
    s = Category.objects.get(id=id)
    form = CategoryForm(instance=s)
    if request.method=='POST':
        form = CategoryForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('medicineCategory')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'app/editCategory.html',context)

@login_required
def medicationAdd(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST,request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user=request.user
            report.save()
            messages.success(request,'category added successfully')
            return redirect('medicationAdd')
    else:
        form = ItemForm()
    context = {
        'form':form
    }
    
    return render(request,'app/medicationAdd.html',context)

def medicationRequest(request, category_slug=None):
    footer = FooterContact.objects.all()
    categories = Category.objects.all().order_by('-id')
    items = Item.objects.all().order_by('-id')
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=category)

    if 'q' in request.GET:
        q = request.GET['q']

        # Split the query into individual words
        search_words = q.split()

        # Initialize an empty Q object
        combined_q = Q()

        # Add conditions for each word using OR
        for word in search_words:
            combined_q |= Q(title__icontains=word) | Q(description__icontains=word)

        # Filter items based on the combined Q object
        items = items.filter(combined_q)

    context = {
        'data': items,
        'footer': footer,
        'categories': categories,
        'category': category,
    }
    return render(request, 'app/medicationRequest.html', context)

def get_suggestions(request):
    if 'q' in request.GET:
        query = request.GET['q']
        search_terms = query.split()  # Split the query into individual terms
        combined_q = Q()

        for term in search_terms:
            combined_q |= Q(title__icontains=term) | Q(description__icontains=term)

        suggestions = Item.objects.filter(combined_q).values_list('title', 'description')
        suggestions = set(s for suggestion in suggestions for s in suggestion)
        return JsonResponse(list(suggestions), safe=False)
    else:
        return JsonResponse([], safe=False)

def get_suggestions_from_database(query):
    # Fetch suggestions based on the entered query from the database
    suggestions = Item.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).values_list('title', 'description')
    suggestions = set(s for suggestion in suggestions for s in suggestion)
    return list(suggestions)


def medicationList(request):
    x = Item.objects.all()
    context = {
        'x':x
    }
    return render(request,'app/medicationList.html',context)

def medicationAllCart(request):
    x = Order.objects.all()
    context = {
        'x':x
    }
    return render(request,'app/medicationAllCart.html',context)

def medicationCartSingle(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Filter items based on the currently logged-in user
        x = Order.objects.filter(user=request.user)

        context = {
            'x': x,
        }
        return render(request, 'app/medicationCartSingle.html', context)

def medicationListSingle(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Filter items based on the currently logged-in user
        user_items = Item.objects.filter(user=request.user)

        context = {
            'x': user_items
        }
        return render(request, 'app/medicationListSingle.html', context)
    
def medicationProcess(request,id):
    s = OrderItem.objects.get(id=id)
    form = OrderItemForm(instance=s)
    if request.method=='POST':
        form = OrderItemForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('medicationCartSingle')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'app/medicationProcess.html',context)
    

def medicationDescription(request,id):
    x = Item.objects.get(id=id)
    context = {
        'x':x
    }
    return render(request,'app/medicationDescription.html',context)

def medicationDescription(request,id):
    x = Item.objects.get(id=id)
    context = {
        'x':x
    }
    return render(request,'app/medicationDescription.html',context)

def medicationDescriptionStaff(request,id):
    x = Item.objects.get(id=id)
    context = {
        'x':x
    }
    return render(request,'app/medicationDescriptionStaff.html',context)
 
def medicationDescriptionEdit(request,id):
    s = Item.objects.get(id=id)
    form = ItemForm(instance=s)
    if request.method=='POST':
        form = ItemForm(request.POST, request.FILES, instance=s) 
        if form.is_valid():
            form.save()
            
            return redirect('medicationList')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/medicationDescriptionEdit.html',context)

def bookLabTest(request):
    footer = FooterContact.objects.all()
    laboratory_categories = LaboratoryTestCategory.objects.all()

    context = {
        'footer': footer,
        'laboratory_categories': laboratory_categories,
    }
    return render(request, 'app/bookLabTest.html', context)

def bookDoctor(request):
    departments = Department.objects.all()
    footer = FooterContact.objects.all()
    form = BookDoctorForm()
    if request.method == 'POST':
        form = BookDoctorForm(request.POST,request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user=request.user
            report.save()
            messages.success(request,'Request is send successfully, the time and day for appointment will send to your sms after processing')
            return redirect('bookDoctor')
    else:
        form = BookDoctorForm()
    context = {
        'departments':departments,
        'form':form,
        'footer':footer,
    }
    return render(request,'app/bookDoctor.html',context)

class OrderSummaryView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        user = request.user  # Get the current user

        # Retrieve user data for the form
        form = UserEditForm2(instance=user)
        footer = FooterContact.objects.all()

        context = {
            'order': order,
            'form': form,
            'footer':footer,
        }
        return render(request, 'app/order_summary.html', context)

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        user = request.user  # Get the current user

        form = UserEditForm2(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "User information updated successfully.")
            return redirect('order_summary')
        
        context = {
            'order': order,
            'form': form,
        }
        return render(request, 'app/order_summary.html', context)
    

    
def add_to_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item}'s quantity was updated")
            return redirect('order_summary')
        else:
            order.items.add(order_item)
            order.save()
            messages.success(request, f"{item} was added to your Order")
            return redirect('order_summary')

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered=False, ordered_date=ordered_date)
        order.items.add(order_item)
        order.save()
        messages.success(request, f"{item} was added to your Order")
        return redirect('order_summary')
    

def remove_from_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_id=item.id).exists():
            order.items.remove(order_item)
            order.save()
            messages.success(request, f"{item.title} was removed from your Order")
                
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.title} was not in your Order")
            return redirect('order_summary')
    else:
        messages.info(request, "You don't have an active order!")
        return redirect('order_summary')


def remove_single_from_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order.save()
            messages.success(request, f"{item}'s quantity was updated")
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.title} was not in your Order")
            return redirect('order_summary')
    else:
        messages.info(request, "You don't have an active Order!")
        return redirect('order_summary')

def doctorBookingAll(request):
    x = BookDoctor.objects.all()
    context = {
        'x':x,
    }
    return render(request,'app/doctorBookingAll.html',context)

def doctorBookingDepartment(request):
    # Check if the user is a doctor and belongs to any department
    user_profile = get_object_or_404(CustomUser, id=request.user.id, is_doctor=True)

    # Get the departments the user belongs to
    user_departments = user_profile.department.all()  # Assuming 'department' is a ForeignKey field in CustomUser

    # Retrieve all doctors for the user's departments
    x = CustomUser.objects.filter(is_doctor=True, department__in=user_departments)

    context = {'x': x}
    
    return render(request, 'app/doctorBookingDepartment.html', context)

def doctorBookingTime(request,id):
    s = BookDoctor.objects.get(id=id)
    form = BookDoctorTimeForm(instance=s)
    if request.method=='POST':
        form = BookDoctorTimeForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            messages.success(request,'you updated time successfully')
            return redirect('doctorBookingTime',id=id)
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'app/doctorBookingTime.html',context)


# purpose section ##########################################
def purposeFirst(request,id):
    s = PurposeTop.objects.get(id=id)
    form = PurposeFirstForm(instance=s)
    if request.method=='POST':
        form = PurposeFirstForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'app/purposeFirst.html',context)

def purposeSecond(request,id):
    s = PurposeTop.objects.get(id=id)
    form = PurposeSecondForm(instance=s)
    if request.method=='POST':
        form = PurposeSecondForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'app/purposeSecond.html',context)

def purposeProblem(request,id):
    s = PurposeTop.objects.get(id=id)
    form = PurposeProblemForm(instance=s)
    if request.method=='POST':
        form = PurposeProblemForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'app/purposeProblem.html',context)

def purposeSolution(request,id):
    s = PurposeTop.objects.get(id=id)
    form = PurposeSolutionForm(instance=s)
    if request.method=='POST':
        form = PurposeSolutionForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'app/purposeSolution.html',context)

def purposeEdit(request,id):
    s = Purpose.objects.get(id=id)
    form = PurposeForm(instance=s)
    if request.method=='POST':
        form = PurposeForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'app/purposeEdit.html',context)

def purposeAdd(request):
    form = PurposeForm()
    if request.method=='POST':
        form = PurposeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"purpose added successfully")
            return redirect('purposeAdd')
    context = {
            'form':form
        }
    return render(request,'app/purposeAdd.html',context)

def purposeDelete(request,id):
    x = get_object_or_404(Purpose,id=id)
    x.delete()
    return redirect('purpose')

def purposeSuccessAdd(request):
    form = SuccessForm()
    if request.method=='POST':
        form = SuccessForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"SuccessForm added successfully")
            return redirect('purposeAdd')
    context = {
            'form':form
        }
    return render(request,'app/purposeSuccessAdd.html',context)

def purposeSuccessEdit(request,id):
    s = Success.objects.get(id=id)
    form = SuccessForm(instance=s)
    if request.method=='POST':
        form = SuccessForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'app/purposeSuccessEdit.html',context)

def purposeSuccessDelete(request,id):
    x = get_object_or_404(Success,id=id)
    x.delete()
    return redirect('purpose')

def purposeVideoEdit(request,id):
    s = PurposeTop.objects.get(id=id)
    form = PurposeVideoForm(instance=s)
    if request.method=='POST':
        form = PurposeVideoForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/purposeVideoEdit.html',context)

def footerContact(request,id):
    s = FooterContact.objects.get(id=id)
    form = FooterContactForm(instance=s)
    if request.method=='POST':
        form = FooterContactForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/footerContact.html',context)

def teamAdd(request):
    form = TeamForm()
    if request.method=='POST':
        form = TeamForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Team member added successfully")
            
            return redirect('teamAdd')
    context = {
            'form':form,
         }

    return render(request,'app/teamAdd.html',context)

def teamEdit(request,id):
    s = Team.objects.get(id=id)
    form = TeamForm(instance=s)
    if request.method=='POST':
        form = TeamForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/teamEdit.html',context)

def teamDelete(request,id):
    x = get_object_or_404(Team,id=id)
    x.delete()
    return redirect('index')

def featuredEdit(request,id):
    s = FeaturedPage.objects.get(id=id)
    form = FeaturedPageForm(instance=s)
    if request.method=='POST':
        form = FeaturedPageForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/featuredEdit.html',context)

def featuredAdd(request):
    form = FeaturedPageForm()
    if request.method=='POST':
        form = FeaturedPageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Sponsor added successfully")
            
            return redirect('featuredAdd')
    context = {
            'form':form,
         }

    return render(request,'app/featuredAdd.html',context)

def featuredDelete(request,id):
    x = get_object_or_404(FeaturedPage,id=id)
    x.delete()
    return redirect('index')

def chatpayedit(request,id):
    s = ChatPay.objects.get(id=id)
    form = ChatPayForm(instance=s)
    if request.method=='POST':
        form = ChatPayForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'app/chatpayedit.html',context)

def packageAdd(request):
    form = LaboratoryTestCategoryForm()
    if request.method=='POST':
        form = LaboratoryTestCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"package added successfully")
            
            return redirect('packageAdd')
    context = {
            'form':form,
         }

    return render(request,'app/packageAdd.html',context)

def packageItem(request):
    form = LaboratoryTestForm()
    if request.method=='POST':
        form = LaboratoryTestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"package item added successfully")
            
            return redirect('packageItem')
    context = {
            'form':form,
         }

    return render(request,'app/packageItem.html',context)




def order_confirmation_success(request):
    return render(request, 'app/order_confirmation_success.html')

def confirm_order(request, category_id):
    category = LaboratoryTestCategory.objects.get(pk=category_id)
    if request.method == 'POST':
        form = OrderConfirmationForm(request.POST)
        if form.is_valid():
            # Save the order confirmation data to the database
            form.save()
            return redirect('order_confirmation_success')
    else:
        form = OrderConfirmationForm(initial={'category': category_id, 'user': request.user})
    return render(request, 'app/confirm_order.html', {'form': form, 'category': category})

def booklabtestview(request):
    x = OrderConfirmation.objects.all()
    context = {
        'x':x
    }
    return render(request,'app/booklabtestview.html',context)

def booklabtestprocess(request,id):
    s = OrderConfirmation.objects.get(id=id)
    form = OrderConfirmationProcessForm(instance=s)
    if request.method=='POST':
        form = OrderConfirmationProcessForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('booklabtestview')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'app/booklabtestprocess.html',context)
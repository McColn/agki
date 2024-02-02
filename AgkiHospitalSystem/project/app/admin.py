from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(SickInfoModel)
admin.site.register(HospitalRegistrationModel)
admin.site.register(ContactModel)
admin.site.register(Medicine)
admin.site.register(Patient)
admin.site.register(Department)

admin.site.register(Prescription)

admin.site.register(Faqs)
admin.site.register(News)
admin.site.register(Portfolio)
admin.site.register(IntroVideo)
admin.site.register(Review)
admin.site.register(Service)
admin.site.register(FrontPage)
admin.site.register(WhyUseAgki)

admin.site.register(MessageModel)

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)

admin.site.register(BookDoctor)

admin.site.register(Purpose)
admin.site.register(Success)
admin.site.register(PurposeTop)

admin.site.register(FooterContact)
admin.site.register(FeaturedPage)
admin.site.register(LaboratoryTestCategory)
admin.site.register(LaboratoryTest)
admin.site.register(Team)

admin.site.register(ChatPay)

admin.site.register(OrderConfirmation)

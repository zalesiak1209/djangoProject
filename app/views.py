# Standard Library
import datetime

# Django


from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
# 3rd-party
from django.views.generic import ListView
from factory.compat import force_text
# Local
from .forms import CustomUserCreationForm
from .forms import UserForm
from .models import Kategoria
from .models import Ogloszenie
from .tokens import account_activation_token

User = get_user_model()


def category_show_content(request):
    kategoria = Kategoria.objects.all()
    context = {'kategoria': kategoria}
    return render(request, 'app/kategoria_show.html', context)


def category_show_all_content(request, kategoria_id):
    kategoriaog = Ogloszenie.objects.filter(kategoria_id=kategoria_id)
    paginator = Paginator(kategoriaog, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/kategoria_show.html', {'page_obj': page_obj})


def ogloszenie_show_detail(request, kategoria_id, ogloszenie_id):
    kategoria = Ogloszenie.objects.filter(kategoria_id=kategoria_id)
    ogloszenie = Ogloszenie.objects.get(id=ogloszenie_id)
    context = {'kategoria': kategoria, 'ogloszenie': ogloszenie}
    return render(request, 'app/ogloszenie_detail.html', context)


def delete_old_ogloszenie():
    f = Ogloszenie.objects.all()
    for foo in f:
        if foo.expiration_date < timezone.now():
            foo.delete()
        pass


def handle_uploaded_file(f):
    with open('static/upload_images/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def create_ogloszenie(request):
    context = {}
    ogloszenie_form = modelform_factory(model=Ogloszenie,
                                        fields=['nazwa_ogloszenia', 'krotki_opis_ogloszenia', 'tresc_ogloszenia',
                                                'kategoria', 'rok_produkcji', 'miejscowosc',
                                                'numer_telefonu', 'cena', 'zdjecie']
                                        )
    context['form'] = ogloszenie_form
    if request.method == 'POST':
        form = ogloszenie_form(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = User.objects.get(id=request.user.id)  # przypisywanie id usera do tworzonego obiektu
            obj.expiration_date = timezone.now() + datetime.timedelta(days=30)  # data waznosci obietku
            obj.zdjecie = form.cleaned_data['zdjecie']
            delete_old_ogloszenie()  # usuwanie obiektu po x czasu            ^
            obj.save()

            context['form'] = form
            context['Potwierdzenie'] = 'Ogloszenie zostało dodane'
            return render(request, 'app/ogloszenie_create.html', context)
        else:
            context['Potwierdzenie'] = "Ogloszenie nie zostało dodane"
            context['form'] = form
            return render(request, 'app/ogloszenie_create.html', context)
    else:
        return render(request, 'app/ogloszenie_create.html', context)


@login_required
def home(request):
    return render(request, "registration/success.html", {})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/verify_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            mail_subject = 'Activate your account.'
            print(mail_subject, message)
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(mail_subject, message, to=[to_email]) # do wysylania email via smtp gmail
            # email.send()
            return render(request, 'registration/confirm_email.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'registration/confirmation_email_success.html', {})
    else:
        return render(request, 'registration/confirmation_email_fail.html', {})


def show_my_ogloszenia(request):
    id = request.user.id
    author = Ogloszenie.objects.filter(author_id=id)
    paginator = Paginator(author, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/my_ogloszenia.html', {'author': author, 'page_obj': page_obj})


def moje_ogloszenia_show_detail(request, id):
    ogloszenie = Ogloszenie.objects.get(id=id)
    context = {'ogloszenie': ogloszenie}
    return render(request, 'app/ogloszenie_detail.html', context)


def delete_ogloszenie(request, id):
    deleteog = Ogloszenie.objects.get(id=id)
    deleteog.delete()
    return render(request, 'app/delete_ogloszenie.html')


def log_in_to_continue(request):
    return render(request, "app/log_in_message.html", {})


def show_my_profile(request):
    id = request.user.id
    profile = User.objects.get(id=id)
    context = {'profile': profile}
    return render(request, 'app/user_profile.html', context)


def profil_edit(request):
    context = {}
    a_data = User.objects.get(id=request.user.id)
    a_form = UserForm(request.POST or None, instance=a_data)
    if a_form.is_valid():
        a_form.save()
        context['form'] = a_form
        context['Potwierdzenie'] = 'Profil został edytowany'
        return render(request, 'app/edit_profil.html', context)
    else:
        context['Potwierdzenie'] = "Profil nie został edytowany"
        context['form'] = a_form
        return render(request, 'app/edit_profil.html', context)


def image(request, id):
    context = get_object_or_404(Ogloszenie, id=id)
    return render(request, 'app/ogloszenie_detail.html', context)


def image2(request, id):
    context = get_object_or_404(Ogloszenie, id=id)
    return render(request, 'app/my_ogloszenia.html', context)


def image3(request, id):
    context = get_object_or_404(Ogloszenie, id=id)
    return render(request, 'searching/search_results.html', context)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "messages/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        # send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False) #to send email smtp gmail
                        print(subject, email)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset/password_reset.html",
                  context={"password_reset_form": password_reset_form})


class SearchResultsView(ListView):
    model = Ogloszenie
    template_name = "searching/search_results.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Ogloszenie.objects.filter(
            Q(nazwa_ogloszenia__icontains=query) | Q(tresc_ogloszenia__icontains=query)
        )
        # paginator = Paginator(object_list, 10)
        # page_number = self.request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        return object_list

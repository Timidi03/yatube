from django.http import HttpResponse
from django.shortcuts import render
from .forms import EnhanceFrom
from django.core.mail import send_mail


def exchange(request):
    form = EnhanceFrom(request.POST)
    if request.method == 'POST' and form.is_valid():
        send_msg(**form.cleaned_data)
        return thankyou(request)
    return render(request, "index1.html", {'form': form})

def thankyou(request):
    return render(request, "thankyou.html")

def send_msg(email, name, title, artist, genre, price, comment):
    subject = f"Обмен {artist}-{title}"
    body = f"""Предложение на обмен диска от {name} ({email})

    Название: {title}
    Исполнитель: {artist}
    Жанр: {genre}
    Стоимость: {price}
    Комментарий: {comment}

    """
    send_mail(
        subject, body, email, ["admin@rockenrolla.net", ],
    )
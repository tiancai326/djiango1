from functools import wraps

from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .model_forms import LoginForm, SignonForm
from .models import Member, News


def member_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("member_id"):
            return redirect("app:login")
        return view_func(request, *args, **kwargs)

    return wrapper


@member_login_required
def home(request):
    member = Member.objects.get(id=request.session["member_id"])
    news_types = [
        {
            "key": key,
            "name": name,
            "count": News.objects.filter(news_type=key).count(),
        }
        for key, name in News.NEWS_TYPE_CHOICES
    ]
    latest_news = News.objects.all()[:6]
    return render(
        request,
        "home.html",
        {
            "active_menu": "home",
            "member": member,
            "news_types": news_types,
            "latest_news": latest_news,
        },
    )


@member_login_required
def news_list(request, news_type):
    type_names = dict(News.NEWS_TYPE_CHOICES)
    if news_type not in type_names:
        return redirect("app:home")

    new_list = News.objects.filter(news_type=news_type)
    return render(
        request,
        "newsList.html",
        {
            "active_menu": "news",
            "newName": type_names[news_type],
            "newList": new_list,
            "current_type": news_type,
            "news_types": News.NEWS_TYPE_CHOICES,
        },
    )


@member_login_required
def news_detail(request, news_id):
    mynew = get_object_or_404(News, id=news_id)
    News.objects.filter(id=mynew.id).update(views=mynew.views + 1)
    mynew.views += 1
    return render(
        request,
        "newsDetail.html",
        {
            "active_menu": "news",
            "mynew": mynew,
        },
    )


@member_login_required
def search(request):
    keyword = request.GET.get("keyword", "").strip()
    if keyword:
        new_list = News.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
        new_name = f'关于 "{keyword}" 的搜索结果'
    else:
        new_list = News.objects.none()
        new_name = "新闻搜索"

    return render(
        request,
        "searchList.html",
        {
            "active_menu": "news",
            "newName": new_name,
            "newList": new_list,
            "keyword": keyword,
        },
    )


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            member = Member.objects.filter(username=username).first()
            if member is not None and check_password(password, member.password):
                request.session["member_id"] = member.id
                request.session["member_username"] = member.username
                next_url = request.POST.get("next") or "app:home"
                return redirect(next_url)
            form.add_error(None, "账号或密码错误。")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout(request):
    request.session.flush()
    return render(request, "logout.html")


def signon(request):
    if request.method == "POST":
        form = SignonForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.password = make_password(form.cleaned_data["password1"])
            member.save()
            return redirect("app:login")
    else:
        form = SignonForm()

    return render(request, "signon.html", {"form": form})

from functools import wraps

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from haystack.query import SearchQuerySet

from .face_detect import detect_faces, draw_faces, encode_image, read_image
from .model_forms import LoginForm, ResumeForm, SignonForm
from .models import Ad, Member, News, Product


PRODUCT_CATEGORY_MAP = {
    "robot": "家用机器人",
    "monitor": "智能监控机器人",
    "face": "工业机器人",
}


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
    query = request.GET.get("q") or request.GET.get("keyword", "")
    query = query.strip()

    results = SearchQuerySet().models(News).load_all()
    if query:
        results = results.auto_query(query).highlight()
    else:
        results = results.none()

    paginator = Paginator(results, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "search/search.html",
        {
            "active_menu": "news",
            "query": query,
            "page_obj": page_obj,
            "paginator": paginator,
            "result_count": paginator.count,
        },
    )


@member_login_required
def products(request, product_name):
    product_type = PRODUCT_CATEGORY_MAP.get(product_name)
    if product_type is None:
        return redirect("app:products", product_name="robot")

    product_queryset = (
        Product.objects.filter(productType=product_type)
        .prefetch_related("productImgs")
        .order_by("-publishDate")
    )
    paginator = Paginator(product_queryset, 2)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "productList.html",
        {
            "active_menu": "products",
            "sub_menu": product_name,
            "product_categories": tuple(PRODUCT_CATEGORY_MAP.items()),
            "productName": product_type,
            "productList": page_obj,
            "page_obj": page_obj,
        },
    )


@member_login_required
def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.prefetch_related("productImgs"),
        id=product_id,
    )
    Product.objects.filter(id=product.id).update(views=product.views + 1)
    product.views += 1
    product_slug = next(
        (slug for slug, name in PRODUCT_CATEGORY_MAP.items() if name == product.productType),
        "robot",
    )

    return render(
        request,
        "productDetail.html",
        {
            "active_menu": "products",
            "sub_menu": product_slug,
            "product": product,
            "product_slug": product_slug,
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


def contact(request):
    return render(
        request,
        "contact.html",
        {
            "active_menu": "contactus",
            "sub_menu": "contact",
        },
    )


def recruit(request):
    ad_list = Ad.objects.all().order_by("-publishDate")
    if request.method == "POST":
        resume_form = ResumeForm(data=request.POST, files=request.FILES)
        if resume_form.is_valid():
            resume = resume_form.save()
            send_mail(
                "简历提交成功",
                "您好，您的简历已经提交成功，请等待审核。",
                settings.DEFAULT_FROM_EMAIL,
                [resume.email],
                fail_silently=False,
            )
            msg = "<br><br>成功新增个人简历，确认邮件已发送..."
            return render(
                request,
                "OK.html",
                {
                    "active_menu": "contactus",
                    "sub_menu": "recruit",
                    "msg": msg,
                },
            )
    else:
        resume_form = ResumeForm()

    return render(
        request,
        "recruit.html",
        {
            "active_menu": "contactus",
            "sub_menu": "recruit",
            "AdList": ad_list,
            "form": resume_form,
        },
    )


def platform(request):
    return render(
        request,
        "platform.html",
        {
            "active_menu": "service",
            "sub_menu": "platform",
        },
    )


@csrf_exempt
def facedetect(request):
    if request.method != "POST":
        return JsonResponse({"faceNum": 0, "faces": []})

    image = read_image(request.FILES.get("image"))
    if image is None:
        return JsonResponse({"faceNum": -1, "faces": []})

    faces = detect_faces(image)
    return JsonResponse({"faceNum": len(faces), "faces": faces})


@csrf_exempt
def facedetect_demo(request):
    if request.method != "POST":
        return JsonResponse({"faceNum": 0, "faces": [], "image": ""})

    image = read_image(request.FILES.get("image"))
    if image is None:
        return JsonResponse({"faceNum": -1, "faces": [], "image": ""})

    faces = detect_faces(image)
    output = draw_faces(image, faces)
    return JsonResponse(
        {
            "faceNum": len(faces),
            "faces": faces,
            "image": encode_image(output),
        }
    )

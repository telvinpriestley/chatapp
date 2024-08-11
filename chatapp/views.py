from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from django.utils.crypto import get_random_string

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q, Subquery,OuterRef, F
from django.core.paginator import Paginator


# Create your views here.
def landing(request):
    return render(request, 'auth/landing.html', {})

# @login_required(login_url="/loginFirst")
def home(request):
    rooms = Room.objects.all().prefetch_related(
        'roomlike_set', 'roomcomment_set', 'roomshare_set'
    ).order_by('-created')

    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'rooms': rooms,
    }

    return render(request, 'home.html', context)

@login_required(login_url="/loginFirst")
def add_comment(request):
    if request.method == 'POST' and request.POST['room_id'] and request.POST['comment']:
        room_id = request.POST['room_id']
        comment_text = request.POST['comment']
        room = get_object_or_404(Room, id=room_id)
        
        if comment_text.strip():
            RoomComment.objects.create(room=room, user=request.user, message=comment_text)
            messages.success(request, 'Done!')
            return redirect('home')
    else:
        messages.warning(request, "an error, try again")
        return redirect("home")

@login_required(login_url="/loginFirst")
def add_like(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    like_instance = RoomLike.objects.filter(room=room, user=request.user).first()

    if like_instance:
        like_instance.delete()
        messages.success(request, 'Done!')
    else:
        RoomLike.objects.create(room=room, user=request.user)
        messages.success(request, 'Done!')
    return redirect('home')

@login_required(login_url="/loginFirst")
def add_share(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    share_instance = RoomShare.objects.filter(room=room, user=request.user).first()
    if share_instance:
        # what to do when this person has already shared
        messages.success(request, 'Done!')
    else:
        RoomShare.objects.create(room=room, user=request.user)
        messages.success(request, 'Done!')
        return redirect('home')


@login_required(login_url="/loginFirst")
def add_comment_reply(request):
    if request.method == 'POST' and request.POST['message'] and request.POST['comment_id']:
        comment_id= request.POST['comment_id']
        message = request.POST['message']
        comment_inst = get_object_or_404(RoomComment, id=comment_id)
        
        if message.strip():
            CommentReply.objects.create(comment=comment_inst, user=request.user, message=message)
            messages.success(request, 'Done!')
            return redirect('home')
        else: 
            messages.warning(request, 'no reply passed!')
            return redirect('home')
    else:
        messages.error(request, 'incorect entery!')
        return redirect('home')

@login_required(login_url="/loginFirst")
def add_comment_like(request, comment_id):
    comment = get_object_or_404(RoomComment, id=comment_id)
    comment_like_instance = CommentLike.objects.filter(comment=comment, user=request.user).first()

    if comment_like_instance:
        comment_like_instance.delete()
        messages.success(request, 'Done!')
    else:
        CommentLike.objects.create(comment=comment, user=request.user)
        messages.success(request, 'Done!')
    return redirect('home')

def room_page(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, "manage/room.html", {"room": room})

def userinfo(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_info = user
    return render(request, "manage/userinfo.html", {"user_info": user_info})

@login_required(login_url="/loginFirst")
def profile(request):
    rooms = Room.objects.filter(host=request.user).prefetch_related(
        'roomlike_set', 'roomcomment_set', 'roomshare_set'
    ).order_by('-created')
    return render(request, "manage/profile.html", {"room_info":rooms})


def signup_view(request):
    messages.info(request, "Please provide information to be Registered")
    return render(request, "auth/signup.html", {})


def login_view(request):
    all_users = User.objects.all()
    data = {"persons": all_users}
    return render(request, "auth/login.html", context=data)


def loginFirst(request):
    messages.warning(request, "please login first")
    return redirect("/login_view")


def logout_view(request):
    logout(request)
    messages.success(request, "logged out, see you another time")
    return redirect("/")


def send_email_verification(useremail, usercode):
    try:
        # send_mail(
        #     subject="email_verification",
        #     message= f'Your OTP IS {usercode}',
        #     from_email="afanwitelvin@gmail.com",
        #     recipient_list=[useremail],
        #     fail_silently=False,
        # )
        print(f"email verification code {usercode} sent to {useremail}")
    except Exception as err:
        messages.error(f"Error sending email: {err}")
        return redirect("/verification_view")


def emailVerification_sign_up(request):
    if (
        request.method == "POST"
        and request.POST["first_name"]
        and request.POST["last_name"]
        and request.POST["email"]
        and request.POST["password"]
        and request.POST["username"]
        and request.POST["address"]
        and request.POST["contact"]
        and request.POST["gender"]
    ):
        if User.objects.filter(email=request.POST["email"]).exists():
            messages.warning(request, "The email you used already exist")
            return redirect("/signup")
        else:
            client_email = request.POST["email"]
            # random_number = [random.randint(1, 10) for _ in range(4)]
            code = get_random_string(4, "1234567890")
            tempdata = Tempstore(
                fname=request.POST["first_name"],
                lname=request.POST["last_name"],
                email=request.POST["email"],
                password=request.POST["password"],
                username=request.POST["username"],
                address=request.POST["address"],
                contact=request.POST["contact"],
                gender=request.POST["gender"],
                code=code,
            )
            tempdata.save()
            send_email_verification(useremail=client_email, usercode=code)
            return redirect("/verification_view")
    else:
        messages.error(request, " please enter all the  details")
        return redirect("/signup_view")


def verification_view(request):
    messages.success(request, "fill in the 4 digit code to verify your email account")
    return render(request, "auth/everification.html", {})
    # return render(request, "auth/login_verify.html", {})


def verification_proper(request):
    if request.method == "POST" and request.POST["passcode"]:
        if Tempstore.objects.filter(code=request.POST["passcode"]).exists():
            tempdata = Tempstore.objects.get(code=request.POST["passcode"])
            user_inst = User.objects.create_user(
                username=tempdata.username,
                email=tempdata.email,
                password=tempdata.password,
                first_name=tempdata.fname,
                last_name=tempdata.lname,
            )

            user_inst.save()
            details = UserDetails(
                user=user_inst,
                contact=tempdata.contact,
                address=tempdata.address,
                gender=tempdata.gender,
            )
            details.save()
            tempdata.delete()
            messages.success(request, "user email verification done in ok")
            data = {"user_detail": user_inst}
            return render(request, "auth/login.html", context=data)
        else:
            messages.warning(request, "email verification not correct")
            return redirect("/verification_view")
    else:
        messages.warning(request, "please enter email verification code")
        return redirect("/verification_view")


def login_email_verify(request):
    if (
        request.method == "POST"
        and request.POST["password"]
        and request.POST["username"]
    ):
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is not None:
            client = User.objects.get(username=request.POST["username"])
            client_email = client.email
            code = get_random_string(4, "1234567890")
            send_email_verification(useremail=client_email, usercode=code)
            messages.info(request, "enter the 4 digit code to login")
            data = {
                "code_check": code,
                "passwordsend": request.POST["password"],
                "usernamesend": request.POST["username"],
            }
            return render(request, "auth/login_verify.html", context=data)

        else:
            messages.error(request, "user not found !")
            return redirect("/login_view")


def login_verify_view(request):
    return render(request, "auth/login_verify.html", {})


def login_proper(request):
    if (
        request.method == "POST"
        and request.POST["passcode"]
        and request.POST["correctcode"]
        and request.POST["password"]
    ):
        if request.POST["passcode"] == request.POST["correctcode"]:
            user = authenticate(
                request,
                username=request.POST["username"],
                password=request.POST["password"],
            )

            login(request, user)
            messages.success(request, "log in successful !")
            return redirect("home")

        else:
            messages.error(request, "wrong code !")
            return redirect("/login_view")
    else:
        messages.error(request, "enter all details !")
        return redirect("/login_view")

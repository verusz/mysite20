from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
# Create your views here.

# Import necessary classes
from django.http import HttpResponse, HttpResponseRedirect
# from pandas.tests.extension import decimal
from django.urls import reverse
import datetime
from .forms import *
from .models import Topic, Course, Student, Order

# lab 8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    """
    default homepage for 127.0.0.1:8000, users can select the landing web-page
    """
    content = "<h1> Welcome! </h1> " \
              "<p> Please select the pages: </p> " \
              "<ul> " \
              "<li> <a href={}> Courses </a></li> " \
              "<li> <a href={}> About </a></li> " \
              "</ul>".format('myapp/', 'myapp/about/')
    #return HttpResponse(content)
    return render(request, 'myapp/home.html')


# Create your views here.
def index0(request):
    """
    the index page of myapp
    """
    # for displaying topics
    top_list = Topic.objects.all().order_by('id')[:10]
    data = {
        'top_list': top_list,
    }
    return render(request, 'myapp/index0.html', data)


# about page
def about(request):
    """
    the about page of myapp
    """
    cookie_val = request.COOKIES.get('about_visits', None)
    if cookie_val is None:  # no cookies
        print('first time!')
        cookie_val = 0

    cookie_val = int(cookie_val) + 1
    text = 'This is an E-learning Website! Search our Topics to find all available Courses. So far we have ' + str(cookie_val) + ' times visiting'
    data = {
        'text': text,
    }
    response = render(request, 'myapp/about.html', data)
    response.set_cookie('about_visits', cookie_val, max_age=600)
    return response


# detail page
def detail(request, top_no):
    """
    the detail page of myapp
    """
    topic = Topic.objects.all().filter(id=top_no)
    cours = Course.objects.all().filter(topic_id=top_no)
    data = {
        'topic': topic,
        'cour': cours,
    }
    return render(request, 'myapp/detail.html', data)


def index(request):
    """
       the index page of myapp
       """
    top_list = Topic.objects.all().order_by('id')[:10]
    data = {
        'top_list': top_list,
        'your_name': request.user.username,
        'loginInfo': request.session.get('last_login')
    }

    return render(request, 'myapp/index.html', data)


def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def place_order(request):
    text = "You can place an order here."
    msg = ''
    stu = request.user
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_status = 1
            name = request.user
            order.student = Student.objects.get(username=name)
            if order.levels <= order.course.stages:
                stu = order.student
                course = order.course
                level = order.levels
                price = course.discount()
                print(price)
                order.save()
                msg = 'Your course has been ordered successfully.'
                return render(request, 'myapp/order_response.html',
                              {'msg': msg, 'student': stu, 'course': course, 'level': level, 'price': price})
            else:
                msg = 'You exceeded the number of levels for this course.'
                return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist, 'text': text, 'stu': str(stu)})


def course_detail(request, cour_id):
    if request.method == 'POST':  # show interests in the current course
        form = InterestForm(request.POST)
        # print(form.interested)
        if form.is_valid():
            course = Course.objects.get(id=cour_id)
            #interest = form.save(commit=False)
            interested = request.POST.get("interested", "")
            level = request.POST.get("levels", "")
            comment = request.POST.get("comments", "")
            if str(interested) == '1':
                course.interested += 1
            # print(course.id)
            course.save()
            top_list = Topic.objects.all().order_by('id')[:10]
            data = {
                'top_list': top_list,
                'your_name': "UWindsor",
            }
            return render(request, 'myapp/index.html', data)

    else:
        course = Course.objects.filter(id=cour_id)
        form = InterestForm()
        # form.interested = '1'
        data = {'form': form, 'course': course, 'course_id': cour_id}
        return render(request, 'myapp/course_detail.html', data)


# lab 8
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # print(user, username, password)
        if user:
            if user.is_active:
                login(request, user)
                now_time = datetime.datetime.now().strftime('%F %T')
                request.session['last_login'] = str(now_time)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    # logout(request)
    # log out the user by deleting request session
    request.session.flush()
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def myaccount(request):
    # if not request.user.is_authenticated():
    #     return redirect('myapp:user_login')

    students = Student.objects.filter(username=request.user.username)
    data = dict()
    # check the username
    if students.count() == 0:
        data['error'] = 'You are not a registered student!'
        data['username'] = request.user.username
    else:
        # The first and last name of the student.
        # All the courses that have been ordered by the student.
        # All the topics the student is interested in.
        # for stu in students:
        data['first_name'] = students[0].first_name
        data['last_name'] = students[0].last_name
        data['orders'] = Order.objects.filter(student_id=students[0].user_ptr_id)
        # all_topics = students[0].interested_in
        # print(all_topics.all())
        data['interested_topics'] = students[0].interested_in.all()
    return render(request, 'myapp/myaccount.html', data)


def test_cookie(request):
    """ this is for testing the cookies """
    cookie_val = request.COOKIES.get('cookie_name', None)
    if cookie_val is None:  # no cookies
        response = HttpResponse("First time Visiting")
        response.set_cookie('cookie_name', 'cookie_value')
        return response
    else:   # already has cookies
        return HttpResponse("the cookie name: {}\n, the cookie value: {}".format('cookie_name', cookie_val))


def register(request):
    form_obj = RegisterForm()
    if request.method == 'POST':
        form_obj = RegisterForm(request.POST)
        if form_obj.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("pwd", "")
            firstname = request.POST.get("firstname", "")
            lastname = request.POST.get("lastname", "")
            city = request.POST.get("city", "")
            addr = request.POST.get("addr", "")
            interested_in = request.POST.getlist("interested_in", "")
            print(interested_in)
            password = make_password(password)
            add_register = Student(username=username, password=password, first_name=firstname, last_name=lastname, city=city, address=addr)
            add_register.save()

            return render(request, "myapp/registerResponse.html")
    return render(request, "myapp/register.html", {'form_obj': form_obj})


def registerResponse(request):
    return render(request, "myapp/registerResponse.html")
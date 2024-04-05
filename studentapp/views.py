from django.shortcuts import render,HttpResponse,redirect
from studentapp.models import student,Cart,orders
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q 
import random
import razorpay
from django.core.mail import send_mail


# Create your views here.

def index_pg(request):
    context={}
    allstu = student.objects.all()
    context['students']=allstu
    return render(request,'new_index.html',context)

def filterByBranch(request,brname):
    #fetch the student data based on specific branch
    #send it to 'new_index.html'
    context={}
    # allstu = student.objects.filter(branch=brname)
    #applying multiple conditions usiing Q
    # ex1: select * from student where branch="   " and percent >= 60.00
    c1 = Q(branch=brname)
    c2 = Q(percent__gte = 60.00)
    allstu = student.objects.filter(c1 & c2)
    # # defining the range using Q
    # # ex2: select * from student where percent between 60.00 and 70.00;
    # # select * from student where percent >= 60.00 and percent <= 70.00;
    # c1 = Q(percent__gte = 60.00)
    # c2 = Q(percent__lte = 70.00)
    # allstu = student.objects.filter(c1 & c2)
    
    context['students']=allstu
    return render(request,'new_index.html',context)

def rangeSearch(request):
    context={}
    min = request.GET['min']
    max  = request.GET['max']
    # # defining the range using Q
    # # ex2: select * from student where percent between min and max;
    # # select * from student where percent >= min and percent <= max;
    c1 = Q(percent__gte = min)
    c2 = Q(percent__lte = max)
    allstu = student.objects.filter(c1 & c2)
    context['students']=allstu
    return render(request,'new_index.html',context)

def sortStudents(request,ord):
    context={}
    if ord == '0':
        # print('ascending sort')
        col='percent'
    else:
        # print('descending')
        col='-percent'
    allstu = student.objects.all().order_by(col)
    # print(type(ord),ord)
    context['students']=allstu
    return render(request,'new_index.html',context)

def home_fn(request):
    #return HttpResponse('login successfully')
    return render(request,'home.html')

# def add_student(request):
#     return render(request,'addstu.html')

def studata_fn(request):
    if request.method=='GET':
        print('within get()')
        return render (request, 'addstu.html')
    else:
        print('wihtin post')
        n = request.POST['stuname']
        b = request.POST['stubranch']
        p = request.POST['stuperc']
        stu = student.objects.create(name = n,branch = b,percent = p)
        stu.save()
        print('student saved:')
        #print('received:',n, b, p)
        #return render(request,'home.html')
        return redirect("/index")
    
def dashboard(request):
    data = student.objects.all()
    #print(type(data))
    context={}
    context['studata']=data
    return render (request, 'dashboard.html',context)

def delstudent(request,rid):
    print('delete student:',rid)
    data = student.objects.filter(id=rid)
    print('TYPE:',type(data))
    print('recieved data:',data) 
    data.delete()  
    return redirect('/index')

def updateStudent(request,rid):
    if request.method=='GET':
        data = student.objects.filter(id=rid)
        # we need to access and use only first recrd data[0]
        #so the single student object is sent to template
        context={}
        context['student']=data[0]
        return render(request, 'updatestudent.html',context)
    else:
        n = request.POST["stuname"]
        b = request.POST['stubranch']
        p = request.POST['stuperc']
        data = student.objects.filter(id=rid)
        updatedStu = data.update(name = n,branch = b,percent = p)
        return redirect("/index")

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        context={}
        n= request.POST['username']
        e= request.POST['useremail']
        p= request.POST['userpassword']
        c= request.POST['confirmpassword']
        if n=='' or p=='':
            context['errorMsg']='Kindly enter all fields'
            return render(request,'register.html',context)
        elif p!=c:
            context['errorMsg']='Password and confirm password must be same'
            return render(request,'register.html',context)
        else:
            # u = User.objects.create(username=n,password=p,email=e)
            # u.save()
            u = User.objects.create(username=n,email=e)
            u.set_password(p)#for encrypted password
            u.save()
            #print('received registration data:',n,p)
            context['success']='Registered successfully!!'
            return render(request,'login.html',context)


def user_login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        context={}
        u=request.POST['username']
        p=request.POST['userpassword']
        #print('login details:',u,p)
        if u=='' or p=='':
            context['errorMsg']='plz provide all details'
            return render(request,'login.html',context)
        else:
            u = authenticate(username=u, password=p)
            if u is not None:
                login(request,u)
                print(request.user.is_authenticated)
                return render(request,'new_index.html')
            else:
                context['errorMsg']='plz provide correct credentials'
                return render(request,'login.html',context)
                

def user_logout(request):
    logout(request)
    return redirect('/index')

def showDetails(request,sid):
    stu = student.objects.filter(id=sid)
    context={}
    context['student']=stu[0]
    return render(request,'details.html',context)


def addtocart(request,sid):
    userid=request.user.id
    if userid:
        user = User.objects.filter(id=userid)
        stu=student.objects.filter(id=sid)
        c=Cart.objects.create(sid=stu[0],uid=user[0])
        c.save()
        return HttpResponse('cart added')
    else:
        return render(request,'login.html')


def viewcart(request):
    userid=request.user.id
    if userid:
        user = User.objects.filter(id=userid)
        mycart=Cart.objects.filter(uid=user[0])
        context={}
        context['cart']=mycart
        return render(request,'viewcart.html',context) 
    else:
        return render(request,'login.html')

def updateQuantity(request,incr,cid):
    c = Cart.objects.filter(id = cid)
    if incr=='0': #decr qty
        new_qunat = c[0].quantity -1
    else: #incr qty
        new_qunat = c[0].quantity +1
    c.update(quantity = new_qunat)
    return redirect('/viewcart')

def deletefromcart(request,cid):
    cart=Cart.objects.filter(id=cid)
    cart.delete()
    return redirect("/viewcart")

def sendemail(request):
    print(request.user.id)
    print(request.user.email)
    return HttpResponse('email sent')



def placeorder(request):
    context={}
    userid = request.user.id
    order_id = random.randrange(1000,9999)
    #fetch current cart
    mycart = Cart.objects.filter(uid = userid)
    #add the cart items to order
    for cart in mycart:
        ord = orders.objects.create(order_id=order_id,sid=cart.sid,uid=cart.uid,quantity=cart.quantity)
        ord.save()
    mycart.delete()#clear cart table for current user
    mycart = orders.objects.filter(order_id=order_id)#fetch order details
    #calculate count and total
    count = len(mycart)
    total = 0
    for cart in mycart:
        total += cart.quantity*cart.sid.percent
    context['count']=count
    context['total']= total
    context['mycart']=mycart
    return render(request,'placeorder.html',context)

def makepayment(request):
    #get the orderdetails for current loggedin user
    userid = request.user.id
    ordDetails = orders.objects.filter(uid = userid)
    #calculate the billamount
    bill=0
    for ord in ordDetails:
        bill += ord.sid.percent*ord.quantity
        ordId = ord.order_id
    client = razorpay.Client(auth=("rzp_test_xWsyoS8I0wZaOO","Hm5k91ikEbSrJLQ9hPz657xW"))
    data = { "amount": bill*100, "currency": "INR", "receipt": str(ordId) }
    payment = client.order.create(data=data)
    # print(payment)
    # return HttpResponse('success')
    context={}
    context['data']=payment
    return render (request,'pay.html',context)



def sendmail (request) :
    msg = "order details are:"
    email = request. user.email
    print (request. user.id, email)
    send_mail(
    "EKart Order Placed Successfully",
    msg,
    "sapitkar@gmail.com"
    [emaill],
    fail_silently=False,
    )
    return HttpResponse("mail sent successfully!!")



# def user_orders(request):
#     orders = orders.objects.filter(user=request.user)
#     return render(request,'orders/user_orders.html', {'orders': orders})

# def userorders(request):
#     userid=request.user.id
#     if userid:
#         user = User.objects.filter(id=userid)
#         orders = orders.objects.filter(oid=orders[0])
#         context={}
#         context['myorders']= orders
#         return render(request,'user_orders.html',context) 
#     else:
#         return render(request,'login.html')
#         46++
#         0.and.

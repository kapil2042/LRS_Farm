from datetime import datetime, timedelta
from time import time
import calendar
from django.shortcuts import redirect, render
from model.models import *
from django.contrib.auth import authenticate,get_user_model
from django.contrib import messages
from pulp import *
import xlwt
from django.http import HttpResponse
import numpy as np
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.mail import send_mail


#login
def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        if username.isnumeric():
            user = authenticate(username=username,password=password)
        else:
            username = get_user_model().objects.get(email=username.lower()).username
            user = authenticate(username=username,password=password)
        if user is not None:
            request.session['admin'] = user.username
            return redirect(home)
        else:
            messages.error(request,'Invalid Mobile number or Email or Password!')
            return redirect(home)
    else:
        return redirect(home)

#log out
def logout(request):
    del request.session['admin']
    return redirect(home)

#forgot password
def forgotpass(request):
    if request.method == 'POST':
        import socket
        email = request.POST.get('uemail')
        try:
            username = get_user_model().objects.get(email=email.lower()).username
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encpass = fernet.encrypt(email.encode())
            aau=encpass.decode()
            lrs=key.decode()
            time1=int(time() * 1000)
            IPAddr = socket.gethostbyname(socket.gethostname())
            a='Reset Password link => '+IPAddr+':8000/chklink?unm='+username+'&lrs='+lrs+'&aau='+aau+'&time='+str(time1)
            send_mail(
                'Reset Password - LRS_AAU',
                a,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request,'Please check your Email for reset password!')
        except:
            messages.error(request,'Entered Email-id is not registered with the website')
        return redirect(home)
    else:
        return redirect(home)

#check mail link
def chklink(request):
    if request.method == 'GET':
        unm = request.GET['unm']
        key = request.GET['lrs']
        email = request.GET['aau']
        timeurl = request.GET['time']
        timenow=int(time() * 1000)
        fernet = Fernet(key.encode())
        decemail = fernet.decrypt(email.encode()).decode()
        if int(timeurl) in range((timenow-3600000),timenow,1):
            try:
                username = get_user_model().objects.get(email=decemail.lower()).username
                if str(username) == str(unm):
                    context = {
                        'username' : username,
                    }
                    return render(request,'resetpass.html',context)
                else:
                    messages.error(request,'Somthing Was Wrong! Please Retry to reset Your Password')
            except:
                messages.error(request,'Somthing Was Wrong! Please Retry to reset Your Password')
        else:
            messages.error(request,'Link is expired!')
    return redirect(home)

#reset password
def resetpass(request):
    if request.method == 'POST':
        unm = request.POST['uunm']
        psw = request.POST['npsw']
        try:
            usr = get_user_model().objects.get(username=unm)
            usr.set_password(psw)
            usr.save()
            messages.success(request,"Your Password Changed Successfully")
        except:
            messages.error(request,'Somthing Was Wrong! Please Retry to reset Your Password')
    return redirect(home)


#home page
def home(request):
    global admin,userdetails
    if request.session.has_key('admin'):
        userdetails = get_user_model().objects.get(username=request.session['admin'])
        admin = request.session['admin']
    else:
        admin = 'Null'
        userdetails ={
            'first_name' : '',
            'last_name' : '',
        }
    data = {
        'admin' : admin,
        'userdetails' : userdetails,
    }
    return render(request,'Home.html',data)

#edit profile
def editprofile(request):
    if request.session.has_key('admin'):
        data = {
            'admin' : admin,
            'userdetails' : userdetails,
        }
        if request.method == 'POST':
            username = request.POST.get('unm')
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            usr = get_user_model().objects.get(username=username)
            usr.first_name = first_name
            usr.last_name = last_name
            usr.save()
            messages.success(request,"Your Profile Changed Successfully")
            return redirect(home)
    return render(request,'editprofile.html',data)

#change password
def changepass(request):
    if request.session.has_key('admin'): 
        data = {
            'admin' : admin,
            'userdetails' : userdetails,
        }
        if request.method == 'POST':
            current_password = request.POST['cpsw']
            new_password = request.POST['npsw']
            user = authenticate(username=userdetails.username,password=current_password)
            if user is not None:
                usr = get_user_model().objects.get(username=userdetails.username)
                usr.set_password(new_password)
                usr.save()
                messages.success(request,"Your Password Changed Successfully")
                return redirect(home)
            else:
                messages.error(request,"Current password does not match")
                return redirect(changepass)
    return render(request,'changepass.html',data)

#add new admin
def addnewadmin(request):
    if request.session.has_key('admin'): 
        data = {
            'admin' : admin,
            'userdetails' : userdetails,
        }
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            mnum = request.POST['mnum']
            email = request.POST['email']
            psw = request.POST['psw']
            get_user_model().objects.create_superuser(username=mnum,password=psw,email=email,first_name=fname,last_name=lname)
            messages.success(request,"New Admin Added Successfully")
            return redirect(users)
    return render(request,'addnewadmin.html',data)

#Users Admin
def users(request):
    if request.session.has_key('admin'): 
        usr = get_user_model().objects.all()
        data = {
            'admin' : admin,
            'userdetails' : userdetails,
            'usr' : usr,
        }
    return render(request,'users.html',data)

#Admin Delete
def userdelete(request,username):
    if request.session.has_key('admin'):
        if request.method == 'POST':
            psw = request.POST['password']
            user = authenticate(username=request.session['admin'],password=psw)
            if user is not None:
                usr = get_user_model().objects.get(username=username)
                usr.delete()
            else:
                messages.error(request,"Your Password is Wrong!")
    return redirect(users)

#add new admin
def vstat(request):
    if request.session.has_key('admin'):
        d = datetime.now()
        y = [ i for i in range(2020,int(d.strftime('%Y'))+1)]
        m = [ i for i in range(1,13)]
        if request.method == 'POST':
            year = request.POST['plotyaer']
            month = request.POST['plotmonth']
        else:
            year = d.strftime('%Y')
            month = d.strftime('%m')
        if month == '2':
            if (int(year) % 400 == 0) and (int(year) % 100 == 0):
                daterange = optimize_log.objects.filter(date__gte=str(year)+"-"+str(month)+"-01",date__lte=str(year)+"-"+str(month)+"-29")
                user_m = [0 for i in range(31)]
            elif (int(year) % 4 ==0) and (int(year) % 100 != 0):
                daterange = optimize_log.objects.filter(date__gte=str(year)+"-"+str(month)+"-01",date__lte=str(year)+"-"+str(month)+"-29")
                user_m = [0 for i in range(31)]
            else:
                daterange = optimize_log.objects.filter(date__gte=str(year)+"-"+str(month)+"-01",date__lte=str(year)+"-"+str(month)+"-28")
                user_m = [0 for i in range(30)]
        elif month == '4' or month == '6' or month == '9' or month == '11':
            daterange = optimize_log.objects.filter(date__gte=str(year)+"-"+str(month)+"-01",date__lte=str(year)+"-"+str(month)+"-30")
            user_m = [0 for i in range(32)]
        else:
            daterange = optimize_log.objects.filter(date__gte=str(year)+"-"+str(month)+"-01",date__lte=str(year)+"-"+str(month)+"-31")
            user_m = [0 for i in range(33)]
        monthrange = optimize_log.objects.filter(date__gte=str(year)+"-01-01",date__lte=str(year)+"-12-31")
        for i in daterange:
            da = str(i.date).split('-')
            user_m[int(da[2])] = i.user_count 
        user_y = [0 for i in range(13)]
        for i in monthrange:
            mo = str(i.date).split('-')
            user_y[int(mo[1])] += i.user_count
        user_y.append(0)
        data = {
            'admin' : admin,
            'userdetails' : userdetails,
            'day' : [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,0],
            'user_m' : user_m,
            'month' : [0,1,2,3,4,5,6,7,8,9,10,11,12,0],
            'user_y' : user_y,
            'y' : y,
            'm' : m,
            'yy' : int(year),
            'mm' : calendar.month_name[int(month)],
            'mmm' : int(month),
        }
    return render(request,'vstat.html',data)
    

#manage ingredients page
def manage_ingredients(request):
    if request.session.has_key('admin'):
        ingredient_data=ingredients.objects.all()
        data={
            'ingredient_data':ingredient_data,
            'admin' : admin,
            'userdetails' : userdetails,
        }
        return render(request,'manage_ingredients.html',data)
    else:
        messages.error(request,'Your last session has been deleted, please login!!')
        return redirect(home)

#delete ingredient
def i_delete(request,i_name):
    if request.method == 'POST':
        chkname = ingredients.objects.get(name=i_name)
        chkname.delete()
    return redirect(manage_ingredients)

#manage feed page
def manage_feed(request):
    if request.session.has_key('admin'):
        feed_data = feeds.objects.all()
        data={
            'feed_data':feed_data,
            'admin' : admin,
            'userdetails' : userdetails,
        }
        return render(request,'manage_feed.html',data)
    else:
        messages.error(request,'Your last session has been deleted, please login!!')
        return redirect(home)

#delete feed
def f_delete(request,f_name):
    if request.method == 'POST':
        chkname = feeds.objects.get(name=f_name)
        chkname.delete()
    return redirect(manage_feed)

#feed formulation page
def feed_formulation(request):
    feed_data = feeds.objects.all()
    n=[]
    if len(feed_data) != 0:
        for i in range(0,len(feed_data)):
            a=feed_data[i].id
            n.append(a)
        mis_id = []
        for ele in range(n[0], n[-1]+1):
            if ele not in n:
                mis_id.append(ele)
    else:
        mis_id=[1]
    mis_id.sort()
    if request.method == 'POST':
        if len(mis_id) == 0:
            f_id = len(n) + 1
        else:
            f_id = mis_id[0]
        f_name = request.POST['f_name']
        f_protein = request.POST['f_protein']
        f_energy = request.POST['f_energy']
        f_lysine = request.POST['f_lysine']
        f_methionine = request.POST['f_methionine']
        f_e_extract = request.POST['f_e_extract']
        f_c_fiber = request.POST['f_c_fiber']
        f_calcium = request.POST['f_calcium']
        f_phosphorus = request.POST['f_phosphorus']
        f_a_phosphorus = request.POST['f_a_phosphorus']
        f_phy_phosphorus = float(f_phosphorus) - float(f_a_phosphorus)
        f_salt = request.POST['f_salt']
        add_feed = feeds(id=f_id,name=f_name,protein=f_protein,energy=f_energy,lysine=f_lysine,methionine=f_methionine,e_extract=f_e_extract,c_fiber=f_c_fiber,calcium=f_calcium,phosphorus=f_phosphorus,a_phosphorus=f_a_phosphorus,pythic_phosphorus=f_phy_phosphorus,salt=f_salt)
        add_feed.save()
        return redirect(manage_feed)
    else:
        return redirect(manage_feed)

#add new ingredients
def add_ingredient(request):
    i_data = ingredients.objects.all()
    n=[]
    if len(i_data) != 0:
        for i in range(0,len(i_data)):
            a=i_data[i].id
            n.append(a)
        mis_id = []
        for ele in range(n[0], n[-1]+1):
            if ele not in n:
                mis_id.append(ele)
    else:
        mis_id=[1]
    mis_id.sort()
    if request.method == 'POST':
        if len(mis_id) == 0:
            i_id = len(n) + 1
        else:
            i_id = mis_id[0]
        i_name = request.POST['i_name']
        i_protein = request.POST['i_protein']
        i_energy = request.POST['i_energy']
        i_lysine = request.POST['i_lysine']
        i_methionine = request.POST['i_methionine']
        i_e_extract = request.POST['i_e_extract']
        i_c_fiber = request.POST['i_c_fiber']
        i_calcium = request.POST['i_calcium']
        i_phosphorus = request.POST['i_phosphorus']
        i_a_phosphorus = request.POST['i_a_phosphorus']
        i_phy_phosphorus = float(i_phosphorus) - float(i_a_phosphorus)
        i_salt = request.POST['i_salt']
        i_rate = request.POST['i_rate']
        add_ingredient = ingredients(id=i_id,name=i_name,protein=i_protein,energy=i_energy,lysine=i_lysine,methionine=i_methionine,e_extract=i_e_extract,c_fiber=i_c_fiber,calcium=i_calcium,phosphorus=i_phosphorus,a_phosphorus=i_a_phosphorus,pythic_phosphorus=i_phy_phosphorus,salt=i_salt,rate=i_rate)
        add_ingredient.save()
        return redirect(manage_ingredients)
    else:
        return redirect(manage_ingredients)

#cost optimize page
def calculation(request):
    ingredient_data=ingredients.objects.all()
    feed_data = feeds.objects.all()
    data={
        'ingredient_data':ingredient_data,
        'feed_data':feed_data,
        'admin' : admin,
        'userdetails' : userdetails,
    }
    return render(request,'calculation.html',data)


#edit feed data
def editfeed(request):
    if request.method == 'POST':
        f_id = request.POST['f_id']
        f_name = request.POST['f_name']
        f_protein = request.POST['f_protein']
        f_energy = request.POST['f_energy']
        f_lysine = request.POST['f_lysine']
        f_methionine = request.POST['f_methionine']
        f_e_extract = request.POST['f_e_extract']
        f_c_fiber = request.POST['f_c_fiber']
        f_calcium = request.POST['f_calcium']
        f_phosphorus = request.POST['f_phosphorus']
        f_a_phosphorus = request.POST['f_a_phosphorus']
        f_phy_phosphorus = request.POST['f_phy_phosphorus']
        f_salt = request.POST['f_salt']
        add_feed = feeds(id=f_id,name=f_name,protein=f_protein,energy=f_energy,lysine=f_lysine,methionine=f_methionine,e_extract=f_e_extract,c_fiber=f_c_fiber,calcium=f_calcium,phosphorus=f_phosphorus,a_phosphorus=f_a_phosphorus,pythic_phosphorus=f_phy_phosphorus,salt=f_salt)
        add_feed.save()
        return redirect(manage_feed)
    else:
        return redirect(manage_feed)


#edit ingredients
def editingredient(request):
    if request.method == 'POST':
        i_id = request.POST['i_id']
        i_name = request.POST['i_name']
        i_protein = request.POST['i_protein']
        i_energy = request.POST['i_energy']
        i_lysine = request.POST['i_lysine']
        i_methionine = request.POST['i_methionine']
        i_e_extract = request.POST['i_e_extract']
        i_c_fiber = request.POST['i_c_fiber']
        i_calcium = request.POST['i_calcium']
        i_phosphorus = request.POST['i_phosphorus']
        i_a_phosphorus = request.POST['i_a_phosphorus']
        i_phy_phosphorus = float(i_phosphorus) - float(i_a_phosphorus)
        i_salt = request.POST['i_salt']
        i_rate = request.POST['i_rate']
        add_ingredient = ingredients(id=i_id,name=i_name,protein=i_protein,energy=i_energy,lysine=i_lysine,methionine=i_methionine,e_extract=i_e_extract,c_fiber=i_c_fiber,calcium=i_calcium,phosphorus=i_phosphorus,a_phosphorus=i_a_phosphorus,pythic_phosphorus=i_phy_phosphorus,salt=i_salt,rate=i_rate)
        add_ingredient.save()
        return redirect(manage_ingredients)
    else:
        return redirect(manage_ingredients)


#pulp calculations
def optimize(request):
    #user counter
    d = datetime.now()
    date = d.strftime("%Y-%m-%d")
    try:
        u = optimize_log.objects.get(date=date)
        if str(u.date) == date:
            u.user_count += 1
            u.save()
        else:
            pass
    except:
        opti_count = optimize_log(date=date,user_count=1)
        opti_count.save()
    global qty_xls,feed_name,total
    qty_xls = []
    ingre_data = ingredients.objects.all()
    if request.method == 'POST':
        MIN_QTY = {}
        MAX_QTY = {}
        for i in ingre_data.values_list('name', flat=True):
            MIN_QTY[i] = request.POST.get('min'+i,0)
            MAX_QTY[i] = request.POST.get('max'+i,100)
        feed_name = request.POST['feed']

    for i in ingre_data.values_list('name', flat=True):
        if MIN_QTY[i] == '':
            MIN_QTY[i] = '0'
        if MAX_QTY[i] == '':
            MAX_QTY[i] = '100'
    
    feed_data = feeds.objects.get(name=feed_name)
    
    INGREDIENTS = list(ingre_data.values_list('name', flat=True))
    RATE = dict(zip(INGREDIENTS,ingre_data.values_list('rate', flat=True)))
    PROTEIN = dict(zip(INGREDIENTS,ingre_data.values_list('protein', flat=True)))
    ENERGY = dict(zip(INGREDIENTS,ingre_data.values_list('energy', flat=True)))
    LYSINE = dict(zip(INGREDIENTS,ingre_data.values_list('lysine', flat=True)))
    METHIONINE = dict(zip(INGREDIENTS,ingre_data.values_list('methionine', flat=True)))
    E_EXTRACT = dict(zip(INGREDIENTS,ingre_data.values_list('e_extract', flat=True)))
    C_FIBRE = dict(zip(INGREDIENTS,ingre_data.values_list('c_fiber', flat=True)))
    CALCIUM = dict(zip(INGREDIENTS,ingre_data.values_list('calcium', flat=True)))
    PHOSPHRUS = dict(zip(INGREDIENTS,ingre_data.values_list('phosphorus', flat=True)))
    A_PHOSPHRUS = dict(zip(INGREDIENTS,ingre_data.values_list('a_phosphorus', flat=True)))
    PHYTIC_PHOSPHRUS = dict(zip(INGREDIENTS,ingre_data.values_list('pythic_phosphorus', flat=True)))
    SALT = dict(zip(INGREDIENTS,ingre_data.values_list('salt', flat=True)))

    prob = LpProblem("LRS",LpMinimize)
    INGREDIENTS_VAR = LpVariable.dicts("INGREDIENTS",INGREDIENTS,lowBound=0,cat='Continuous')

    prob += lpSum([RATE[i]*INGREDIENTS_VAR[i] for i in INGREDIENTS])

    if request.method == 'POST':
        if request.POST.get('ed') == 'on':
            for i in INGREDIENTS:
                prob += INGREDIENTS_VAR[i] >= float(MIN_QTY[i])
                prob += INGREDIENTS_VAR[i] <= float(MAX_QTY[i])
    
    prob += lpSum([INGREDIENTS_VAR[i] for i in INGREDIENTS]) == 100

    prob += lpSum([PROTEIN[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.protein-((feed_data.protein*1)/100))*100
    prob += lpSum([PROTEIN[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.protein+((feed_data.protein*1)/100))*100

    prob += lpSum([ENERGY[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.energy - ((feed_data.energy*1)/100))*100
    prob += lpSum([ENERGY[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.energy + ((feed_data.energy*1)/100))*100

    prob += lpSum([LYSINE[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.lysine - ((feed_data.lysine*1)/100))*100
    prob += lpSum([LYSINE[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.lysine + ((feed_data.lysine*1)/100))*100

    prob += lpSum([METHIONINE[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.methionine - ((feed_data.methionine*1)/100))*100
    prob += lpSum([METHIONINE[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.methionine + ((feed_data.methionine*1)/100))*100

    prob += lpSum([E_EXTRACT[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.e_extract - ((feed_data.e_extract*1)/100))*100
    prob += lpSum([E_EXTRACT[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.e_extract + ((feed_data.e_extract*1)/100))*100

    prob += lpSum([C_FIBRE[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.c_fiber - ((feed_data.c_fiber*1)/100))*100
    prob += lpSum([C_FIBRE[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.c_fiber + ((feed_data.c_fiber*1)/100))*100

    prob += lpSum([CALCIUM[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.calcium - ((feed_data.calcium*1)/100))*100
    prob += lpSum([CALCIUM[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.calcium + ((feed_data.calcium*1)/100))*100

    # prob += lpSum([PHOSPHRUS[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.phosphorus - ((feed_data.phosphorus*1)/100))*100
    # prob += lpSum([PHOSPHRUS[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.phosphorus + ((feed_data.phosphorus*1)/100))*100

    prob += lpSum([A_PHOSPHRUS[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.a_phosphorus - ((feed_data.a_phosphorus*1)/100))*100
    prob += lpSum([A_PHOSPHRUS[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.a_phosphorus + ((feed_data.a_phosphorus*1)/100))*100

    # prob += lpSum([PHYTIC_PHOSPHRUS[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.pythic_phosphorus - ((feed_data.pythic_phosphorus*1)/100))*100
    # prob += lpSum([PHYTIC_PHOSPHRUS[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.pythic_phosphorus + ((feed_data.pythic_phosphorus*1)/100))*100

    prob += lpSum([SALT[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) >= (feed_data.salt - ((feed_data.salt*1)/100))*100
    prob += lpSum([SALT[i] * INGREDIENTS_VAR[i] for i in INGREDIENTS]) <= (feed_data.salt + ((feed_data.salt*1)/100))*100

    prob.solve()

    if LpStatus[prob.status] == 'Optimal':
        qty={}
        total = value(prob.objective)
        for i in INGREDIENTS:
            qty_xls.append(INGREDIENTS_VAR[i].value())
            if INGREDIENTS_VAR[i].value():
                qty[i] = {
                    'ing' : i,
                    'p_qty' : round(INGREDIENTS_VAR[i].value(),2),
                }
        pri_qty = {
            'qty' : qty,
            'feed_name' : feed_name,
            'total' : total,
        }
        return render(request,'optimize.html',pri_qty)
    else:
        messages.error(request,'The cost optimization process is not able to optimize the costs because you have not entered the correct quantities of ingredients')
    return redirect(calculation)


def export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="lrs_aau.xls"'

    wb = xlwt.Workbook(encoding='utf-8')

    #sheet 1
    ws = wb.add_sheet('Ingredients') 

    style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow; font: bold on, height 220; borders: left thin, right thin, top thin, bottom thin')
    columns = ['INGREDIENTS', 'PROTEIN', 'ENERGY', 'LYSINE', 'METHIONINE', 'E.EXTRACT', 'C.FIBRE', 'CALCIUM', 'PHOSPHORUS' ,'A.PHOSPHORUS' ,'PHYTIC PHOSPHORUS', 'SALT']

    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], style)
        if col_num == 0:
            ws.write(1, col_num, '', style)
            ws.col(col_num).width = 256 * 25
        elif col_num == 2:
            ws.write(1, col_num, 'KCAL/KG', style) 
            ws.col(col_num).width = 256 * 15
        else:
            ws.write(1, col_num, '%', style)
            ws.col(col_num).width = 256 * 15

    row_num = 1
    font_style = xlwt.XFStyle()
    font_style.font.height = 220
    font_style.borders.left = 1
    font_style.borders.right = 1
    font_style.borders.top = 1
    font_style.borders.bottom = 1

    rows = ingredients.objects.all().values_list('name', 'protein', 'energy', 'lysine', 'methionine', 'e_extract', 'c_fiber', 'calcium', 'phosphorus', 'a_phosphorus', 'pythic_phosphorus', 'salt')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    #sheet 2
    ws = wb.add_sheet('Calculation',cell_overwrite_ok = True)

    columns = ['INGREDIENTS', 'PROTEIN', 'ENERGY', 'LYSINE', 'METHIONINE', 'E.EXTRACT', 'C.FIBRE', 'CALCIUM', 'PHOSPHORUS' ,'A.PHOSPHORUS' ,'PHYTIC PHOSPHORUS', 'SALT']

    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], style)
        if col_num == 0:
            ws.write(1, col_num, '', style)
            ws.col(col_num).width = 256 * 25
        elif col_num == 2:
            ws.write(1, col_num, 'KCAL/KG', style) 
            ws.col(col_num).width = 256 * 15
        else:
            ws.write(1, col_num, '%', style)
            ws.col(col_num).width = 256 * 15

    calcu = []
    row_num = 1
    for row in rows:
        row_num += 1
        calcu.append([])
        for col_num in range(len(row)):
            if col_num != 0:
                ws.write(row_num, col_num, float(row[col_num])*float(qty_xls[row_num-2]), font_style)
                calcu[row_num-2].append(float(row[col_num])*float(qty_xls[row_num-2]))
            else:
                ws.write(row_num, col_num,row[col_num], font_style)
    
    style1 = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue; font: colour white, bold on, height 220; borders: left thin, right thin, top thin, bottom thin')
    
    total_calcu = np.array(calcu)
    final_total  = total_calcu.sum(axis=0)
    row_num +=1
    for i in range(len(final_total)):
        if i == 0:
            ws.write(row_num, i, 'TOTAL', style1) 
            ws.write(row_num, i+1, final_total[i]/100, style1) 
        else:
            ws.write(row_num, i+1, final_total[i]/100, style1)

    
    #sheet 3
    ws = wb.add_sheet('FINAl OutPut',cell_overwrite_ok = True)

    columns = ['INGREDIENTS', 'QTY', 'RATE', 'VALUE', '', '', 'FINAL ANALYSIS']
    columns.append(feed_name)

    for col_num in range(len(columns)):
        if columns[col_num] == '':
            ws.write(0, col_num, columns[col_num])
            ws.write(1, col_num, '')
            ws.write(2, col_num, '')
        else:
            ws.write(0, col_num, columns[col_num], style)
            if columns[col_num] == 'QTY':
                ws.write(1, col_num, '(KG)', style)
                ws.col(col_num).width = 256 * 15
            elif columns[col_num] == 'RATE':
                ws.write(1, col_num, '(Rs/Kg)', style)
                ws.col(col_num).width = 256 * 15
            elif columns[col_num] == 'VALUE':
                ws.write(1, col_num, '', style)
                ws.col(col_num).width = 256 * 15
            else:
                ws.write(1, col_num, '', style)
                ws.col(col_num).width = 256 * 25
            ws.write(2, col_num, '', style)
        

    row_num = 2
    rows = ingredients.objects.all().values_list('name', 'protein', 'rate', 'energy')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 0 or col_num == 2:
                ws.write(row_num, col_num,row[col_num], font_style)
            elif col_num == 1:
                ws.write(row_num, col_num,round(qty_xls[row_num-3],2), font_style)
            else:
                ws.write(row_num, col_num,round((row[col_num-1]*qty_xls[row_num-3]),2), font_style)

    row_num +=1
    for i in range(3):
        if i == 0:
            ws.write(row_num, i, 'TOTAL', style1) 
            ws.write(row_num, i+1, round(sum(qty_xls),2), style1) 
        elif i == 1:
            ws.write(row_num, i+1, '', style1)
        else:
            ws.write(row_num, i+1, round(total,2), style1)

    columns = ['PROTEIN(%)', 'ENERGY(Kcal)', 'LYSINE(%)', 'METHIONINE(%)', 'E.EXTRACT(%)', 'C.FIBRE(%)', 'CALCIUM(%)', 'PHOSPHORUS(%)' ,'A.PHOSPHORUS(%)' ,'PHYTIC PHOSPHORUS(%)', 'SALT(%)']
    row_num = 3
    for col_num in range(len(columns)):
        ws.write(row_num, 6, columns[col_num], font_style)
        row_num+=2
    
    row_num = 3
    for i in range(len(final_total)):
        ws.write(row_num, 7, round(final_total[i]/100,2), font_style)
        row_num+=2


    wb.save(response)
    return response

#optimize log dummmy data
def optidummy(request):
    import datetime
    import random
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.now()
    delta = timedelta(days=1)
    while start_date <= end_date:
        date = start_date.strftime("%Y-%m-%d")
        start_date += delta
        opti_count = optimize_log(date=date,user_count=random.randint(10, 35))
        opti_count.save()
    return redirect(home)
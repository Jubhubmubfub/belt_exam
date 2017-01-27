from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote, Favorite


# year range
year_range = []
for i in range(2017,1900,-1):
    year_range.append(i)

# Create your views here.
# =========================================================
#               LOGIN AND REGISTRATION
# =========================================================
def index(request):
    context = {
        'year_range':year_range
    }
    return render(request, 'belt/index.html',context)

def register(request):
    result = User.objects.validateReg(request)
    if result[0]==False:
        print_messages(request, result[1])
        return redirect('/')
    return log_user_in(request,result[1])

def login(request):
    result = User.objects.validateLogin(request)
    if result[0]==False:
        print_messages(request, result[1])
        return redirect('/')
    return log_user_in(request,result[1])

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.INFO, message)

def log_user_in(request,user):
    request.session['user'] = {
            'id':user.id,
            'first_name':user.first_name,
            'alias':user.alias,
            'email':user.email,
    }
    messages.add_message(request, messages.INFO, "successfully logged in! VALID EMAIL {}".format(request.POST['email']))
    return redirect('/success')

def logout(request):
    request.session.pop('user')
    return redirect('/')

# =========================================================
#               QUOTES HOME PAGE
# =========================================================

def success(request):
    user = User.objects.get(id=request.session['user']['id'])
    # check if user is logged in
    if 'user' not in request.session:
        return redirect('/')

    # print to terminal all existing objects
    print "ALL QUOTE OBJECTS",Quote.objects.all()
    print "ALL FAVORITE OBJECTS",Favorite.objects.all()
    print "ALL USER OBJECTS",User.objects.all()

    # gather all quotes *that are not in the user's favorite list*
    quotes = Quote.objects.all()

    # gather all favorites for specific user
    favorites_list = Favorite.objects.filter(user_id=request.session['user']['id'])

    # get the quote objects and put them in a list
    favorited_quotes = []
    for favorite in favorites_list:
        favorited_quotes.append(favorite.quote)

    # gather all quotes and put them in a list
    quotes_list = Quote.objects.all()
    print "THIS IS CURRENTLY THE QUOTES LIST",quotes_list
    #going to populate this list with quotes if they are not in the favorites list
    unfavorited_quotes = []
    for quote in quotes_list:
        if quote not in favorited_quotes:
            unfavorited_quotes.append(quote)

    # pass context to page
    context = {
        'quotes':unfavorited_quotes,
        'favorites':favorites_list
    }
    return render(request, 'belt/success.html',context)

def contribute_quote(request,user_id):
    result = Quote.objects.validate_inputs(request)
    if result[0]==False:
        for error in result[1]:
            messages.add_message(request,messages.INFO,error)
            return redirect('/success')
    else:
        user = User.objects.get(id=user_id)
        Quote.objects.create(quote=request.POST['quote'],quoted_by=request.POST['quoted_by'], user=user)
        return redirect('/success')

    # =========================================================
    #               DEALING WITH FAVORITES
    # =========================================================


def add_to_favorites(request,quote_id):
    # get user object
    user = User.objects.get(id=request.session['user']['id'])

    # get quote object
    quote = Quote.objects.get(id=quote_id)
    # maybe do a check to see if the favorite quote already exists
    # create favorite with user and quote objects
    Favorite.objects.create(quote=quote,user=user)
    return redirect('/success')

def remove_from_favorites(request,favorite_id):
    # remove favorite with user and quote objects
    Favorite.objects.get(id=favorite_id).delete()
    return redirect('/success')



# =========================================================
#               USER PAGE
# =========================================================

def user(request,user_id):
    # check if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    # get user object
    user = User.objects.get(id=user_id)
    # get user quotes
    quote_list = Quote.objects.filter(user_id=user_id)
    # pass context to page
    count = len(quote_list)
    context = {
        'user':user,
        'quote_list':quote_list,
        'count':count
    }
    return render(request, 'belt/user.html',context)

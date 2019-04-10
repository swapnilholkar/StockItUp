from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.http import Http404

# for user registration
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, StockQuestionForm, FeedbackForm
from .forms import UserRegisterForm, UserUpdateForm, StockQuestionForm

#for csv upload/write/read
import csv, io
from csv import writer
from django.contrib import messages
from django.contrib.auth.decorators import permission_required,login_required

import json

#import database tables
from .models import Question,StockDetail,Response
from django.db.models import Count


# api for getting finance stock data 
# import datetime
from datetime import datetime,date,time,timedelta
from iexfinance.stocks import get_historical_data
import os


# using plotly for creating charts in python
import plotly
plotly.__version__
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
from plotly.offline import plot

import numpy as np
import pandas as pd

# for web scraping
import requests
from bs4 import BeautifulSoup

# for twitter
from twitterscraper import query_tweets
# for twitter Sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# import cv2
# from PIL import Image 




# user registration 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Your account is now created for { username }, please log in')
            return redirect('Stocks:login') 

    else:
        form =UserRegisterForm()

    return render(request,'Stocks/register.html', {'form': form})



def feedback(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        feedback_form = FeedbackForm(request.POST)
        # check whether it's valid:
        if feedback_form.is_valid():

            # ease_of_use = feedback_form.cleaned_data['ease_of_use']
            # stat_info = feedback_form.cleaned_data['stat_info']
            # experience = feedback_form.cleaned_data['experience']
            # like = feedback_form.cleaned_data['like']
            # not_like = feedback_form.cleaned_data['not_like']
            
            feedback_form.save()
            messages.success(request, f'Thank you for your feedback!')
            return redirect('Stocks:feedback') 
    else:
        feedback_form =FeedbackForm()

    context = {
        'feedback_form': feedback_form
    }
    return render(request,'Stocks/feedback.html', context)



@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form= UserUpdateForm(request.POST,instance = request.user) 
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, f'You have updated your details')
            return redirect('Stocks:profile') 
    else:
        user_update_form= UserUpdateForm(instance = request.user) 

    context ={
        'user_update_form' : user_update_form
    }
    return render(request,'Stocks/profile.html',context)


#home page

def index(request):
    # for getting stock data

    # print('executing this function')
    # get_stock_data_iex()
    # print('done executing this function')


    # get_yahoo_target_prices()
    # get_nasdaqSite_target_prices()
    # get_stocktargetadvisior_target_prices()

    # get_twitter_tweets()

    return render(request, 'Stocks/index.html')


@login_required
def selectStock(request):
    stock_list = StockDetail.objects.all()
    user=request.user
    favourite_stocks = user.favourite.all()

    print(favourite_stocks)

    for ele in favourite_stocks:
        print(ele.stock_symbol)

    top_responses = StockDetail.objects.annotate(num_response= Count('response')/2).order_by('-num_response')[:5]
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'stock_list': stock_list,'top_responses':top_responses,'favourite_stocks':favourite_stocks}

    return render(request, 'Stocks/selectStock.html', context)

#for response
def stocks(request,stock_id):
    stock = get_object_or_404(StockDetail, pk=stock_id)
    question_list = Question.objects.all()

    stock_question_form = StockQuestionForm(instance = request.user)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        stock_question_form = StockQuestionForm(request.POST,instance = request.user)
        # check whether it's valid:
        if stock_question_form.is_valid():
            bullish_bearish = stock_question_form.cleaned_data['bullish_bearish']
            target_price = stock_question_form.cleaned_data['target_price']

            question1 = Question.objects.get(id=5)
            question2 = Question.objects.get(id=6)
            stock = StockDetail.objects.get(id=stock_id)
            user = request.user
            try:
                response_q1 = Response.objects.get(stock = stock, question=question1, user=request.user)
                response_q2 = Response.objects.get(stock = stock, question=question2, user=request.user)
                print("has found an existing object and should update")
              
                response_q1.response_text = bullish_bearish
                response_q1.save()
                response_q2.response_text = target_price
                response_q2.save()
                return redirect('Stocks:results',stock_id) 
                
            except Response.DoesNotExist:
                print("no existing object, creating a new one")
                response_q1 = Response(user = user, question = question1, stock = stock,response_text = bullish_bearish).save()
                response_q2 = Response(user = user, question = question2, stock = stock,response_text = target_price).save()
                return redirect('Stocks:results',stock_id)          
    else:
        stock_question_form = StockQuestionForm(instance = request.user)

    df = pd.read_csv('stock_data/{}.csv'.format(stock.stock_symbol))
    historical_trace = go.Scatter(x = df['date'], y = df['close'],
        name='Close Share Prices (in USD)')

    data=[historical_trace]
    
    layout = go.Layout(title='{} Close Share Prices 2017-18'.format(stock),
                    autosize=True,
                    plot_bgcolor='rgb(230, 230,230)', 
                    showlegend=True)

    config = {'scrollZoom': True,'displaylogo': False,'responsive':True}

    fig = go.Figure(data=data, layout=layout)
    historical_chart_div = plot(fig, output_type='div', include_plotlyjs=False,config=config)

    # print(question_list)
    context = {'question_list': question_list,'stock': stock,'historical_chart_div':historical_chart_div, 'StockQuestionForm': stock_question_form}

    return render(request, 'Stocks/Stocks.html', context)
    
    
    

# def stock_question_submission(request):
#     # if 'loggedin' in request.session:

#     try:

#         questionArray = request.POST.getlist('questionArray[]')
#         answerArray = request.POST.getlist('answerArray[]')
#         stockId = request.POST['stockId']
        
#         print("stockId of this stock is:" + stockId)
#         print(questionArray)
#         print(answerArray)

#         for index in range(0, len(questionArray)):
#             print("\n"+questionArray[index] + ": " + answerArray[index])

#         print(questionArray[0])

#         # Response.objects.update_or_create()

#         # this is where is the issue is:
#         print("creating the database object")
#         for value in range(0,len(questionArray)):
#             print("inside the for loop"+str(value))
#             question_id = int(float(questionArray[value]))
#             question = Question.objects.get(id=question_id)
#             stock = StockDetail.objects.get(id=stockId)
#             user = request.user
#             try:
#                 response = Response.objects.get(stock = stock, question=question, user=request.user)
#                 print("has found an existing object and should update")
#                 print(questionArray[value])
                
#                 response.response_text = answerArray[value]
#                 response.save()

#             except Response.DoesNotExist:
#                 print("no existing object, creating a new one")
#                 print(questionArray[value])
#                 response = Response(
#                     user = user,
#                     question = question,
#                     stock = stock,
#                     response_text = answerArray[value]
#                 )
#                 response.save()



            
#             # Response.objects.filter(question=some_question)

#         # return redirect('Stocks:results', stockId) 
#         # return results(request, stockId)
#         responseurl = {
#             'redirectUrl': stockId+"/results"
#         }
#         return HttpResponse(json.dumps(responseurl), content_type='application/json')
#         # return HttpResponse("status=201")
#     except Exception as ex:
#         print(ex)
#         return HttpResponse(status=500)


# selecting a favourite stock

def makeFavourite(request,stock_id):
    fav_stock = get_object_or_404(StockDetail,id=stock_id)
    if fav_stock.favourite.filter(id=request.user.id).exists():
        fav_stock.favourite.remove(request.user)
    else:
        fav_stock.favourite.add(request.user)
    
    return redirect('Stocks:results', stock_id) 
    

@login_required
def results(request,stock_id):
    
    stockname = get_object_or_404(StockDetail, pk=stock_id)
    print(stockname.stock_symbol)

    # is the stock a favourite or not
    is_fav = False

    if stockname.favourite.filter(id=request.user.id).exists():
        is_fav = True

    #counts the num of responses
    stockq1 = Response.objects.filter(stock=stock_id,question=5)
    stockq1Response = Response.objects.filter(stock=stock_id,question=5).count() 

    stockq2 = Response.objects.filter(stock=stock_id,question=6)
    stockq2Response = Response.objects.filter(stock=stock_id,question=6).count()

    stockq1UserResponse = Response.objects.filter(stock=stock_id,question=5,user=request.user)
    stockq2UserResponse = Response.objects.filter(stock=stock_id,question=6,user=request.user)
    q2userresponseInt = 0  

    # getting the target price response value
    for res in stockq2UserResponse:
        q2userresponseInt = float(res.response_text)
    print("printing the users answers")
    print(stockq1UserResponse)
    print(stockq2UserResponse)
    print(q2userresponseInt)


    # bullish/bearish pie chart
    bull_count = Response.objects.filter(stock=stock_id,question=5, response_text="Bullish").count()
    bear_count = Response.objects.filter(stock=stock_id,question=5, response_text="Bearish").count()

    labels = ['Bullish','Bearish'] 
    values = [bull_count,bear_count]
    chart_trace = go.Pie(labels=labels, values=values)
    layout = go.Layout(
        title='Bullish vs Bearish - User Sentiment',
    )
    config = {'displaylogo': False}
    bull_bear_pie_chart = go.Figure(data=[chart_trace],layout=layout)
    bull_bear_pie_chart_div = plot(bull_bear_pie_chart, output_type='div', include_plotlyjs=False,config=config)

    # Target price bar chart 
    sum_tp =0
    avg_tp=0
    if stockq2.exists():
        for tp in stockq2:
            print(sum_tp)
            sum_tp+= float(tp.response_text)
            
        
        avg_tp = sum_tp/stockq2Response
        print(avg_tp)
    else:
        avg_tp=sum_tp


    bar_trace = go.Bar(
    x=['All User Avg Target Price', 'Your Target Price'],
    y=[avg_tp, q2userresponseInt],
    text=[f'Avg taken from a total of { stockq2Response } responses', 'The targe price you entered'],
    marker=dict(
        color='rgb(0,0,128)',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5,
        )
    ),
        opacity=1
    )

    data = [bar_trace]
    layout = go.Layout(
        title='Avg Target Price Compared vs Your Target Price ',
    )
    config = {'displaylogo': False}

    target_price_bar = go.Figure(data=data, layout=layout)
    target_price_bar_div = plot(target_price_bar, output_type='div', include_plotlyjs=False,config=config)


    # importing the different csv files
    df = pd.read_csv('stock_data/{}.csv'.format(stockname.stock_symbol)) #for historical 
    tdf = pd.read_csv('twitter_tweets/{}.csv'.format(stockname.stock_symbol)) #for twitter sentiment
    yahoo_tp= pd.read_csv('yahoo_target_prices/{}.csv'.format(stockname.stock_symbol))
    nasdaq_com_tp = pd.read_csv('nasdaq.com_target_prices/{}.csv'.format(stockname.stock_symbol))
    stocktargetadvisor_tp = pd.read_csv('stocktargetadvisor_target_prices/{}.csv'.format(stockname.stock_symbol))

    # Main chart with historical data

    historical_trace = go.Scatter(x = df['date'], y = df['close'],
        name='Close Share Prices (in USD)')

    # getting the date in a year from now
    futureDate =datetime.now() + timedelta(days=365)

    external_price_yahoo = go.Scatter(x = [futureDate], y= yahoo_tp['TargetPrice'],
        name= "Yahoo Target Price (1Y Target)",
        line = dict(color = '#17BECF'),
        opacity = 0.8)
    
    external_price_nasdaq_com = go.Scatter(x = [futureDate], y= nasdaq_com_tp['TargetPrice'],
        name= "Nasdaq.com Target Price (1Y Target)",
        line = dict(color = '#ff9900'),
        opacity = 0.8)
    
    external_price_stocktargetadvisor = go.Scatter(x = [futureDate], y= stocktargetadvisor_tp['TargetPrice'],
        name= "Stock Target Advisor Target Price (1Y Target)",
        line = dict(color = '#00ff00'),
        opacity = 0.8)

    avg_user_price = go.Scatter(x = [datetime.now()], y= [avg_tp],
        name= "Avg Price From {} User(s)".format(stockq2Response),
        line = dict(color = '#FF2626'),
        opacity = 0.8)

    your_price = go.Scatter(x = [datetime.now()], y= [q2userresponseInt],
        name= "Your Target Price".format(stockq2Response),
        line = dict(color = '#8F39FF'),
        opacity = 0.8)


    data=[historical_trace, external_price_yahoo, external_price_nasdaq_com, external_price_stocktargetadvisor, avg_user_price,your_price]
    
    layout = go.Layout(title='{} Close Share Prices 2017-18'.format(stockname),
                    autosize=True,
                    plot_bgcolor='rgb(230, 230,230)', 
                    showlegend=True)

    config = {'scrollZoom': True,'displaylogo': False,'responsive':True}

    fig = go.Figure(data=data, layout=layout)
    historical_chart_div = plot(fig, output_type='div', include_plotlyjs=False,config=config)
    
    # twitter sentiment analsyis + graph 
    pos_sentence_count=0
    neg_sentence_count=0
    nuet_sentence_count=0
    count_of_tweets=0
    # santise the tweet before passing it to the analsyis

    analyzer = SentimentIntensityAnalyzer()
    for sentence in tdf['Tweet']:
        # print(sentence, type(sentence))
        vs = analyzer.polarity_scores(str(sentence))
        if vs['compound'] > 0:
            pos_sentence_count+=1
        elif vs['compound'] < 0:
            neg_sentence_count+=1
        else:
            nuet_sentence_count+=1
        count_of_tweets+=1
    
    if count_of_tweets == 0:
        pos_sentence_count_percent = 0
        neg_sentence_count_percent = 0
        nuet_sentence_count_percent = 0
    else:
        pos_sentence_count_percent = pos_sentence_count/count_of_tweets*100
        neg_sentence_count_percent = neg_sentence_count/count_of_tweets*100
        neut_sentence_count_percent = nuet_sentence_count/count_of_tweets*100
    # pie chart for showing twitter sentiment

    labels = ['Bullish','Bearish','Neutral'] 
    values = [pos_sentence_count_percent,neg_sentence_count_percent,neut_sentence_count_percent]
    chart_trace = go.Pie(labels=labels, values=values)
    layout = go.Layout(
        title='Bullish vs Bearish - Twitter Sentiment',
    )
    config = {'displaylogo': False}
    bull_bear_pie_chart = go.Figure(data=[chart_trace],layout=layout)
    twitter_pie_chart_div = plot(bull_bear_pie_chart, output_type='div', include_plotlyjs=False,config=config)


    # print("pos is : {} negative is : {} and total number of tweets : {} and nut {}".format(pos_sentence_count,neg_sentence_count,count_of_tweets, nut_sentence_count))
    # print("pos as % : {} negative as % : {} and total number of tweets : {}".format(pos_sentence_count/count_of_tweets*100, neg_sentence_count/count_of_tweets*100, count_of_tweets))
    # print('pos {} and neg {}'.format(pos_sentence_count_percent,neg_sentence_count_percent))
    
    context ={'stockq1': stockq1,'stockq2':stockq2, 'stockname':stockname,
    'plot':historical_chart_div,
    'bull_bear_pie_chart_div':bull_bear_pie_chart_div,
    'target_price_bar_div':target_price_bar_div,
    'stockq1Response':stockq1Response,
    'stockq2Response':stockq2Response,
    'stockq1UserResponse':stockq1UserResponse,
    'stockq2UserResponse':stockq2UserResponse,
    'twitter_pie_chart_div':twitter_pie_chart_div,
    'is_fav':is_fav,
    }
    return render(request, 'Stocks/result.html',context)



# method that gets the stock data and target prices using the api, will need it for updating the data
def get_stock_data_iex():
    print('currently in the get_stock function')
    stockTicker = StockDetail.objects.all()

    start = datetime(2017, 1, 1)
    end = datetime.now()
    for ticker in stockTicker:
        print('inside the loop creating the files:')
        print(ticker)

        if not os.path.exists('stock_data/{}.csv'.format(ticker.stock_symbol)):
            df = get_historical_data(ticker.stock_symbol, start, end, output_format='pandas')
            df.to_csv('stock_data/{}.csv'.format(ticker.stock_symbol))
        else:
            print('Already have {}'.format(ticker.stock_symbol))
            df = get_historical_data(ticker.stock_symbol, start, end, output_format='pandas')
            df.to_csv('stock_data/{}.csv'.format(ticker.stock_symbol))
    
    print("all done")


def get_yahoo_target_prices():
    stockTicker = StockDetail.objects.all()

    for ticker in stockTicker:
        response = requests.get('https://uk.finance.yahoo.com/quote/{}'.format(ticker.stock_symbol))
        soup = BeautifulSoup(response.text,'html.parser')
        spanTags = soup.findAll('span',{'class':'Trsdu(0.3s)'})
        span = spanTags[-1].get_text()


        with open('yahoo_target_prices/{}.csv'.format(ticker.stock_symbol),'w') as f:
            csv_writer = writer(f)
            headers = ['TargetPrice']
            csv_writer.writerow(headers)
            csv_writer.writerow([span])
    print("all done")
            

def get_nasdaqSite_target_prices():
    count=0
    stockTicker = StockDetail.objects.all()
    for ticker in stockTicker:
        if ticker.stock_symbol=='LBTYK':
            continue
        else:
            response = requests.get('https://www.nasdaq.com/symbol/{}/analyst-research'.format(ticker.stock_symbol))
            soup = BeautifulSoup(response.text,'html.parser')
            tdTags = soup.findAll('td')
            tag = tdTags[5].get_text()
            tagSplit=tag.split()
            tp = tagSplit[1]

            with open('nasdaq.com_target_prices/{}.csv'.format(ticker.stock_symbol),'w') as f:
                csv_writer = writer(f)
                headers = ['TargetPrice']
                csv_writer.writerow(headers)
                csv_writer.writerow([tp])
                count+=1
                print(count)
    print("all done")


def get_stocktargetadvisior_target_prices():
    count=0
    stockTicker = StockDetail.objects.all()
    print(stockTicker[count])
    try:
        for ticker in stockTicker:
            if ticker.stock_symbol=='LBTYK' or ticker.stock_symbol=='FOX':
                continue
            else:
                response = requests.get('https://www.stocktargetadvisor.com/stock/USA/NSD/{}'.format(ticker.stock_symbol))
                soup = BeautifulSoup(response.text,'html.parser')
                spanTags = soup.findAll('span')
                tag = spanTags[26].get_text()
                tagSplit=tag.split()
                tp = tagSplit[1]

                with open('stocktargetadvisor_target_prices/{}.csv'.format(ticker.stock_symbol),'w') as f:
                    csv_writer = writer(f)
                    headers = ['TargetPrice']
                    csv_writer.writerow(headers)
                    csv_writer.writerow([tp])
                    count+=1
                    print(count)
        print("all done")
    except:
        print(stockTicker[count])

def get_twitter_tweets():

    # this will query tweets from yesterday to today's date
    count=0
    stockTicker = StockDetail.objects.all()
    Previous_Date = date.today() - timedelta(days=1)

    for ticker in stockTicker:
        with open('twitter_tweets/{}.csv'.format(ticker.stock_symbol),'w') as f:
            csv_writer = writer(f)
            headers = ['Tweet']
            csv_writer.writerow(headers)
            count+=1
            
            for tweet in query_tweets("${}".format(ticker.stock_symbol),20, Previous_Date):
                csv_writer.writerow([tweet.text])
        print(count)
       
    print("all done")


#for csv upload
@permission_required('admin.can_add_log_entry')

def stock_upload(request):  
    template = "stock_upload.html"
    
    prompt ={
        'order':'Order of csv should be stock symbol, name, targetPrice'
    }
    
    if request.method == "GET":
        return render(request, template,prompt)
    
    csv_file = request.FILES['file']
    
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Not a csv file')
        
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = StockDetail.objects.update_or_create(
            stock_symbol = column[0],
            company_name = column[1],
            target_price = column[2]
        )
        
    context ={}
    return render(request,template,context)

    
    
    
    
    
    
# forms

# from django.http import HttpResponseRedirect
# from django.shortcuts import render

# from .forms import NameForm

# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             price = form.cleaned_data['price']
#             name = form.cleaned_data['name']

#             Stock1(name=name, price=price, response_text=...).save()
#             Stock2(name=name, price=2*price, resopnse_text=....).save()


#             return HttpResponseRedirect('/thanks/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, 'name.html', {'form': form})

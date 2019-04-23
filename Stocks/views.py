# Code for rendering the charts adapted from Author: Plotly Technologies Inc. Title: Collaborative data science Publisher: Plotly Technologies Inc. Place of publication: Montréal, QC Date of publication: 2015 URL: https://plot.ly/python/
# code for twitter analyse adapted from Author: C.J. Hutto, Published on 19 Dec 2018, Availability: https://github.com/cjhutto/vaderSentiment 
# Code for login,logout,profile,register adapted from Author: Corey Schafer, Published on Aug 2018, Availability: https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p 

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

#import database tabless
from .models import Question,StockDetail,Response
from django.db.models import Count


# api for getting finance stock data 
# import datetime
from datetime import datetime,date,time,timedelta
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

# for twitter Sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



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


# function for feedback form 

def feedback(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        feedback_form = FeedbackForm(request.POST)
        # check whether it's valid:
        if feedback_form.is_valid():
            feedback_form.save()
            messages.success(request, f'Thank you for your feedback!')
            return redirect('Stocks:feedback') 
    else:
        feedback_form =FeedbackForm()
    context = {
        'feedback_form': feedback_form
    }
    return render(request,'Stocks/feedback.html', context)


# function for making changes to profile

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


#home page and for running the functions when needed

def index(request):
    return render(request, 'Stocks/index.html')


# stock selection page

@login_required
def selectStock(request):
    stock_list = StockDetail.objects.all()
    user=request.user
    favourite_stocks = user.favourite.all()
    top_responses = StockDetail.objects.annotate(num_response= Count('response')/2).order_by('-num_response')[:5]
    context = {'stock_list': stock_list,'top_responses':top_responses,'favourite_stocks':favourite_stocks}

    return render(request, 'Stocks/selectStock.html', context)

#question and response page

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
                # has found an existing object and should update
              
                response_q1.response_text = bullish_bearish
                response_q1.save()
                response_q2.response_text = target_price
                response_q2.save()
                return redirect('Stocks:results',stock_id) 
                
            except Response.DoesNotExist:
                # no existing object, creating a new one
                response_q1 = Response(user = user, question = question1, stock = stock,response_text = bullish_bearish).save()
                response_q2 = Response(user = user, question = question2, stock = stock,response_text = target_price).save()
                return redirect('Stocks:results',stock_id)          
    else:
        stock_question_form = StockQuestionForm(instance = request.user)

    # show historical chart---------->

    df = pd.read_csv('stock_data/{}.csv'.format(stock.stock_symbol))
    historical_trace = go.Scatter(x = df['date'], y = df['close'],
        name='Close Share Prices (in USD)')

    data=[historical_trace] 
    layout = go.Layout(title='{} Close Share Prices 2017-19'.format(stock),
                    autosize=True,
                    plot_bgcolor='rgb(230, 230,230)', 
                    showlegend=True)

    config = {'scrollZoom': True,'displaylogo': False,'responsive':True}
    fig = go.Figure(data=data, layout=layout)
    historical_chart_div = plot(fig, output_type='div', include_plotlyjs=False,config=config)

    context = {'question_list': question_list,'stock': stock,'historical_chart_div':historical_chart_div, 'StockQuestionForm': stock_question_form}

    return render(request, 'Stocks/Stocks.html', context)
    

# selecting a favourite stock

def makeFavourite(request,stock_id):
    fav_stock = get_object_or_404(StockDetail,id=stock_id)
    if fav_stock.favourite.filter(id=request.user.id).exists():
        fav_stock.favourite.remove(request.user)
    else:
        fav_stock.favourite.add(request.user)
    
    return redirect('Stocks:results', stock_id) 
    
# shows all the statistical charts on results page

@login_required
def results(request,stock_id):
    
    stockname = get_object_or_404(StockDetail, pk=stock_id)
    # is the stock a favourite or not
    is_fav = False
    if stockname.favourite.filter(id=request.user.id).exists():
        is_fav = True

    #counts the num of responses
    stockq1 = Response.objects.filter(stock=stock_id,question=5)
    stockq1Response = Response.objects.filter(stock=stock_id,question=5).count() 
    stockq2 = Response.objects.filter(stock=stock_id,question=6)
    stockq2Response = Response.objects.filter(stock=stock_id,question=6).count()

    # get the user response to the questions
    stockq1UserResponse = Response.objects.filter(stock=stock_id,question=5,user=request.user)
    stockq2UserResponse = Response.objects.filter(stock=stock_id,question=6,user=request.user)
    q2userresponseInt = 0  

    # getting the target price response value
    for res in stockq2UserResponse:
        q2userresponseInt = float(res.response_text)
   
    # bullish/bearish pie chart ------->
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


    # Target price bar chart calculating the average ------->
    sum_tp =0
    avg_tp=0
    if stockq2.exists():
        for tp in stockq2:
            sum_tp+= float(tp.response_text)
        avg_tp = sum_tp/stockq2Response
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
    # for target prices
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
    
    layout = go.Layout(title='{} Close Share Prices 2017-19'.format(stockname),
                    autosize=True,
                    plot_bgcolor='rgb(230, 230,230)', 
                    showlegend=True)

    config = {'scrollZoom': True,'displaylogo': False,'responsive':True}

    fig = go.Figure(data=data, layout=layout)
    historical_chart_div = plot(fig, output_type='div', include_plotlyjs=False,config=config)
    
    # twitter sentiment analysis + graph 
    pos_sentence_count=0
    neg_sentence_count=0
    nuet_sentence_count=0
    count_of_tweets=0
    # santise the tweet before passing it to the analysis

    analyzer = SentimentIntensityAnalyzer()
    for sentence in tdf['Tweet']:
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
        neut_sentence_count_percent = 0
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

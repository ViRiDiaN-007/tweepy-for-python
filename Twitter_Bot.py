import tweepy
import requests
import re


##Get OAuth tokens from file. This is needed to authenticate the user
with open('auth.txt','r')as authFile:
    tokens=authFile.readlines()
    tokens= [token.strip('\n') for token in tokens]
    tokens=[token.split('=')[1]for token in tokens]
    consumer_key,consumer_secret,access_key,access_secret=tokens[0],tokens[1],tokens[2],tokens[3]
try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key,access_secret)
    api=tweepy.API(auth)
except Exception as e:
    print(f'Error: {e}')




##Options
def Send_Tweet():
    confirm=False
    tweet=input('\nWhat would you like to tweet?: ')
    while not confirm:
        confirmation=input(f'Are you sure you want to tweet\n"{tweet}"? [Y/N]: ')
        if confirmation.lower()=='y':
            confirm=True
        else:
            tweet=input('What would you like to tweet?: ')
    print('Sending Tweet!')
    try:
        api.update_status(tweet)
        print('Tweet Sent!')
    except Exception as e:
        print(f'Error: {e}')


##OPTIONS
def Show_Menu():
    print()
    print('[1] Post A Tweet')
    print('[2] Print Home Feed')
    print('[3] Send A Direct Message')
    print('[4] Follow/Unfollow A User')

def Print_Timeline():
    homePage=api.home_timeline()
    for tweet in homePage:
        print(tweet.text)
        print()
        

def Send_DM():
    try:
        screenName=input('Who Would You Like To Message? ')
        screenName=screenName.strip('@')
        user=api.get_user(screen_name = screenName)
        message=input('Enter Your Message: ')
        confirmed=False
        while not confirmed:
            confirmation=input(f'Are you sure you want to message\n"{message}" to {screenName}? [Y/N]: ')
            if confirmation.lower()=='y':
                confirmed=True
            else:
                choice=input('What would you like to change?\n[1] The User\n[2] The Message\n ')
                while True:
                    if choice=='1':
                        screenName=input('Who Would You Like To Message? ')
                        break
                    elif choice=='2':
                        message=input('Enter Your Message: ')
                        break
                    else:
                        print('Invalid Input. Choose Again')
        api.send_direct_message(user.id,message)
        print('DM Sent')
    except Exception as e:
        print(e[1])

def Follow():
    try:
        choice=input('[1] Follow\n[2] Unfollow\nWhat Would You Like To Do? ')
        if choice=='1':
            screenName=input('Who Would You Like To Follow? ')
            screenName=screenName.strip('@')
            user=api.get_user(screen_name = screenName)
            api.create_friendship(user.id,screenName)
            print(f'Now Following @{screenName}!')
        elif choice=='2':
            screenName=input('Who Would You Like To Unfollow? ')
            screenName=screenName.strip('@')
            user=api.get_user(screen_name = screenName)
            api.destroy_friendship(user.id,screenName)
            print(f'Unfollowed @{screenName} :(')
    except Exception as e:
        print(e)
    
##main
cont=True
while cont:
    Show_Menu()
    while True:
        try:
            choice = input('\nWhat would you like to do? ')
        except ValueError:
            print("Input Error: Lets try again.")
            continue
        else:
            break
    if choice=='1':
        Send_Tweet()
    elif choice =='2':
        Print_Timeline() 
    elif choice =='3':
        Send_DM()
    elif choice=='4':
        Follow()

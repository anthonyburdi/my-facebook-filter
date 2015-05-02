from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from random import randint
import urllib2
import facebook

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def retrieve():
    """Create a shortlink from input link"""
    error = None
    if request.method == 'POST':
        token = request.form['token'] # receive the entered token
        # shortlink = shortLink(links) # create shortlink
        # links[shortlink] = link # place shortlink into global dict
        # comments = get_comments(token)
        # notifications, num_notifications = get_all_notifications(token)
        # friend_requests = get_friend_requests(token)
        # group_notifications = get_group_notifications(token)

        n = separate_notification_types(token)
        inbox = get_inbox(token)

        return render_template('mytoday.html', comments=n['comments'], 
            notifications=n['notifications'], num_notifications=n['total'],
            friend_requests=n['friend_requests'], group_notifications=n['group_notifications'],
             event_notifications=n['event_notifications'], 
             inbox=inbox, error=error)
    if request.method == 'GET':
        return render_template('mytoday.html')

def get_all_notifications(token):
    """Get all notifications"""
    graph = facebook.GraphAPI(token)
    notifications = graph.get_connections(id='me', connection_name='notifications')['data']
    return notifications

def separate_notification_types(token):
    """Return notifications based on type"""
    comments = []
    friend_requests = []
    group_notifications = []
    event_notifications = []
    notifications = get_all_notifications(token)
    for notification in notifications:
        app_name = notification['application']['name']
        if app_name == 'Feed Comments':
            comments.append(notification)
        elif app_name == 'Friends':
            friend_requests.append(notification)
        elif app_name == 'Groups':
            group_notifications.append(notification)
        elif app_name == 'Events':
            event_notifications.append(notification)
        else:
            continue
    return {"comments": comments,
     "friend_requests": friend_requests,
     "group_notifications": group_notifications, 
     "event_notifications": event_notifications,
     "total": len(notifications),
     "notifications": notifications}

def get_inbox(token):
    """Get all available inbox items"""
    graph = facebook.GraphAPI(token)
    inbox_items = graph.get_connections(id='me', connection_name='inbox')
    return inbox_items


# def get_comments(token):
#     """Get all comments notifications"""
#     comments = []
#     notifications, num_notifications = get_all_notifications(token)
#     for notification in notifications:
#         if notification['application']['name'] == 'Feed Comments':
#             comments.append(notification)
#     return comments

# def get_friend_requests(token):
#     """Get all friend request notifications and acceptance notifications"""
#     friend_requests = []
#     notifications, num_notifications = get_all_notifications(token)
#     for notification in notifications:
#         if notification['application']['name'] == 'Friends':
#             friend_requests.append(notification)
#     return friend_requests    

# def get_group_notifications(token):
#     """Get all group related notifications"""
#     group_notifications = []
#     notifications, num_notifications = get_all_notifications(token)
#     for notification in notifications:
#         if notification['application']['name'] == 'Groups':
#             group_notifications.append(notification)
#     return group_notifications

# @app.route('/', methods=['POST', 'GET'])
# def shorten():
#   """Create a shortlink from input link"""
#   error = None
#   if request.method == 'POST':
#       link = request.form['link'] # receive the entered link
#       shortlink = shortLink(links) # create shortlink
#       links[shortlink] = link # place shortlink into global dict
#       return render_template('shortener.html', link=link, 
#           shortlink=shortlink, error=error, links=links, my_ip=my_ip)
#   if request.method == 'GET':
#       return render_template('shortener.html')



if __name__ == '__main__':
    app.debug = True
    app.run(port=5001, host='0.0.0.0') # Port 5000 giving errors, shared w Apple

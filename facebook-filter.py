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
        
        n = separate_notification_types(token)
        inbox = get_inbox(token)

        return render_template('mytoday.html', comments=n['comments'], 
            notifications=n['notifications'], num_notifications=n['total'],
            friend_requests=n['friend_requests'], group_notifications=n['group_notifications'],
             event_notifications=n['event_notifications'], 
             inbox=inbox, error=error)
    if request.method == 'GET':
        return render_template('facebook-filter.html')

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



if __name__ == '__main__':
    app.debug = True
    app.run(port=5001, host='0.0.0.0') # Port 5000 giving errors, shared w Apple

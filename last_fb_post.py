import requests
import json

import persistent


def get_new_post():
    # Currently temporary 60 day token is active! (activated 11 July 2017)
    token = 'EAACEdEose0cBADtIu1L7C5HRfO7NmgyE1glvcpg78Co0qVWfSwAtzLsjOSoaBI51cLvZASLogLJ5txSalXLLR2aCVh0IMBxk2z9fsYQ2uvKpwyT3ZA1v7zXWZAHwDdTVKZBKeyqlBk2rtFUo4tCvZAPUYqBo6SSrgSc1Xotq0WIEN6dGOaTDGNAahlgSq6ZAYZD'
    response = requests.get('https://graph.facebook.com/v2.9/1008311329300738/feed?access_token=%s' % token)
    parsed_data = json.loads(response.content)

    post_message = parsed_data['data'][0]['message']

    # Only show preview of the post
    post_words = post_message.split()
    if len(post_words) > 4:
        post_message = ' '.join(post_words[0:4])

    post_id = parsed_data['data'][0]['id'].split('_')

    # Do not repeat posts
    if 'last_post' in persistent.data:
        if persistent.data['last_post'] == post_id[1]:
            return None

    persistent.lock.acquire()
    persistent.data['last_post'] = post_id[1]
    persistent.save_data()
    persistent.lock.release()

    post_url = '<https://www.facebook.com/%s/posts/%s>' % (post_id[0], post_id[1])

    return post_message + '...\n' + post_url

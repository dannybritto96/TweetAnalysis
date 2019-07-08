from celery import shared_task, current_task
import twitter

@shared_task
def get_followers_n(username,twitter_token,twitter_secret,
                    user_token,user_secret):
    print("tasks.py")
    api = twitter.Api(consumer_key=twitter_token,consumer_secret=twitter_secret,
                      access_token_key=user_token,access_token_secret=user_secret)
    user = api.GetUser(screen_name=username)
    total = user.followers_count
    followers = api.GetFollowers()
    print(user)
    followers = [i.AsDict() for i in followers]
    user_name = []
    followers_n = []
    for i in followers:
        user = api.GetUser(screen_name=i['screen_name'])
        user_name.append(user)
        print(user)
        n = user.followers_count
        print(n)
        followers_n.append(n)
        process_percent = int(100 * float(i) / float(total))
        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent':process_percent})
    if len(user_name) == len(followers_count):
        dicts = {}
        for i in range(len(user_name)):
            dict[user_name[i]] = followers_n[i]
        return dicts
    else:
        return "Can't fetch followers"

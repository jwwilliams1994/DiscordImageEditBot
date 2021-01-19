import random
import time
import datetime

def magicConch(placeholder, randId):
    print("tried")
    conchAnswers = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
                    'Don\'t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.',
                    'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.', 'Yes.',
                    'Yes - definitely.', 'You may rely on it.']
    answer = random.randint(0, 19)
    response = conchAnswers[answer]
    return response

def cyberpunk(placeholder, randId):
    now = datetime.datetime.now()
    release_date = "2020-12-10 00:00:00.0"
    release_obj = datetime.datetime.strptime(release_date, '%Y-%m-%d %H:%M:%S.%f')
    delta_time = release_obj - datetime.datetime.now()
    dt = str(delta_time)[str(delta_time).find(',') + 2:]
    onep = dt.find(":") + 1
    twop = dt.find(":", onep) + 1
    hours = dt[:onep - 1]
    minutes = dt[onep:onep + 2]
    seconds = dt[twop:twop + 2]
    formatted_string = "Cyberpunk 2077 releases in {} days, {} hours, {} minutes, and {} seconds.".format(delta_time.days, hours, minutes, seconds)
    return formatted_string

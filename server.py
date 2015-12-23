import logging
import telegram
from token import TOKEN
from loklak import Loklak

from utils import get_tweet_rating, tweet_reply


LAST_UPDATE_ID = None

l = Loklak()

commands = {
    'no-args': ['/start', '/help'],
    'with-args': ['/search', '/suggest', '/crawler', '/geocode', '/user']
}

def main():
    global LAST_UPDATE_ID

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot(TOKEN)

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        echo(bot)

def search(query):
    """Search Loklak for a specific query.

    Args:
        query: the query to search for.
    Returns:
        search results for query.

    """
    try:
        tweets = l.search(query)['statuses']
        if tweets:
            tweets.sort(key=get_tweet_rating)
            tweet = tweets.pop()
            return tweet_reply(tweet, len(tweets))
        else:
            # Try to search for a weaker query by deleting the last word
            # "An awesome query" -> "An awesome" -> ...
            query = query.split()[:-1]
            if query:
                query = ' '.join(query)
                search(query)
            else:
                return 'Sorry, but I haven\'t found any tweets for your query'
    except:
        return 'Something went wrong'


def serveOptions():
    options = """
            Search API Wrapper which helps to query loklak for JSON results.\n
            Status API Wrapper for the loklak status check.\n
            Suggestions API Wrapper , Works better with local loklak instance.\n
            Crawler API Wrapper on Loklak to crawl for tweets for a particular crawl depth.\n
            Loklak status check API.\n
            Geocode API for geolocation based information.\n
            Loklak API for peers connected on the distributed network.\n
            Public API to push geojson objects to the loklak server.\n
            User API to show twitter user information.\n
            Map Visualization render using Loklak service.\n
            Markdown conversion API to render markdown as image using Loklak.\n
            """
    return options

def stringParse(bot, messageString):
    # String parser functions that are required for the bot.
    global LAST_UPDATE_ID

    # String parse as required according to the functions
    try:
        command, query = messageString.split(' ', 1)
    except ValueError:
        # single argument given
        command = messageString
        if command in commands['no-args']:
            if command == '/start' or command == '/help':
                return serveOptions()
        else:
            if command in commands['with-args']:
                return 'Sorry, you have to pass some arguments to {}'.format(command)
            else:
                return 'Sorry, but I don\'t know what to do with {}'.format(command)
            
    if command in commands['with-args']:      
        if command == '/search':
            return search(query)
        elif command == '/status':
            # do some operations
            pass
        elif command == '/suggest':
            # do some operations
            pass
        elif command == '/crawler':
            # do some operations
            pass
        elif command == '/geocode':
            # do some operations
            pass
        elif command == '/user':
            # do some operations
            pass
    else:
        return 'Sorry, but I don\'t know what to do with {}'.format(command)

def echo(bot):
    global LAST_UPDATE_ID

    # Request updates after the last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        # chat_id is required to reply any message
        chat_id = update.message.chat_id
        message = update.message.text.encode('utf-8')

        if message:
            # Reply the message
            print str(chat_id) + ' :: ' + str(message)
            reply = stringParse(bot, message)
            bot.sendMessage(chat_id=chat_id,
                            text=reply)

            # Updates global offset to get the new updates
            LAST_UPDATE_ID = update.update_id + 1


if __name__ == '__main__':
    main()
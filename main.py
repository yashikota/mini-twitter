import tweepy
import os
from dotenv import load_dotenv
import discord


# 認証
def twitter_auth():
    load_dotenv()
    client = tweepy.Client(bearer_token=os.environ["BT"])

    return client


def discord_auth():
    load_dotenv()
    token = os.getenv("DISCORD")
    client = discord.Client()

    return token, client


def get_tweets():
    client = twitter_auth()
    ID = "1419021878115540995"
    tweet_list = list()

    tweets = client.get_users_tweets(id=ID, max_results=20)
    for tweet in tweets[0]:
        tweet_id = tweet.id
        tweet_url = "https://twitter.com/{}/status/{}".format(ID, tweet_id)
        tweet_list.append(tweet_url)

    return tweet_list


def post_discord(tweet_list):
    load_dotenv()
    token = os.getenv("DISCORD")
    client = discord.Client()
    message_list = list()

    @client.event
    async def on_ready():
        ch_name = "mini様のありがたいお言葉"
        for channel in client.get_all_channels():
            if channel.name == ch_name:
                # 最新のメッセージ本文を取得
                last_msg = await channel.fetch_message(channel.last_message_id)
                last_msg_content = last_msg.content

                for tweet in tweet_list:
                    if tweet != last_msg_content:
                        message_list.append(tweet)
                    else:
                        break

                message_list.reverse()

                for message in message_list:
                    if message != last_msg_content:
                        await channel.send(message)
                    else:
                        await client.close()

        await client.close()

    try:
        client.run(token)
    except RuntimeError:
        print("token is invalid")


def main():
    tweet_list = get_tweets()
    post_discord(tweet_list)


if __name__ == "__main__":
    main()

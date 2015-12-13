import tweepy

consumer_key = " "74dgq1cyvMXe7Ll52hTIMIL0x":wq";



consumer_secret = "I53EJlz15MzzUV23meVOxuDSQvwmdci6V8MHIFaLsF7JFaEk8S";


access_token = "139377964-qiuWyeWTtmgrkOBblySTRBLkd2dRkTpaCEDru36O";


access_token_secret =  "UFtTLjOxIRBcxf2djbGm72Ql36Nfx5w6FJNEOelMr1rKh";



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Imports
import os
import tweepy
from dotenv import load_dotenv
import pandas as pd
import time
from tweepy.errors import TooManyRequests

# Load environment variables
load_dotenv()

# Authenticate user credentials
client = tweepy.Client(
    # Access tokens via .env using variables
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET")
)

# Verify authentication
print("Authentication Sucessful!")


# Function to search through tweets based on user-given parameters
def search_tweets(query, max_results=10):

    # Try to execute the search logic provided that too many requests have not been made 
    try:

        # Store search results into the tweets object
        tweets = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "public_metrics", "author_id"],
            expansions=["author_id"]
        )
        
        # Create empty list
        tweet_data = []

        ''' If search data exists, loop through the tweets and append them
        to the empty list for easy access
        '''

        # If tweet data exists, append the data to the empty list for easier access
        if tweets.data:
            for tweet in tweets.data:
                tweet_data.append({
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "likes": tweet.public_metrics["like_count"],
                    "retweets": tweet.public_metrics["retweet_count"],
                    "author": tweet.author_id
                })
        
        # Return the tweet data list as a dataframe using pandas
        return pd.DataFrame(tweet_data)
    
    # Exception to handle too many requests (Free API Tier)
    except TooManyRequests:
        print("Hit rate limit! Waiting 15 minutes...")

        # Wait 15 minutes
        time.sleep(15 * 60) 

        # Retry 
        return search_tweets(query, max_results)


# Get user tweets using user parameters
def get_user_tweets(username, max_results=10):

    # Get a hold of correct user and store tweet data into the tweets object. 
    user = client.get_user(username=username)
    tweets = client.get_users_tweets(
        user.data.id,
        max_results=max_results,
        tweet_fields=["created_at", "public_metrics"]
    )
    
    # Use pandas to return data as a dataframe for easy access
    return pd.DataFrame([{
        "text": tweet.text,
        "created_at": tweet.created_at,
        "likes": tweet.public_metrics["like_count"]
    } for tweet in tweets.data])


# Function to display basic stats about the collected tweets
def display_stats(df):

    # Display the stats (Total tweets, likes, most popular, etc)
    print("\n=== Tweet Statistics ===")
    print(f"Total Tweets: {len(df)}")
    print(f"Average Likes: {df['likes'].mean():.1f}")
    if 'retweets' in df.columns:
        print(f"Average Retweets: {df['retweets'].mean():.1f}")
    print("\nMost Popular Tweet:")
    print(df.loc[df['likes'].idxmax()]['text'])


# Function to save pandas dataframe to a csv
def save_to_csv(df, filename):

    # Save DataFrame to CSV
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")


# Main function to handle user choice and correlating functions
def main():
    print("\n=== Twitter Data Miner ===")
    
    # Ask user what they would like to do with validation
    while True:
        print("\nOptions:")
        print("1. Search tweets by keyword")
        print("2. Get tweets from a user")
        print("3. Exit")
        
        # Retrieve input 
        choice = input("Enter your choice (1-3): ")
        
        # Conditionals for each user choice (1-3)
        if choice == "1":

            # Ask user for a search parameter, then pass that parameter to the search function.
            query = input("Enter search query: ")
            max_results = int(input("Number of tweets to fetch (10-100): "))
            df = search_tweets(query, max_results)

            # Use display function to show the user their results and save to a csv
            print("\n=== Search Results ===")
            print(df.head())
            display_stats(df)
            save_to_csv(df, f"{query}_tweets.csv")
        
        # Conditionals continued
        elif choice == "2":

            # Ask user for their desired username to search by
            username = input("Enter Twitter username (without @): ")
            max_results = int(input("Number of tweets to fetch (10-100): "))
            df = get_user_tweets(username, max_results)

            # Use display function to show the user their results and save to a csv
            print(f"\n=== @{username}'s Recent Tweets ===")
            print(df.head())
            display_stats(df)
            save_to_csv(df, f"{username}_tweets.csv")
        
        # Conditional to end the program
        elif choice == "3":
            print("Exiting...")
            break
        
        # Conditional to handle incorrect input
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
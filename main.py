import os
import csv

import twitter

TOKENS = {
    'consumer_key': os.environ.get('TWITTER_CONSUMER_KEY'),
    'consumer_secret': os.environ.get('TWITTER_CONSUMER_SECRET'),
    'access_token_key': os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
    'access_token_secret': os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
}

FIELDS = ['link', 'favorites', 'retweets', 'user']


def main():
    favorites = []
    offset = None

    # Twitter API Client bootstrapping
    api = twitter.Api(**TOKENS)

    print(f'Fetching...')
    while True:

        # Get 200 results
        try:
            results = api.GetFavorites(count=200, max_id=offset)
        except twitter.errors.TwitterError:
            print('Rate limit exceeded. Exiting.')
            break
        except:
            print('Exiting.')
            break

        # Save results
        favorites = [*favorites, *[res.AsDict() for res in results]]
        print(f'  Fetched {len(favorites)}. max_id={offset}', end='\r')

        # Save last ID for later
        offset = results[-1].id

        # Game over ?
        if len(results) == 1:
            print(f'\nFetched all favorites. Exiting.')
            break

    # Export result in CSV format.
    with open('out.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        for favorite in favorites:
            writer.writerow({
                'link': 'https://twitter.com/team_vitality/status/'+favorite['id_str'],
                'favorites': favorite['favorite_count'],
                'retweets': favorite.get('retweet_count', 0),
                'user': favorite['user']['screen_name']
            })


if __name__ == '__main__':
    main()

import requests
import pandas as pd


def grab_data(headers, payload, endpoint):
    response = requests.post(f'https://search.patentstyret.no/api/search/{endpoint}',
                             headers=headers,
                             json=payload)
    
    data = response.json()
    return data


def scraper(endpoint):
    headers = {
        'sec-ch-ua-platform': 'Windows',
        'Referer': 'https://search.patentstyret.no/advanced/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-GB,en,q=0.5',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'Origin': 'https://search.patentstyret.no',
        'Content-Type': 'application/json'
    }

    size = 1000

    payload = {
        'aggregation': {},
        'filters': [],
        'from': 0,
        'size': size
    }
    
    data = grab_data(headers, payload, endpoint)
    total_hits = data['totalHits']

    result_df = pd.DataFrame(data['results'])

    for i in range(size, total_hits, size):
        payload['from'] = i
        data = grab_data(headers, payload, endpoint)
        data = data['results']
        payload_df = pd.DataFrame(data)

        result_df = pd.concat([result_df, payload_df])

        print(f'{i} rows')


    result_df.to_csv('result.csv', index=False, encoding='utf-8')


def main():
    # patent endpoint: '' (empty)
    # trademark endpoint: 'trademark'
    # design endpoint: 'design'
    endpoint = ''

    scraper(endpoint)


if __name__ == '__main__':
    main()

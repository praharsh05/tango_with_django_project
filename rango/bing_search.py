import json
import requests
import os



def read_bing_key():
    """
    reads the BING API key from a file called 'bing.key'
    returns: a string which is either None, i.e. no key found, or with a key
    remember to put bing.key in your .gitignore file to avoid committing it.

    See Python Anti-Patterns - it is an awesome resource to improve your python code
    Here we using "with" when opening documents
    http://bit.ly/twd-antipattern-open-files
    """

    bing_api_key = None
    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline().strip()
    except:
        try:
            with open('../bing.key','r') as f:
                bing_api_key = f.readline().strip()
        except:
            raise IOError('bing.key file not found')
    
    if not bing_api_key:
        raise KeyError('Bing key not found')
    
    return bing_api_key

def run_query(search_terms):
    """
    See the Microsoft's documentation on other parameters that you can set.
    http://bit.ly/twd-bing-api
    """
    bing_key = read_bing_key()
    endpoint = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_key}
    params = {"q": search_terms, "textDecorations": True, "textFormat":"HTML"}
    #Issue the request, given the details above
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    search_result = response.json()

    #with response now in play build a list
    results=[]
    for result in search_result['webPages']['value']:
        results.append({
            'title':result['name'],
            'link':result['url'],
            'summary':result['snippet']
        })
    return results

def main():
    searching = input("enter query: ")
    results = run_query(searching)
    for result in results:
        print(result)


if __name__ == '__main__':
    main()



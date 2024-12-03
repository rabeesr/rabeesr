import requests
import datetime

baseurl = 'https://newsapi.org/v2'
date = 'from=' + str(datetime.date.today())
sort = 'sortBy=popularity&'
APIKEY= #REPLACE

def format_date(published_date):
    try:
        date_obj = datetime.datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%SZ')
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return "Unknown Date"

# [1] business   
# [2] entertainment   
# [3] general   
# [4] health   
# [5] science   
# [6] sports   
# [7] technology   
def getCategory(category):
    categories = {'1': 'business', '2': 'entertainment', '3':'general',
                  '4': 'health', '5':'science', '6':'sports', '7':'technology'

                    }
    return categories[category]

class getNews():
    def get_top_headlines(category):
        url = f'{baseurl}/top-headlines?sortBy=popularity&category={category}&apiKey={APIKEY}'
        list_of_articles=[]
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for article in enumerate(data.get('articles', []), start=0):
                list_of_articles.append(article)
            return list_of_articles
        else:
            print(f"Error fetching data: {response.status_code}")
    def search_articles(searchterm):
        url = f'{baseurl}/everything?sortBy=publishedAt&q={searchterm}&apiKey={APIKEY}'
        list_of_articles=[]
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for article in enumerate(data.get('articles', []), start=0):
                list_of_articles.append(article)
            return list_of_articles
        else:
            print(f"Error fetching data: {response.status_code}")

def main():
    print('Welcome to Command Line News!\n\n')
    run = 'y'
    while run.lower() == 'y':
        ent = input('Please make a choice: [1] Top headlines [2] Search\n>> ')
        if ent == '1':
                print("\nSelect which category would you like to headlines for:")
                print("[1] business")
                print("[2] entertainment")
                print("[3] general")
                print("[4] health")
                print("[5] science")
                print("[6] sports")
                print("[7] technology")
                category = input('Please enter a category>> ')
                category_map = getCategory(category)
                list_of_articles = getNews.get_top_headlines(category_map)
                for i in list_of_articles[0:10]:
                    date = format_date(i[1]['publishedAt'])
                    print(f"{i[0]+1}. {i[1]['title']}\n  \tPublished: {date}\n  \tDescription: {i[1]['description']}\n \tSource: {i[1]['source']['name']}\n   \tURL: {i[1]['url']}\n")
                run = input('Would you like to find more news articles? [y/n]\n>>')
        if ent == '2':
            searchterm = input(f'Enter your search term:\n >> ')
            list_of_articles = getNews.search_articles(searchterm)
            if list_of_articles != []:
                for i in list_of_articles[0:10]:
                    date = format_date(i[1]['publishedAt'])
                    print(f"{i[0]+1}. {i[1]['title']}\n  \tPublished: {date}\n  \tDescription: {i[1]['description']}\n \tSource: {i[1]['source']['name']}\n   \tURL: {i[1]['url']}\n")
            else:
                print('Sorry there were no articles found with the keyword. Please try with a different keyword')
            run = input('Would you like to find more news articles? [y/n]\n>> ')

if __name__ == '__main__':
    main()

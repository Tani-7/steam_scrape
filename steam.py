import requests
import lxml.html
import pandas as pd


# Steam is blockinf scrapping so these headers are a must --afterthought
# html = requests.get('https://store.steampowered.com/explore/new/')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
    html = requests.get(
        'https://store.steampowered.com/explore/new/', headers=headers)
    html.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    exit()

doc = lxml.html.fromstring(html.content)

new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]
titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')

prices = new_releases.xpath(
    './/div[contains(@class, "discount_final_price") or contains(@class, "tab_item_price")]/text()')
tags_divs = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
# tags = []

# print(prices)

# for div in tags_divs:
# tags.append(div.text_content())
# print(tags)

# tags = [tag.split(', ') for tag in tags]
tags = [div.text_content().split(', ')
        for div in new_releases.xpath('.//div[@class="tab_item_top_tags"]')]


# platforms_div = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
total_platforms = []

# for game in platforms_div:
#    temp = game.xpath('.//span[contains(@class, "platform_img")]')
#    platforms = [t.get('class').split(' ')[-1] for t in temp]
#    if 'hmd_separator' in platforms:
#        platforms.remove('hmd_separator')
#        total_platforms.append(platforms)

# print(total_platforms)
for game in new_releases.xpath('.//div[@class="tab_item_details"]'):
    platforms = [
        span.get('class').split()[-1].replace('_separator', '')
        for span in game.xpath('.//span[contains(@class, "platform_img")]')
        # if 'hmd_separator' not in span.get('class')
        if 'vr_required' not in span.get('class')
    ]
    total_platforms.append(', '.join(platforms))

# for info in zip(titles, prices, tags, total_platforms):
# Using tyupples was the wrong idea here, what were you thinking charles !!!
# resp = ()
# resp['title'] = info[0]
# resp['price'] = info[1]
# resp['tags'] = info[2]
# resp['platforms'] = info[3]
# output.append(resp)

# games = pd.to_DataFrame(
# output, columns=[titles, prices, tags, total_platforms], index=False)
# Gives empty dataframe,,,,,troubleshoot

# output = []
# for title, price, tag, platform in zip(titles, prices, tags, total_platforms):
#    output.append({
#        'title': title,
#        'price': price,
#        'tags': tag,
#        'platforms': platform
#    })

print(f"Titles: {len(titles)}")
print(f"Prices: {len(prices)}")
print(f"Tags: {len(tags)}")
print(f"Platforms: {len(total_platforms)}")


# Create DataFrame
# games = pd.DataFrame(output)
if len(titles) == len(prices) == len(tags) == len(total_platforms):
    games = pd.DataFrame({
        'title': titles,
        'price': [p.strip() for p in prices],
        'tags': tags,
        'platforms': total_platforms
    })

    print("\nFirst 10 entries:")
    print(games.head(10))
else:
    print("\nData mismatch - check your XPaths:")
    print(
        f"Titles: {len(titles)}, Prices: {len(prices)}, Tags: {len(tags)}, Platforms: {len(total_platforms)}")

filename = "steam_new_releases.csv"
filename2 = "steam_new_releases.xlsx"
games.to_csv(filename, index=False, encoding='utf-8')
games.to_excel(filename2, index=False, engine='openpyxl')

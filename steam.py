import requests
import lxml.html
import pandas as pd

html = requests.get('https://store.steampowered.com/explore/new/')
doc = lxml.html.fromstring(html.content)

new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]
titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')

prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')
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
        span.get('class').split()[-1]
        for span in game.xpath('.//span[contains(@class, "platform_img")]')
        if 'hmd_separator' not in span.get('class')
    ]
    total_platforms.append(platforms)

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

games = pd.DataFrame({
    'title': titles,
    'price': prices,
    'tags': tags,
    'platforms': total_platforms
})

# Display the DataFrame
print(games.head())

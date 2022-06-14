import re

patterns = {
    re.compile('^搜\\s(.*)$'): ['actions.ActionSearchImages', 'search_for_shop_names'],
    re.compile('^圖\\s(.*)$'): ['actions.ActionSearchImages', 'list_shop_images'],
    re.compile('^[雷達|天氣].*'): ['actions.ActionWeatherInfo', 'get_cloud_image']
}

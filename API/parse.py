from .request import get_response


class WildberrisParse:
    
    default_url = 'https://card.wb.ru/cards/v1/detail?appType=1&curr=uzs&dest=491&spp=27&nm='
    default_url_image = 'https://basket-{}.wbbasket.ru/vol{}/part{}/{}/images/c246x328/1.webp'
    
    def __init__(self, article: str) -> None:
        """Initialize WildParse

        Args:
            article (str): article product from wildberris
        """
        self.article = int(article)
        self.full_url = self.default_url + article
        self.response = get_response(self.full_url)
        self.data = self.response.json()
    
    def parse(self, with_image: bool = True) -> dict:
        """Parse data from json WildberrisAPI
        
        Args:
            with_image (bool, optional): Get product data with image card or not, default with. Defaults to True.

        Returns:
            dict: Data in dict
        """
        data = self.__get_normalize_data()
        if with_image:
            data.update(self.__get_normalize_image())
        return data

    def __get_normalize_data(self) -> dict:
        data = self.data['data']['products'][0]
        return {
            'brand': data['brand'], 'feedbacks': data['feedbacks'],
            'rating_feedbacks': data['reviewRating'], 'article': str(data['id']), 'name': data['name'].capitalize(), 
            'rating': data['rating'], 'price': int(data['salePriceU'] / 100)
        }
        
    def __get_normalize_image(self) -> dict:
        _short_id = self.article // 100000
        if 0 <= _short_id <= 143:basket = '01'
        elif 144 <= _short_id <= 287:basket = '02'
        elif 288 <= _short_id <= 431:basket = '03'
        elif 432 <= _short_id <= 719:basket = '04'
        elif 720 <= _short_id <= 1007:basket = '05'
        elif 1008 <= _short_id <= 1061:basket = '06'
        elif 1062 <= _short_id <= 1115:basket = '07'
        elif 1116 <= _short_id <= 1169:basket = '08'
        elif 1170 <= _short_id <= 1313:basket = '09'
        elif 1314 <= _short_id <= 1601:basket = '10'
        elif 1602 <= _short_id <= 1655:basket = '11'
        elif 1656 <= _short_id <= 1919: basket = '12'
        else: basket = '13'
        return {
            'url_image': self.default_url_image.format(basket, _short_id, self.article // 1000, self.article)
        }

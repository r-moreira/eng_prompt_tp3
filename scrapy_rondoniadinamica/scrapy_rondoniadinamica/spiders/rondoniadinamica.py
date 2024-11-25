from typing import Dict, Generator
import scrapy
from datetime import datetime, timedelta
import pytz

class RondoniadinamicaSpider(scrapy.Spider):
    limit_pages = 10
    name = "rondoniadinamica"
    allowed_domains = ["rondoniadinamica.com"]
    start_urls = ["https://rondoniadinamica.com/ultimas-noticias?pagina=1"]

    def parse(self, response):
        news_links = response.css('div.post-thumb a::attr(href)').getall()
        for link in news_links:
            yield response.follow(link, self._parse_news)
            
        next_page = self._increment_page_url(response.url)
        if next_page:
            yield response.follow(next_page, self.parse)
        
    def _increment_page_url(self, url) -> str | None:
        current_page = int(url.split('=')[-1])
        
        if current_page < RondoniadinamicaSpider.limit_pages:
            return url.split('=')[0] + '=' + str(current_page + 1)
        return None
    
    def _parse_news(self, response):
        title = response.css('h1 strong::text').get()
        subtitle = response.css('div.post-data div div.post-excerp::text').get()
        author = response.css('div.post-excerp strong:nth-of-type(1)::text').get()
        datetime = self._parse_news_datetime(response)
        content = response.css('div.post-data div.post-meta p::text').getall()
                
        yield {
            'url': response.url,
            'datetime': datetime,
            'title': title.strip() if title else None,
            'subtitle': subtitle.strip() if subtitle else None,
            'author': author.strip() if author else None,
            'content': [p.strip() for p in content if p.strip()]
        }
        
    def _parse_news_datetime(self, response) -> str:
        datetime = response.css('div.post-excerp strong:nth-of-type(2)::text').get()
        return self._parse_date(datetime)
    
    def _parse_date(self, date_str: str) -> str:               
        local_dt = datetime.strptime(date_str, "%d/%m/%Y às %Hh%M")
        local_dt =  pytz.timezone('America/Sao_Paulo').localize(local_dt) + timedelta(hours=3)
        return local_dt.isoformat()
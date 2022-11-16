import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MoviesSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc', headers={
            'User-Agent' : self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='lister-page-next next-page']"), process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield{
            'name' : response.xpath("//div[@class='sc-80d4314-1 fbQftq']/h1/text()").get(),
            'year' : response.xpath("//div[@class='sc-80d4314-2 iJtmbR']/ul/li[1]/span/text()").get(),
            'genre' : response.xpath("//a[@class='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt']/span/text()").get(),
            'duration' : ''.join(response.xpath("//div[contains(@class,'sc-80d4314-2 iJtmbR')]/ul/li[3]/text()").getall()),
            'rating': response.xpath("//div[@class='sc-7ab21ed2-2 kYEdvH']/span/text()").get(),
            'url' : response.url
        }
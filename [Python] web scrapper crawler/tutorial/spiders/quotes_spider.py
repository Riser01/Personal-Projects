import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    def start_requests(self):
        urls =['https://www.thefamouspeople.com/famous-people-by-birthday.php',]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        monthsurlhalf=response.css("div.pod.colorbar.editorial a::attr(href)").extract()
        for x in monthsurlhalf:
            yield scrapy.Request(url="https:"+x,callback=self.parsemonths)
        
    def parsemonths(self,response):
        daysurlhalf=response.css("div.col-md-12 a::attr(href)").extract()
        for x in daysurlhalf:
            yield scrapy.Request(url="https:"+x,callback=self.parsedays)

    def parsedays(self,response):
        month=response.css("title::text").extract_first().split(" ")[0:1][0]
        date=response.css("title::text").extract_first().split(" ")[1:2][0]
        for quote in response.css('div.tile'):
            yield {'name': quote.css(".btn-primary.btn-sm.btn-block::text").extract_first() if quote.css(".btn-primary.btn-sm.btn-block::text").extract()!=[] else "",'country': quote.css("p::text").extract_first() if quote.css("p::text").extract()!=[] else "" ,'tags': quote.css(".rec-country-name::text").extract_first()  if quote.css(".rec-country-name::text").extract()!=[] else "" ,'image': "https:"+quote.css("img::attr(data-src)").extract()[0] if quote.css("img::attr(data-src)").extract()!=[] else "https:"+quote.css("img::attr(src)").extract_first() if quote.css("img::attr(src)").extract()!=[] else ""  ,'date': date,'month': month,'bday':1,"dday":0}

            

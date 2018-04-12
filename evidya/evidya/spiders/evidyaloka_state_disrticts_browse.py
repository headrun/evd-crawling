import scrapy
import json
from scrapy.selector import Selector
from scrapy.http import FormRequest
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class EvdcodesBrowse(scrapy.Spider):
    name = 'evidyalokacodes_browse'
    start_urls = ['http://schoolreportcards.in/SRC-New/AdvanceSearch/AdvanceSearch.aspx']

    def __init__(self):
        self.final_dict = {}
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self,spider):
        with open('information.json', 'w') as file1:
            json.dump(self.final_dict, file1)

    def parse(self, response):
        sel = Selector(response)
        form_data = {"Method":"FillDropDown", "ACYear":"2016-17","Code":"0","DropDownName":"State","Type":"0","TName":"SCHDATA4NET"}
        yield FormRequest('http://schoolreportcards.in/SRC-New/AjaxCallerService.axd', callback = self.parse_now, formdata = form_data, meta = {'state_data':form_data})

    def parse_now(self, response):
        sel = Selector(response)
        state_codes_dict, data_json = {}, {}
        try:
            data_json = json.loads((response.body).split('|')[-1].strip('[').strip(']').strip('[').strip(']'))
        except:
            data_json = {}
        if data_json:
            data_ = data_json.get('Data', {})
            for each in data_:
                state_name = each.get('DropDownName', '')
                
                state_code = each.get('DropDownValue', '')
                form_district_data = {'Code': str(state_code), 'ACYear': '2016-17', 'DropDownName': 'District', 'TName': 'SCHDATA4NET', 'Type': '0', 'Method': 'FillDropDown'}
                yield FormRequest('http://schoolreportcards.in/SRC-New/AjaxCallerService.axd', callback = self.parse_new, formdata = form_district_data, meta = {"state_name":state_name, "state_code":state_code})

    def parse_new(self, response):
        sel = Selector(response)
        state_name = response.meta.get('state_name', '').strip()
        state_code = response.meta.get('state_code', '').strip()
        data_json = json.loads((response.body).split('|')[-1].strip('[').strip(']').strip('[').strip(']'))
        csv = data_json.get('Data', {})
        district_codes = {}
        for each in csv:
            district_name = each.get('DropDownName','').strip()
            district_code = each.get('DropDownValue','').strip()
            district_codes.update({district_code:district_name})
        self.final_dict.update({state_code:[district_codes, state_name]})


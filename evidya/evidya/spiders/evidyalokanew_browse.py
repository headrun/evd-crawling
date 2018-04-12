import scrapy
import json
from scrapy.selector import Selector
from scrapy.http import FormRequest
from evidya.items import *

class EvdnewBrowse(scrapy.Spider):
    name = 'evidyanew_browse'
    start_urls = ['http://schoolreportcards.in/SRC-New/AdvanceSearch/AdvanceSearch.aspx']

    def parse(self, response):
        sel = Selector(response)
        state_data = {"Method":"FillDropDown", "ACYear":"2016-17","Code":"0","DropDownName":"State","Type":"0","TName":"SCHDATA4NET"}

        yield FormRequest('http://schoolreportcards.in/SRC-New/AjaxCallerService.axd', callback = self.parse_now, formdata = state_data, meta = {'data1':state_data})

    def parse_now(self, response):
        sel = Selector(response)
        form_data = response.meta.get('data1','')
        district_data = {"Method":"FillDropDown","ACYear": "2016-17","TName": "SCHDATA4NET","Code": "2822","DropDownName": "Block","Type": "0"}
        yield FormRequest('http://schoolreportcards.in/SRC-New/AjaxCallerService.axd', callback = self.parse_new, formdata = district_data, meta = {'data1':form_data,'data2':district_data})

    def parse_new(self, response):
        sel = Selector(response)
        #data2 = response.meta.get('data2','')
        data1 = response.meta.get('data1','')
        import pdb;pdb.set_trace()
        data_json = json.loads((response.body).split('|')[-1].strip('[').strip(']').strip('[').strip(']'))
        csv = data_json.get('Data')
        
        for each in csv:
            dropdownname = each.get('DropDownName','')
            dropdownvalue = each.get('DropDownValue','')
            import pdb;pdb.set_trace()
        view_state = ''.join(sel.xpath('//input[@name="__VIEWSTATE"]/@value').extract())
        generator_view = ''.join(sel.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract())
        headers = {
            'Origin': 'http://schoolreportcards.in',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Referer': 'http://schoolreportcards.in/SRC-New/AdvanceSearch/AdvanceSearch.aspx',
            'Connection': 'keep-alive',
        }
        form_dict = {"PageSize":"10","PageNo":"1" ,"AcadYear":"2016-17","StateCD":data1,"DistrictCD":data2,"BlockCD":"","ClusterCD":"","VillageCD":"","SchoolManagement":"","SchoolCategory":"","SchoolArea":"","SchoolType":"","CToilet":"","BToilet":"","GToilet":"","Electricity":"","Ramps":"","Building":"","Boundary":"","Playground":"","DrinkingWater":"","MedCheckup":"","Library":"","PPSection":"","HMRoom":"","Computers":"","CAL":"","KitDevGrant":"","MDM":"","WeatherRoad":"","CCE":"","SMC":"","Residential":"","Shift":"","HM":"","ContractTeacher":"","Disabled":"","BlackBoard":"","MajorRepair":"","EstYear":"","SchoolFunc":"","BRCCoordinator":"","CRCCoordinator":"","PTR":"","SCR":"","Classrooms":"","TotalTeacher":"","Enrolment":"","TeachProfQual":"","SearchString":"","SearchCriteria":"","BuildingType":"","MinorRepair":"","ClassGoodCondition":"","Handrail":"","TableNameDatabase":"SCHDATA4NET","SortBy":"SCHNAME","MediumType":"","RTEGrade":-1,"SchoolName":"","Method":3}
        form_data1 = {'__EVENTARGUMENT': '', '': '', '__VIEWSTATE': view_state, 'txtSearchSchool': '', '__CALLBACKID': '__Page', '__CALLBACKPARAM': json.dumps(form_dict), '__VIEWSTATEGENERATOR': generator_view, '__EVENTTARGET': ''}
        yield FormRequest('http://schoolreportcards.in/SRC-New/AdvanceSearch/AdvanceSearch.aspx', callback=self.parse_next,formdata=form_data1, meta = {'form_dict':form_dict , 'form_data':form_data1})

    def parse_next(self, response):
        import pdb;pdb.set_trace()
        form_data = response.meta.get('form_data','')
        form_dict = response.meta.get('form_dict','')
        page_no = response.meta.get('form_dict',{}).get('PageNo', '')
        data_json = json.loads((response.body).split('|')[-1].strip('[').strip(']'))
        csv = data_json['Data']
        next_page = ''
        for each in csv:
            print each
            totalrecords = each.get('TotalRecords','')
            page_size = each.get('PageSize','')
            page_number = page_no
            complete_records = page_number * page_size
            if complete_records > totalrecords:
                next_page = int(page_number) + 1
            else:
                next_page = ''
            school_code = each.get('SchoolCD','')
            school_name = each.get('SchoolName','')
            block_name = each.get('BlockName', '')
            rural_urban = each.get('SchoolRuralUrban','')
            schl_mngmnt = each.get('SchoolManagementName','')
            schl_categry = each.get('SchoolCategory','')
            schl_type = each.get('SchoolType','')
            rte_grade = each.get('RTEGrade','')
            hm_name = each.get('HeadMasterName','')
            evidya = EvidyaItem()
            evidya['page_number'] = page_number  
            evidya['school_code'] = school_code
            evidya['school_name'] = school_name
            evidya['block_name'] = block_name
            evidya['rural_urban'] = rural_urban
            evidya['schl_mngmnt'] = schl_mngmnt
            evidya['schl_categry'] = schl_categry
            evidya['schl_type'] = schl_type
            evidya['rte_grade'] = rte_grade
            evidya['hm_name'] = hm_name
            yield evidya
        if next_page:
           form_dict["PageNo"] = next_page
           form_data["__CALLBACKPARAM"] = json.dumps(form_dict)
           yield FormRequest('http://schoolreportcards.in/SRC-New/AdvanceSearch/AdvanceSearch.aspx', callback = self.parse_next, formdata = form_data, meta = {'form_dict':form_dict , 'form_data':form_data})
           
           


            
            




            

import json
import scrapy

from scrapy.http        import FormRequest
from scrapy.selector    import Selector

from evidya.items       import *


class EvdmetaBrowse(scrapy.Spider):
    
    name = 'evidyameta_browse'
    
    start_urls = ['http://schoolreportcards.in/SRC-New/AdvanceSearch/AdvanceSearch.aspx']
    
    def __init__(self):
        with open("information.json", "r") as data:
            self.information = json.load(data)
        
    def parse(self, response):
        sel = Selector(response)
        view_state = ''.join(sel.xpath('//input[@name="__VIEWSTATE"]/@value').extract())
        generator_view = ''.join(sel.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract())
        
        for key, value in self.information.iteritems():
                for key1, value1 in value[0].iteritems():
                    form_dict = {   "PageSize":"10",
                                    "PageNo":"1" ,
                                    "AcadYear":"2016-17",
                                    "StateCD":key,
                                    "DistrictCD":key1,
                                    "BlockCD":"",
                                    "ClusterCD":"",
                                    "VillageCD":"",
                                    "SchoolManagement":"",
                                    "SchoolCategory":"",
                                    "SchoolArea":"",
                                    "SchoolType":"",
                                    "CToilet":"",
                                    "BToilet":"",
                                    "GToilet":"",
                                    "Electricity":"",
                                    "Ramps":"",
                                    "Building":"",
                                    "Boundary":"",
                                    "Playground":"",
                                    "DrinkingWater":"",
                                    "MedCheckup":"",
                                    "Library":"",
                                    "PPSection":"",
                                    "HMRoom":"",
                                    "Computers":"",
                                    "CAL":"",
                                    "KitDevGrant":"",
                                    "MDM":"",
                                    "WeatherRoad":"",
                                    "CCE":"",
                                    "SMC":"",
                                    "Residential":"",
                                    "Shift":"",
                                    "HM":"",
                                    "ContractTeacher":"",
                                    "Disabled":"",
                                    "BlackBoard":"",
                                    "MajorRepair":"",
                                    "EstYear":"",
                                    "SchoolFunc":"",
                                    "BRCCoordinator":"",
                                    "CRCCoordinator":"",
                                    "PTR":"",
                                    "SCR":"",
                                    "Classrooms":"",
                                    "TotalTeacher":"",
                                    "Enrolment":"",
                                    "TeachProfQual":"",
                                    "SearchString":"",
                                    "SearchCriteria":"",
                                    "BuildingType":"",
                                    "MinorRepair":"",
                                    "ClassGoodCondition":"",
                                    "Handrail":"",
                                    "TableNameDatabase":"SCHDATA4NET",
                                    "SortBy":"SCHNAME",
                                    "MediumType":"",
                                    "RTEGrade":-1,
                                    "SchoolName":"",
                                    "Method":3
                                }
                    form_data1 = {  '__EVENTARGUMENT': '', 
                                    '': '', 
                                    '__VIEWSTATE': view_state, 
                                    'txtSearchSchool': '', 
                                    '__CALLBACKID': '__Page', 
                                    '__CALLBACKPARAM': json.dumps(form_dict), 
                                    '__VIEWSTATEGENERATOR': generator_view, 
                                    '__EVENTTARGET': ''
                                }           
                    yield FormRequest('http://schoolreportcards.in/SRC-New/AdvanceSearch/AdvanceSearch.aspx', callback=self.parse_next,formdata=form_data1, meta = {'form_dict':form_dict , 
                                                                                                                    'form_data':form_data1, 'state_name':value[-1], "district_name":value1})
                    # Question to Ramya? why send it(form_data1) as both form_data and in meta ??

    def parse_next(self, response):
        state_name = response.meta.get('state_name', '')
        district_name = response.meta.get('district_name','')
        form_data = response.meta.get('form_data','')
        form_dict = response.meta.get('form_dict','')
        page_no = response.meta.get('form_dict',{}).get('PageNo', '')
        data_json = json.loads((response.body).split('|', 1)[-1].strip('[').strip(']'))
        csv = data_json.get('Data', {})
        next_page = ''
        for each in csv:
            totalrecords = each.get('TotalRecords','')
            page_size = each.get('PageSize','')
            page_number = page_no
            complete_records = int(page_number) * int(page_size)
            if complete_records <= totalrecords:
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
            evidya['state_name'] = state_name
            evidya['district_name'] = district_name
            evidya['total_records'] = str(totalrecords)
           
            yield evidya
        if next_page:
           form_dict["PageNo"] = next_page
           form_data["__CALLBACKPARAM"] = json.dumps(form_dict)
           
           yield FormRequest('http://schoolreportcards.in/SRC-New/AdvanceSearch/AdvanceSearch.aspx', callback = self.parse_next, formdata = form_data, meta = {'form_dict':form_dict , 'form_data':form_data, 'state_name':state_name, "district_name":district_name}, dont_filter=True)
        else:
            pass

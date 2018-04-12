import scrapy 
import json
import re
import os
import csv
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
from evidya.items import *
from pandas import read_csv
from generic_functions import *
from collections import OrderedDict
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class EvdmetaBrowsepdf(scrapy.Spider):
    name = 'evidyaloka_pdf_browse'
    start_urls = ['http://schoolreportcards.in/SRC-New/AdvanceSearch/AdvanceSearch.aspx']
    
    def clean_it(self, text):
        return text.strip().encode('utf-8').replace('\xc2\xa0', ' ')

    def __init__(self,state = '', **kwargs):
        with open("information.json", "r") as data: 
             super(EvdmetaBrowsepdf,self).__init__(**kwargs)
             self.counter = 0
             self.final_json = OrderedDict()
             self.state = state
             #self.district = district
             self.information = json.load(data)
             with open('total_page_stats.csv') as csvdata:
                    self.csv_data = csv.reader(csvdata)
                    self.one_state_data = [line for line in self.csv_data if line[-1]== self.state] #and line[8]==self.district
                    #self.one_state_data = [line for line in self.csv_data if line[-1]== self.state and line[8]==self.district]
                    self.all_schools = [ons[9] for ons in self.one_state_data ]
             
             self.headers = ['ref_url', 'School_Academic_Year', 'School_Code', 'School_Name', 'State', 'District', 'Block', 'Cluster', 'Village', 'Principal', 'Location', 'Pincode', 'School_Category', 'Lowest_Class', 'Highest_Class', 'Type_of_School', 'Management', 'Approachable_by_All_Weather_Road', 'Year_of_Establishment', 'Year_of_Recognition', 'Year_of_Upgradation_P_to_UP', 'Special_School_for_CWSN', 'Shift_School', 'Residential_School', 'Type_of_Residential_School', 'Pre_Primary_Section', 'Total_Students_Pre_Primary', 'Total_Teachers_Pre_Primary', 'Academic_Inspections', 'No_of_Visits_by_CRC_Coordinator', 'No_of_Visits_by_Block_Level_Officer','School_Development_Grant_Receipt','School_Development_Grant_Expenditure','School_Maintenance_Grant_Receipt', 'School_Maintenance_Grant_Expenditure', 'Regular_Teachers', 'Contract_Teachers', 'Graduate_or_above', 'Teachers_Male', 'Teachers_Female', 'Teachers_Aged_above', 'Head_Master', 'Trained_for_teaching_CWSN', 'Trained_in_use_of_Computer', 'Part_Time_Instructor', 'Teachers_Involved_in_Non_Teaching_Assignments', 'Avg_working_days_spent_on_Non_Tch_assignments', 'Teachers_with_Professional_Qualification', 'Teachers_Received_Inservice_Training', 'Medium_one', 'Medium_two', 'Medium_three', 'Status_of_School_Building', 'Boundary_wall', 'Classrooms_for_Teaching', 'Furniture_for_Students', 'Number_of_Other_Rooms', 'Classrooms_in_Good_Condition', 'Classrooms_Require_Minor_Repair', 'Classrooms_Require_Major_Repair', 'Separate_Room_for_HM', 'Electricity_Connection', 'Boys_Toilet_Seats_Total', 'Boys_Toilet_Seats_Functional', 'Girls_Toilet_Seats_Total', 'Girls_Toilet_Seats_Functional', 'CWSN_Friendly_Toilet', 'Drinking_Water_Facility', 'Drinking_Water_Functional', 'Library_Facility', 'No_of_Books_in_School_Library', 'Computer_Aided_Learning_Lab', 'Playground_Facility', 'Land_available_for_Playground', 'No_of_Computers_Available', 'No_of_Computers_Functional', 'Medical_check', 'Ramp_for_Disabled_Needed', 'Ramp_Available', 'Hand_Rails_for_Ramp', 'Classroom_Required_Major_Repair', 'Teachers_with_Prof_Qualification', 'Muslim_Girls_to_Muslim_Enrolment', 'Repeaters_to_Total_Enrolment', 'Change_in_Enrolment_over_Previous_Year', 'SC_Girls_to_SC_Enrolment', 'ST_Girls_to_ST_Enrolment', 'Pupil_Teacher_Ratio', 'Student_Classroom_Ratio', 'Girls_Enrolment', 'Muslim_Students', 'SC_Students', 'ST_Students', 'OBC_Enrolment']
             self.file_name = "%s%s" % (self.state.replace(' ', '_'), '.csv')     # self.file_name = "%s%s" % (self.state, '.csv')
             self.csv_file = self.is_path_file_name(self.file_name)
             self.csv_file.writerow(self.headers)
             dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        with open(self.file_name.replace('.csv', '.json'), 'w+') as fin:
            json.dump(self.final_json, fin)

    def is_path_file_name(self, excel_file_name):
        if os.path.isfile(excel_file_name):
                os.system('rm %s' % excel_file_name)
        oupf = open(excel_file_name, 'ab+')
        todays_excel_file = csv.writer(oupf)
        return todays_excel_file


    def parse(self, response):
        sel = Selector(response)
        view_state = ''.join(sel.xpath('//input[@name="__VIEWSTATE"]/@value').extract())
        generator_view = ''.join(sel.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract())
        for each_school_code in self.all_schools:
                print each_school_code
                
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Connection': 'keep-alive',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                }

                params = (
                    ('T', '1'),
                    ('AY', '2016-17'),
                    ('cmbschool', each_school_code ),
                    ('RT', '1'),
                )
                url = 'http://schoolreportcards.in/SRC-New/ReportCard/ViewReport.aspx?T=1&AY=2016-17&cmbschool='+str(each_school_code).strip()+'&RT=1'
                print url
                yield Request(url, headers=headers, callback = self.parse_next)

    def parse_next(self, response): 
        data = ''.join(response.xpath('//script[contains(text(), "writeWidget")]/text()').extract())
        html = ''.join(re.findall('content(.*)extraCssFileUrl', data))
        coo = html.replace('\\r\\n', '').replace('\\/', '/')
        coo = coo.strip("'").strip(":").strip("'").strip(',').strip("'")
        sel = Selector(text=coo)
        state =  ''.join(sel.xpath('//div[@id="STATNAME1"]//text()').extract()).strip()
        block = ''.join(sel.xpath('//div[@id="BLKNAME1"]//text()').extract()).strip()
        district = ''.join(sel.xpath('//div[@id="DistrictName1"]//text()').extract()).strip() 
        cluster = ''.join(sel.xpath('//div[@id="CLUNAME1"]//text()').extract()).strip().encode('utf-8').replace('\xc2\xa0', ' ')
        village =''.join(sel.xpath('//div[@id="VILNAME1"]//text()').extract()).strip()
        principal = ''.join(sel.xpath('//div[@id="HTCHNAME1"]//text()').extract()).strip().encode('utf-8').replace('\xc2\xa0','')
        
        acad_year =  ''.join(sel.xpath('//div[@id="ACYEAR1"]//text()').extract()).strip()
        school_code = ''.join(sel.xpath('//div[@id="SCHCD1"]//text()').extract()).strip()
        school_name = ''.join(sel.xpath('//div[@id="SCHNAME1"]//text()').extract()).strip().encode('utf-8').replace('\xc2\xa0', ' ')
        location = ''.join(sel.xpath('//div[@id="RURURBdesc1"]//text()').extract()).strip()               
        pincode = ''.join(sel.xpath('//div[@id="PINCD1"]//text()').extract()).strip()
        school_cate = ''.join(sel.xpath('//div[@id="SCHCAT1"]//text()').extract()).strip().encode('utf-8').replace('\xc2\xa0', ' ')
        lowest_class = ''.join(sel.xpath('//div[@id="LOWCLASS1"]//text()').extract()).strip()
        highest_class = ''.join(sel.xpath('//div[@id="HIGHCLASS1"]//text()').extract()).strip()
        school_type = ''.join(sel.xpath('//div[@id="SCHTYPEdesc1"]//text()').extract()).strip()
        management = ''.join(sel.xpath('//div[@id="SCHMGT1"]//text()').extract()).strip()
        road = ''.join(sel.xpath('//div[@id="APPROACHBYROADdesc1"]//text()').extract()).strip()
        est_year = ''.join(sel.xpath('//div[@id="ESTDYEAR1"]//text()').extract()).strip()
        reg_year = ''.join(sel.xpath('//div[@id="YORG1"]//text()').extract()).strip()
        upgrade = ''.join(sel.xpath('//div[@id="YOU1"]//text()').extract()).strip()
        cwsn_spl = ''.join(sel.xpath('//div[@id="CWSNSCHYNdesc1"]//text()').extract()).strip()
        shift_school = ''.join(sel.xpath('//div[@id="SCHSHIYNdesc1"]//text()').extract()).strip()
        resi_school = ''.join(sel.xpath('//div[@id="SCHRESYNdesc1"]//text()').extract()).strip()
        type_resi = ''.join(sel.xpath('//div[@id="ResiType1"]//text()').extract()).strip()
        pre_primary_sec = ''.join(sel.xpath('//div[@id="PPSECYNdesc1"]//text()').extract()).strip()
        pre_students = ''.join(sel.xpath('//div[@id="PPSTUDENT1"]//text()').extract()).strip()
        total_teachers = ''.join(sel.xpath('//div[@id="PPTEACHER1"]//text()').extract()).strip()
        acad_inspections = ''.join(sel.xpath('//div[@id="NOINSPECT1"]//text()').extract()).strip()
        crc_visit = ''.join(sel.xpath('//div[@id="VISITSCRC1"]//text()').extract()).strip()
        officer_visit = ''.join(sel.xpath('//div[@id="VISITSBRC1"]//text()').extract()).strip()
        dev_receipt = ''.join(sel.xpath('//div[@id="CONTIR1"]//text()').extract()).strip()
        dev_expenditr = ''.join(sel.xpath('//div[@id="CONTIE1"]//text()').extract()).strip()
        maint_receipt = ''.join(sel.xpath('//div[@id="SCHMNTCGRANTR1"]//text()').extract()).strip()
        maint_expenditure = ''.join(sel.xpath('//div[@id="SCHMNTCGRANTE1"]//text()').extract()).strip()
        regular_teachrs = ''.join(sel.xpath('//div[@id="RegularTch1"]//text()').extract()).strip()
        contract_teachrs = ''.join(sel.xpath('//div[@id="TotContractTch1"]//text()').extract()).strip()
        graduate_teachrs= ''.join(sel.xpath('//div[@id="GRADABOVE1"]//text()').extract()).strip()
        male_teachrs = ''.join(sel.xpath('//div[@id="TCHMALE1"]//text()').extract()).strip()
        female_teachers= ''.join(sel.xpath('//div[@id="TCHFEMALE1"]//text()').extract()).strip()
        teach_age55 = ''.join(sel.xpath('//div[@id="TeachersAbove551"]//text()').extract()).strip()
        head_master = ''.join(sel.xpath('//div[@id="HEADTCHYN1"]//text()').extract()).strip()
        cwsn_trained = ''.join(sel.xpath('//div[@id="CWSNTCH1"]//text()').extract()).strip()
        comp_trained = ''.join(sel.xpath('//div[@id="CWSNTRTCH1"]//text()').extract()).strip()
        part_time_instruc = ''.join(sel.xpath('//div[@id="TCHPARTUPR1"]//text()').extract()).strip()
        non_teach = ''.join(sel.xpath('//div[@id="TCHINVLD1"]//text()').extract()).strip()
        avg_workg_days = ''.join(sel.xpath('//div[@id="AvgWorkDays1"]//text()').extract()).strip()
        prof_qual_teachrs = ''.join(sel.xpath('//div[@id="TCHWITHPROF1"]//text()').extract()).strip()
        inserv_training = ''.join(sel.xpath('//div[@id="TeachersInService1"]//text()').extract()).strip()
        medium_one = ''.join(sel.xpath('//div[@id="Medium11"]//text()').extract()).strip() 
        medium_two = ''.join(sel.xpath('//div[@id="Medium21"]//text()').extract()).strip()
        medium_three = ''.join(sel.xpath('//div[@id="Medium31"]//text()').extract()).strip()
        school_buildg = ''.join(sel.xpath('//div[@id="StatusSchBLD1"]//text()').extract()).strip()
        bound_wall = ''.join(sel.xpath('//div[@id="BNDRYWALLdesc1"]//text()').extract()).strip()
        class_rooms = ''.join(sel.xpath('//div[@id="CLSTEACHING2"]//text()').extract()).strip()
        furniture = ''.join(sel.xpath('//div[@id="FURNSTUYN2"]//text()').extract()).strip()
        other_rooms = ''.join(sel.xpath('//div[@id="OTHGOOD2"]//text()').extract()).strip()
        class_good_cond = ''.join(sel.xpath('//div[@id="CLGOOD2"]//text()').extract()).strip()
        minor_repair = ''.join(sel.xpath('//div[@id="CLMINOR2"]//text()').extract()).strip()
        major_repair = ''.join(sel.xpath('//div[@id="CLMAJOR2"]//text()').extract()).strip()
        hm = ''.join(sel.xpath('//div[@id="HMROOMYNDESC2"]//text()').extract()).strip()
        elec_connection = ''.join(sel.xpath('//div[@id="ELECTRICYNDESC2"]//text()').extract()).strip()
        boys_toilet_seat_total = ''.join(sel.xpath('//div[@id="TOILETB2"]//text()').extract()).strip()
        boys_toilet_seat_func = ''.join(sel.xpath('//div[@id="BoysToiletFunctional2"]//text()').extract()).strip()
        girls_toilet_seat_total = ''.join(sel.xpath('//div[@id="TOILETG2"]//text()').extract()).strip()
        girls_toilet_Seat_func = ''.join(sel.xpath('//div[@id="GirlsToiletFunctional2"]//text()').extract()).strip()
        cwsn_toilet = ''.join(sel.xpath('//div[@id="IsCWSNToilet1"]//text()').extract()).strip() 
        drinkg_water = ''.join(sel.xpath('//div[@id="WATERDESC2"]//text()').extract()).strip().encode('utf-8').replace('\u00a0',' ')
        drinkg_water_func = ''.join(sel.xpath('//div[@id="WaterFunctional2"]//text()').extract()).strip()
        library_facility = ''.join(sel.xpath('//div[@id="LIBRARYYNDESC2"]//text()').extract()).strip()
        books_in_lib = ''.join(sel.xpath('//div[@id="BOOKINLIB2"]//text()').extract()).strip()
        comptr_lab = ''.join(sel.xpath('//div[@id="CAL1"]//text()').extract()).strip()
        play_grnd = ''.join(sel.xpath('//div[@id="PGROUNDYNDESC2"]//text()').extract()).strip()
        land_for_playgrnd = ''.join(sel.xpath('//div[@id="LandPGr2"]//text()').extract()).strip()
        comptr_available = ''.join(sel.xpath('//div[@id="COMPUTER2"]//text()').extract()).strip()
        comp_funct = ''.join(sel.xpath('//div[@id="ComputersFunctional2"]//text()').extract()).strip()
        medical_check = ''.join(sel.xpath('//div[@id="MEDCHKYNDESC2"]//text()').extract()).strip()
        ramp_disabld_needed = ''.join(sel.xpath('//div[@id="RampsNeeded2"]//text()').extract()).strip()
        ramp_avail = ''.join(sel.xpath('//div[@id="RampsAvailable2"]//text()').extract()).strip()
        hand_rails = ''.join(sel.xpath('//div[@id="HandrailF2"]//text()').extract()).strip()
        class_req_repair = ''.join(sel.xpath('//div[@id="CLRQUMJR1"]//text()').extract()).strip()
        prof_qual_teach = ''.join(sel.xpath('//div[@id="TCHPROFQUA1"]//text()').extract()).strip()
        muslim_enroll_percnt = ''.join(sel.xpath('//div[@id="MUSGIRLS1"]//text()').extract()).strip()
        total_enrol_repetrs = ''.join(sel.xpath('//div[@id="REPTOTOTE1"]//text()').extract()).strip()
        change_in_enrol = ''.join(sel.xpath('//div[@id="ChangeInEnrolmentPreYear1"]//text()').extract()).strip()
        sc_grls_enrol = ''.join(sel.xpath('//div[@id="SCGirls1"]//text()').extract()).strip()
        st_girls_enrol = ''.join(sel.xpath('//div[@id="STGIRLS1"]//text()').extract()).strip()
        pupil_teachr_ratio = ''.join(sel.xpath('//div[@id="PTR1"]//text()').extract()).strip()
        studnt_classrm_ratio = ''.join(sel.xpath('//div[@id="SCR1"]//text()').extract()).strip() 
        girl_enrol_percent = ''.join(sel.xpath('//div[@id="Girls1"]//text()').extract()).strip()
        muslim_stud_percent = ''.join(sel.xpath('//div[@id="MusENR1"]//text()').extract()).strip()
        sc_stud_percent = ''.join(sel.xpath('//div[@id="SCStudents1"]//text()').extract()).strip()
        st_stud_percent = ''.join(sel.xpath('//div[@id="STSTUDENTS1"]//text()').extract()).strip()
        obc_enrol_percent = ''.join(sel.xpath('//div[@id="OBCENR1"]//text()').extract()).strip() 
        values = [response.url,  acad_year ,  school_code,  school_name,  state  ,  district ,  block ,  cluster ,  village,  principal,  location ,   pincode ,  school_cate ,  lowest_class  ,  highest_class ,  school_type ,  management ,  road,  est_year,  reg_year,  upgrade,  cwsn_spl ,  shift_school,  resi_school,  type_resi,  pre_primary_sec,  pre_students,  total_teachers,  acad_inspections,  crc_visit, officer_visit,  dev_receipt,  dev_expenditr,  maint_receipt,  maint_expenditure,  regular_teachrs ,  contract_teachrs ,  graduate_teachrs,  male_teachrs ,  female_teachers,  teach_age55,  head_master ,  cwsn_trained ,  comp_trained ,  part_time_instruc ,  non_teach ,  avg_workg_days ,  prof_qual_teachrs ,  inserv_training ,  medium_one ,  medium_two ,  medium_three ,  school_buildg ,  bound_wall,  class_rooms,  furniture,  other_rooms,  class_good_cond,  minor_repair ,  major_repair,  hm,  elec_connection ,  boys_toilet_seat_total ,  boys_toilet_seat_func ,  girls_toilet_seat_total ,  girls_toilet_Seat_func ,  cwsn_toilet  ,  drinkg_water ,  drinkg_water_func ,  library_facility ,  books_in_lib ,  comptr_lab ,  play_grnd ,  land_for_playgrnd ,  comptr_available ,  comp_funct ,  medical_check ,  ramp_disabld_needed ,  ramp_avail ,  hand_rails ,  class_req_repair ,  prof_qual_teach ,  muslim_enroll_percnt ,  total_enrol_repetrs ,  change_in_enrol ,  sc_grls_enrol ,  st_girls_enrol ,  pupil_teachr_ratio ,  studnt_classrm_ratio ,  girl_enrol_percent ,  muslim_stud_percent ,  sc_stud_percent ,  st_stud_percent ,  obc_enrol_percent]
        mydict = OrderedDict()
        for head, valu in zip(self.headers, values):
            mydict.update({head:valu})
        self.final_json[self.counter] = mydict
        self.counter += 1
        values = [normalize(i) for i in values]

        self.csv_file.writerow(values)

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field

class EvidyaItem(scrapy.Item):
    ref_url = Field()
    School_Academic_Year = Field()
    School_Code = Field()
    School_Name = Field()
    State = Field()
    District = Field()
    Block = Field()
    Cluster = Field()
    Principal = Field()
    Village = Field()
    Location = Field()
    Pincode = Field()
    School_Category = Field()
    Lowest_Class = Field()
    Highest_Class = Field() 
    Type_of_School = Field()
    Management = Field()
    Approachable_by_All_Weather_Road = Field()
    Year_of_Establishment = Field()
    Year_of_Recognition = Field()
    Year_of_Upgradation_P_to_UP = Field()
    Special_School_for_CWSN = Field()
    Shift_School = Field()
    Residential_School = Field()
    Type_of_Residential_School = Field()
    Pre_Primary_Section = Field()
    Total_Students_Pre_Primary = Field()
    Total_Teachers_Pre_Primary = Field()
    Academic_Inspections = Field()
    No_of_Visits_by_CRC_Coordinator = Field()
    School_Development_Grant_Receipt = Field()
    School_Development_Grant_Expenditure = Field()
    School_Maintenance_Grant_Receipt = Field()
    School_Maintenance_Grant_Expenditure = Field()
    Regular_Teachers = Field()
    Contract_Teachers = Field()
    Graduate_or_above = Field()
    Teachers_Male = Field()
    Teachers_Female = Field()
    Teachers_Aged_above = Field()
    Head_Master = Field()
    Trained_for_teaching_CWSN = Field()
    Trained_in_use_of_Computer = Field()
    Part_Time_Instructor = Field()
    Teachers_Involved_in_Non_Teaching_Assignments = Field()
    Avg_working_days_spent_on_Non_Tch_assignments = Field()
    Teachers_with_Professional_Qualification = Field()
    Teachers_Received_Inservice_Training = Field()
    Medium_one = Field()
    Medium_two = Field()
    Medium_three = Field()
    Status_of_School_Building = Field()
    Boundary_wall = Field()
    Classrooms_for_Teaching = Field()
    Furniture_for_Students = Field()
    Number_of_Other_Rooms = Field()
    Classrooms_in_Good_Condition = Field()
    Classrooms_Require_Minor_Repair = Field()
    Classrooms_Require_Major_Repair = Field()
    Separate_Room_for_HM = Field()
    Electricity_Connection = Field()
    Boys_Toilet_Seats_Total = Field()
    Boys_Toilet_Seats_Functional = Field()
    Girls_Toilet_Seats_Total = Field()
    Girls_Toilet_Seats_Functional = Field()
    CWSN_Friendly_Toilet = Field()
    Drinking_Water_Facility = Field()
    Drinking_Water_Functional = Field()
    Library_Facility = Field()
    No_of_Books_in_School_Library = Field()
    Computer_Aided_Learning_Lab = Field()
    Playground_Facility = Field()
    Land_available_for_Playground = Field()
    No_of_Computers_Available = Field()
    No_of_Computers_Functional = Field()
    Medical_check = Field()
    Ramp_for_Disabled_Needed = Field()
    Ramp_Available = Field()
    Hand_Rails_for_Ramp = Field()
    Classroom_Required_Major_Repair = Field()
    Teachers_with_Prof_Qualification = Field()
    Muslim_Girls_to_Muslim_Enrolment = Field()
    Repeaters_to_Total_Enrolment = Field()
    Change_in_Enrolment_over_Previous_Year = Field()
    SC_Girls_to_SC_Enrolment = Field()
    ST_Girls_to_ST_Enrolment = Field()
    Pupil_Teacher_Ratio = Field()
    Student_Classroom_Ratio = Field()
    Girls_Enrolment = Field()
    Muslim_Students = Field()
    SC_Students = Field()
    ST_Students = Field()
    OBC_Enrolment = Field()

      #pass 


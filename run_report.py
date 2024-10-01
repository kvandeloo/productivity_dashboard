import report_card
from report_card import Db
import datetime

def main():
    target_resources = ['Minnie Mouse'] #resource you want to compare against the group average
    #choose either resources_to_hide or resources_to_include when calculating the group average
    resources_to_include = ['Donald Duck','Mickey Mouse','Minnie Mouse','Bugs Bunny','Daffy Duck','Snoopy Dog','Tigger Tiger','Winnie Pooh']
    resources_to_hide = []
    #adjust the file_location path to the path where your report_card folder is now 
    file_location = r'C:\Users\mmouse\Desktop\python_projects\scripts\report_card'
    lookback_months = 12
    
    ##you should not need to adjust anything else
    query_folder = file_location + '\\queries'
    db = Db() 
    run_time_str = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    out_csv = file_location + '\\out_csv_' + run_time_str + '.csv'

    #query assumptions: resource_name (not lead_data_resource or reported_by), month_to_date
    categories = [ #only the first four items in this list will display in the plot
        {'query_file': 'data_rev_rec.sql','xlabel': '# Months Ago','ylabel': '$ (USD)','title': 'Monthly Services Rev Rec - Data Milestones by Resource', 'checkbox_include': 1},
        {'query_file': 'hdavs_per_project.sql','xlabel': '# Months Ago','ylabel': 'Average # HDAVs per Project','title': 'Average Number of HDAVs per project as Lead Data Resource','checkbox_include': 0}, 
        {'query_file': 'projects_touched_per_month.sql','xlabel': '# Months Ago','ylabel': '# Projects Worked On','title': 'Monthly Average Number of Projects Worked On','checkbox_include': 1},           
        {'query_file': 'tasks_total.sql','xlabel': '# Months Ago','ylabel': '# Total Tasks','title': 'Monthly Number of Tasks Completed by Resource','checkbox_include': 1},
        {'query_file': 'build_reviews.sql','xlabel': '# Months Ago','ylabel': '# Build Reviews','title': 'Monthly Build Reviews by Resource','checkbox_include': 1},
        {'query_file': 'on_time_task_percent.sql','xlabel': '# Months Ago','ylabel': 'Percent of Tasks Closed On Time','title': 'On Time Task Closure Percentage','checkbox_include': 1},
        {'query_file': 'cleanups.sql','xlabel': '# Months Ago','ylabel': '# Project Cleanups','title': 'Monthly Project Cleanups by Resource','checkbox_include': 0},
    ]
    #run
    report_card.report_card(db,query_folder,categories,lookback_months,out_csv,target_resources,resources_to_hide,resources_to_include)

if __name__ == '__main__':
    main()
import pypyodbc, datetime
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class Db(object):
    def __init__(self,server = 'server-name',database = 'database-name',username='username',password='password'):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def query_db(self, query):
        '''return all results from query as a dataframe'''
        connection_info = 'Driver={ODBC Driver 17 for SQL Server};' + 'Server=' + self.server  + ';Database=' + self.database + ';uid='+ self.username + ';pwd=' + self.password
        connection = pypyodbc.connect(connection_info)
        df = pd.read_sql(query,connection)
        return df

###################################################
def read_query_file(query_file):
    with open(query_file) as f:
        query = f.read()
    return query

def limit_data(df,resources_to_hide = [],resources_to_include = []):
    resources = list(df)
    tmp_resources_to_hide = []
    if len(resources_to_include) > 0:
        for resource in resources:
            if resource not in resources_to_include:
                tmp_resources_to_hide.append(resource)
    if len(resources_to_hide) > 0:  
        for resource in resources_to_hide:
            if resource not in tmp_resources_to_hide:
                tmp_resources_to_hide.append(resource)  
    new_df = df.copy()
    new_df = df.drop(tmp_resources_to_hide,axis = 1)
    return new_df

def add_average_col(df):
    df_with_avg = df.copy()
    df_with_avg['Group Average'] = df_with_avg.mean(axis=1)
    return df_with_avg

def get_resource_average(df,lookback_months,category_dict):
    df_with_avg = df.copy()
    rows_to_drop = []
    for row_name in df_with_avg.index:
        if row_name == 'month_to_date':
            rows_to_drop.append(row_name)            
        elif int(row_name) > lookback_months:
            rows_to_drop.append(str(row_name))
    df_with_avg = df_with_avg.drop(rows_to_drop)
    row_name = 'Average ' + category_dict['title']
    df_with_avg.loc[row_name] = df_with_avg.mean()
    df_avg = pd.DataFrame()
    df_avg = df_with_avg.loc[[row_name]]
    #drop group average
    df_avg = df_avg.drop(['Group Average'], axis = 1)
    df_avg.insert(0,'Checkbox Include', [category_dict['checkbox_include']])
    return df_avg

def format_plot(df,ax, xlabel,ylabel,title):
    df.plot.line(ax = ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return ax

def visualize_data(db,query_folder,category_dict,target_resources,resources_to_hide,resources_to_include,lookback_months,ax,viz = True):
    #run functions
    query_filepath = query_folder + '\\' + category_dict['query_file']
    query = read_query_file(query_filepath)
    df = db.query_db(query)
    df.set_index('resource_name', inplace=True)
    df = df.transpose() #rows to columns, columns to rows
    df = limit_data(df,resources_to_hide,resources_to_include)
    df = df.drop('month_to_date',axis=0) #remove current month from calculations and display
    df = add_average_col(df)
    #move avg row calculation to separate function
    avg_df = get_resource_average(df,lookback_months,category_dict)
    #drop all but the special resource from the plot
    columns_to_display = target_resources + ['Group Average']
    display_df = df.filter(columns_to_display,axis=1)
    if viz == True:
        ax = format_plot(display_df,ax,category_dict['xlabel'],category_dict['ylabel'],category_dict['title'])
    return ax, avg_df

def report_card(db,query_folder,categories,lookback_months,out_csv,target_resources,resources_to_hide = [],resources_to_include = []):
    resource_summary_df = pd.DataFrame()
    num_grid_columns = 3
    num_grid_rows = 3
    grid_column_index = 1
    gs = GridSpec(num_grid_rows,num_grid_columns)
    fig = plt.figure(figsize=(15,15))

    ##add list of people used to calculate the average in the display
    #resource_string = 'Resources in Group Average:\n'
    #resources_to_include_alpha = sorted(resources_to_include)
    #for resource in resources_to_include_alpha: #will not work if we use the resources_to_hide input parameter instead
    #    resource_string += '\n' + resource
    #fig.text(0.025,0.8,s=resource_string)
    
    #get data and create visualizations
    for i in range(len(categories)):
        category_dict = categories[i]
        grid_row_index = i
        if i < num_grid_rows: #only about 4 plots can reasonably display, and the last one will be a pie chart
            ax = fig.add_subplot(gs[grid_row_index,grid_column_index:])
            ax.invert_xaxis() #because we are measuring in months_ago and want to display data chronologically
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            viz = True
        else:
            viz = False
        category_ax,category_avg_df = visualize_data(db,query_folder,category_dict,target_resources,resources_to_hide,resources_to_include,lookback_months,ax,viz)
        resource_summary_df = pd.concat([resource_summary_df,category_avg_df])

    #write resource_summary_df to csv
    resource_summary_df = resource_summary_df.astype(float).round(2)
    print(resource_summary_df)
    resource_summary_df.to_csv(out_csv)

    #add resource summary pie chart
    pie_chart_query_index = 0 #use the first query in the input list for the pie chart
    ax = fig.add_subplot(gs[0,0])
    pie_chart_data = resource_summary_df.iloc[[pie_chart_query_index]].values.tolist()[0][1:] #turn df into list, then remove the checkbox include value
    pie_chart_labels = list(resource_summary_df.columns.values)[1:] #remove checkbox include header
    ax.pie(pie_chart_data,labels=pie_chart_labels,autopct="%1.1f%%",radius=1.5)
    ax.set_title('Avg. Rev Rec Distribution',y=1.2)
    

    #show visualizations
    #plt.tight_layout()
    fig.suptitle('Trends Over Time',fontsize=16)
    plt.subplots_adjust(hspace=0.5)
    plt.show()

# def main():
#     db = Db('d-sql-01','clarizen','pentaho','!H@rm0ny12345')
#     query_folder = r'C:\Users\kvandeloo\Desktop\python_projects\scripts\report_card\queries'
#     run_time_str = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
#     out_csv = r'C:\Users\kvandeloo\Desktop\python_projects\scripts\report_card\report_card_results\out_csv_' + run_time_str + '.csv'
#     #choose either resources_to_hide or resources_to_include
#     resources_to_hide = [] #['Tai Gunter','Liz Burzynski','Kate Cole','Jackie Amador']
#     resources_to_include = ['Lucas Crider','Isaiah Mumaw','James Goble','Ariane Boissonnas','Tom Nielsen']
#     lookback_months = 12

#     #query assumptions: resource_name (not lead_data_resource or reported_by), month_to_date
#     categories = [
#         {'query_file': 'data_rev_rec.sql','xlabel': '# Months Ago','ylabel': '$ (USD)','title': 'Monthly Services Rev Rec - Data Milestones by Resource', 'checkbox_include': 1},
#         {'query_file': 'tasks_total.sql','xlabel': '# Months Ago','ylabel': '# Total Tasks','title': 'Monthly Number of Tasks Completed by Resource','checkbox_include': 1},
#         {'query_file': 'on_time_task_percent.sql','xlabel': '# Months Ago','ylabel': 'Percent of Tasks Closed On Time','title': 'On Time Task Closure Percentage','checkbox_include': 1},
#         {'query_file': 'hdavs_per_project.sql','xlabel': '# Months Ago','ylabel': 'Average # HDAVs per Project','title': 'Average Number of HDAVs per project as Lead Data Resource','checkbox_include': 1}, 
#         {'query_file': 'projects_touched_per_month.sql','xlabel': '# Months Ago','ylabel': '# Projects Worked On','title': 'Monthly Average Number of Projects Worked On','checkbox_include': 1},   
#         {'query_file': 'build_reviews.sql','xlabel': '# Months Ago','ylabel': '# Build Reviews','title': 'Monthly Build Reviews by Resource','checkbox_include': 0},
#         {'query_file': 'cleanups.sql','xlabel': '# Months Ago','ylabel': '# Project Cleanups','title': 'Monthly Project Cleanups by Resource','checkbox_include': 0},
#     ]

#     report_card(db,query_folder,categories,lookback_months,out_csv,resources_to_hide,resources_to_include)

# if __name__ == '__main__':
#     main()
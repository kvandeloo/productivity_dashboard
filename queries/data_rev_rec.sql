SET NOCOUNT ON;
/*data_rev_rec (services and total)*/

drop table if exists #cte_hours
drop table if exists #lead_data_resource
drop table if exists #cte_hdav
drop table if exists #cte_ops
drop table if exists #project_summary

DECLARE @lookback_months INT;
SET @lookback_months = 12;

/*
...
SQL code removed to protect proprietary information
...
*/


 /*find resource who worked the most hours on a data milestone*/
SELECT cte_hours.*, ROW_NUMBER()OVER(PARTITION BY project_id ORDER BY reported_hours_total DESC) AS lead_data_resource
INTO #lead_data_resource
FROM #cte_hours cte_hours

/*get number of dollars per project*/
select 
p.project_id
,p.name
,p.services_rev_rec_dollars
,p.total_rev_rec_dollars
,p.Reported_By as lead_data_resource
,p.workstream
,p.months_ago
into #project_summary
from #lead_data_resource p
WHERE p.lead_data_resource = 1

/*monthly breakdown - sum of services rev rec per month*/
SELECT lead_data_resource as resource_name,
[0] as month_to_date /*excluded from average*/
,[1] as [1],[2] as [2],[3] as [3]
,[4] as [4],[5] as [5],[6] as [6]
,[7] as [7],[8] as [8],[9] as [9]
,[10] as [10],[11] as [11],[12] as [12]
,[13] as [13],[14] as [14],[15] as [15] /*excluded from average*/
FROM (SELECT services_rev_rec_dollars,months_ago,lead_data_resource from #project_summary) p
PIVOT (
SUM(services_rev_rec_dollars)
FOR
months_ago
IN ([0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15])
) AS pvt
ORDER BY lead_data_resource

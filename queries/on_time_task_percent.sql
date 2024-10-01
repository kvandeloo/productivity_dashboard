SET NOCOUNT ON;
SET ANSI_WARNINGS OFF;

drop table if exists #task_summary;
drop table if exists #monthly_on_time_closure_percent;

DECLARE @lookback_months INT;
SET @lookback_months = 12;
  
/*
...
SQL code removed to protect proprietary information
...
*/

/*monthly breakdown - percent of tasks closed on time each month*/
SELECT reported_by as resource_name
,[0] as month_to_date /*excluded from average*/
,[1] as [1],[2] as [2],[3] as [3]
,[4] as [4],[5] as [5],[6] as [6]
,[7] as [7],[8] as [8],[9] as [9]
,[10] as [10],[11] as [11],[12] as [12]
,[13] as [13],[14] as [14],[15] as [15] /*excluded from average*/
FROM (SELECT ontime_task_closure,months_ago,reported_by from #monthly_on_time_closure_percent) p
PIVOT (
AVG(ontime_task_closure)
FOR
months_ago
IN ([0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15])
) AS pvt

ORDER BY reported_by
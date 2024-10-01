SET NOCOUNT ON; 

DROP TABLE IF EXISTS #task_summary;

DECLARE @lookback_months INT;
SET @lookback_months = 12;

/*
...
SQL code removed to protect proprietary information
...
*/


/*monthly breakdown - number of tasks per month*/
SELECT reported_by as resource_name
,[0] as month_to_date /*excluded from average*/
,[1] as [1],[2] as [2],[3] as [3]
,[4] as [4],[5] as [5],[6] as [6]
,[7] as [7],[8] as [8],[9] as [9]
,[10] as [10],[11] as [11],[12] as [12]
,[13] as [13],[14] as [14],[15] as [15] /*excluded from average*/
FROM (SELECT task_id,months_ago,reported_by from #task_summary) p
PIVOT (
COUNT(task_id)
FOR
months_ago
IN ([0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15])
) AS pvt
ORDER BY reported_by

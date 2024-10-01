SET NOCOUNT ON;

drop table if exists #cte_hours;
drop table if exists #lead_data_resource;
drop table if exists #cte_hdav;
drop table if exists #cte_ops;
drop table if exists #aggregate;
drop table if exists #project_summary;

DECLARE @lookback_months INT;
SET @lookback_months = 12;

/*
...
SQL code removed to protect proprietary information
...
*/

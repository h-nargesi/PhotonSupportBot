select username
	, floor(time_left / 24) as left_days
	, mod(time_left, 24) as left_hours
	, round(data_left / 1024 / 1024 / 1024, 2) as giga_left
from (
	select *
		, greatest(0, timestampdiff(hour, now(), expiration)) as time_left
		, total_data - ifnull(data_usage, 0) as data_left
	from (
		select u.username, u.expiration
			, case when u.reset_type_data is null then null else u.total_data end as total_data
			, case when total_data is null then null else (
				select sum(acctinputoctets) + sum(acctoutputoctets) as data_usage
				from radacct d
				where d.username = u.username
			) end as data_usage
		from ph_v_all_users u
		where (@where)
		  and account_disabled = 0
	) u
) rep
;

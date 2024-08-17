select username
	, floor(time_left / 24) as left_days
	, mod(time_left, 24) as left_hours
	, to_gigabyte(data_left, 2) as giga_left
	, time_left as total_hour_left
from (
	select *
		, greatest(0, timestampdiff(hour, now(), expiration)) as time_left
		, total_data_limit - ifnull(data_usage, 0) as data_left
		, total_data_limit - ifnull(data_usage, 0) as data_left
	from (
		select u.username, u.expiration
			, case when u.reset_type_data is null then null else ifnull(u.total_data_limit, 0) end as total_data_limit
			, case when u.reset_type_data is null then null else (
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

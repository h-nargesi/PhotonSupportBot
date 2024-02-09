select username
	, floor(time_left / 24) as left_days
	, mod(time_left, 24) as left_hours
    , round(data_left / 1024 / 1024 / 1024, 2) as giga_left
from (
	select *
		, greatest(0, timestampdiff(hour, now(), expiration)) as time_left
		, greatest(0, total_data - data_usage) as data_left
	from ph_v_users_data_usage u
	where
	  and account_disabled = 0
) rep
;

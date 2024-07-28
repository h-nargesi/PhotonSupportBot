select username, round(data / 1024 / 1024 / 1024, 2) as data, time, days_to_use, type
from (
	select u.username, t.data, t.time, t.days_to_use, t.type
		, row_number() over(partition by t.permanent_user_id order by t.id desc) as ranking
	from top_ups t
	join permanent_users u on u.id = t.permanent_user_id
	where (@where)
) top
where ranking = 1
;

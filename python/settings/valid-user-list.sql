select u.username, u.clear_password
from ph_v_users_data_usage u
where u.valid_account = 1
;
select username
	, sum(acctinputoctets) + sum(acctoutputoctets) as data_usage
from radacct
where @where
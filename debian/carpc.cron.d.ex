#
# Regular cron jobs for the carpc package
#
0 4	* * *	root	[ -x /usr/bin/carpc_maintenance ] && /usr/bin/carpc_maintenance

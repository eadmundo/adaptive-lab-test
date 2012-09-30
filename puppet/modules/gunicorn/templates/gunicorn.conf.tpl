<% if startup -%>
start on <%= startup %>
<% end -%>
stop on runlevel [016]

expect daemon
respawn

<% envs.each do | key, value | -%>
env <%= key %>="<%= value %>"
<% end -%>

exec /sbin/start-stop-daemon \
		--start \
		--chdir "<%= site_root %>" \
		--chuid www-data:www-data \
		--exec "<%= site_root %>/.venv/bin/gunicorn" -- \
			--daemon \
			--name app \
			--workers 4 \
			--config gunicorn.conf \
			--log-file /var/log/gunicorn.log \
			'app:create_app()'

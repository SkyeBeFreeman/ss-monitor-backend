iptables -A OUTPUT -p tcp --sport 8080

iptables -L -v -n -x --line-numbers

Iptable -Z OUTPUT
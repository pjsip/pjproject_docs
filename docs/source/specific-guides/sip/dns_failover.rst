Implement DNS SRV failover
=========================================
Our DNS SRV failover support is only limited to TCP (or TLS)
:cpp:any:`connect()` failure, which in this case pjsip will automatically
retries the next server. But even then, there is no mechanism to flag that
a server has been failing, which means that the next request may try
the same server again and triggering the failover again.

What we've been suggesting is to implement the failover mechanism in the
application layer. In this case, the application queries the list of available
servers either with :cpp:any:`gethostbyname()`, DNS SRV, or by other means.
It then specifies which server to use by putting the IP address as
proxy parameter (i.e. Route header) in the account config. The mechanism to
test the wellness of a server and when to initiate the failover is totally
controlled by the application. The application can change which server to
use by changing the account proxy setting with :cpp:any:`pjsua_acc_modify()`.

# parseEmail
Scripts to parse header/body from spam/phishing email

## ToDo
- [x] implement python-whois 
- [x] get domain name from urls collected (module ttldextract not used, regex chosen)
- [x] check creation_date using whois module
- [ ] code with windows portability in mind (in progress)
- [ ] check with bs4 if lxml.parser is necessary or not (in progress: apparently not necessary)
- [ ] implement email.parser.Parser with body (not only header)
	- check how to retrieve header only
	- then code msg.get_payload() to retrieve email body
- [ ] implement Base64 body mail check and decode
	- regex: ^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$


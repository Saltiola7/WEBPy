SELECT * FROM scrupp4 WHERE scraping_notes = 'altmed-us-canada' AND email = '' AND (company_domain != '' OR website_1 != '' OR website_2 != '' OR website_3 != '') use this and also return the output so that in one column there are is key and every domain is listed in another. row with one key can have multiple domains so all the domains have to be listed in one column and have its corresponding key. the domains are in company_domain, website_1, website_2, website_3

to repeat I want columns key, domain
domain includes all the domains from any of these rows.
if there are multiple domains, there are many rows with same key


# Facebook-Miner

This project extracts Facebook page posts long with its comments and sub-comments using Graph API. It is the primary way to get data into and out of the Facebook platform. It's a low-level HTTP-based API that apps can use to programmatically query data, post new stories, manage ads, upload photos, and perform a wide variety of other tasks.

Before the Graph API can be accessed, a user token is required[7]. An access_token can be acquired from Facebook’s developer tools located at https://developers.facebook.com/tools/

Once acquired, an endpoint API can be access as follows:

curl -i -X GET \
 "https://graph.facebook.com/facebook/picture?redirect=false&access_token={valid-access-token-goes-here}"


The Graph API is named after the idea of a "social graph" — a representation of the information on Facebook. It's composed of:

•	nodes — basically individual objects, such as a User, a Photo, a Page, or a Comment
•	edges — connections between a collection of objects and a single object, such as Photos on a Page or Comments on a Photo
•	fields — data about an object, such as a User's birthday, or a Page's name

Typically, you use nodes to get data about a specific object, use edges to get collections of objects on a single object, and use fields to get data about a single object or each object in a collection. 

Company Page Data Structure

Each post by a company on their company page in Facebook is published on the main page accessible using the URL form http://www.facebook.com/<company_page_name>. There are variations on how content gets published on a company page. Some companies only allow authorized personnel to post content, while others are open to all users in Facebook.

Below is the structure of posts for a company page:
<pre>
	dsfsdf
</pre>
- Company A Page
-> Page Post by Company or Customer
	-> Page Post Comments
		-> Page Post Comment Sub-Comments
		...
		...
		...
	...
	...
...
-> Page Post by Company or Customer
	-> Page Post Comments
			-> Page Post Comment Sub-Comments
			...
		...
		...
		...
	...
	...
...

- Company B Page
	...
	...
...
- ...


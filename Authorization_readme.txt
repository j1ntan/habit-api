The authentication to the backend has been implemented using DRF authentication.

Login requires a POST request with a dict containing two fields, e.g.,
{
    "username":"XYZ", (This field should may be replaced by an email field, BUT at least one of these two must be present.)
    "password":"__12"
}

The response would be a dict containing two fields, "status" and "data". "status" is true only when the credentials provided are correct, while
data is a dict containing the user's token under the "token" field. This token must be saved and provided under the "Authorization" header of 
every subsequent POST request that is made in order to authenticate with the backend. The header has the following format:
"Authorization" : "token {token code without double quotes}"

Signup requires a dict containing 4 fields: username, password, retype_password, email.

Logout only requires the user's token as a header and returns a dict containing two fields: status(True if logout successful) and message(says
"Logout successful!" in case of success).
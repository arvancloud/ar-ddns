# ar-ddns
ArvanCloud Dynamic DNS Tool

# Brief
Some Times the origin servers don't have the static IP and their IP may change after a while.
With this tool the user can update DNS record in ArvanCloud DNS service automatically.

# Input
User API Token available in ArvanCloud panel

# Capabalities
* Set DNS Record 
* Update DNS Record

# Usage

<pre>
./ar-ddns.sh -k "API-KEY" \
             -d "yourDomain.com"   \
             -n "yourRecordName"   \
             -r "Record ID"

</pre>

# Example

./ar-ddns.sh -k d67f2e136a15 -d test.ir -n www -r 185520

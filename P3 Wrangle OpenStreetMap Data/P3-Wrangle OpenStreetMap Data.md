# OpenStreetMap Data Case Study

## Map Area

Bengaluru, Karnataka, India

- https://www.openstreetmap.org/node/3401391999
- http://metro.teczno.com/#bengaluru

This is my current living city, So I am interested in tweaking and getting insights from the data.

## Problems Encountered in the Map
These are the problems that I encountered after running the data.py

- Postal codes with different keys *("pincode", "postal_code", "post_code", "postcode")*
- Spaces between postal codes *("560 047")*
- Postal codes with less than 6 numbers *("560")*
- Phone numbers with spaces between them *("+9194 94 218169")*
- Phone numbers with hiphen between them *("+9194-94-218169")*
- Multiple phone numbers divided by `;` and `,` *("+9194 94 218169";"+9132 4343 3434")*
- Phone numbers with missing numbers *("+919494")*
- Some streets have full address instead of just street name *("Whitefield, Bangalore, Karnataka, India")*
- Abbreviations were used in many addresses *("Jn of Koramangala Rd")*

### Postal Codes
I changed all different keys of postal codes to pincode. I removed all spaces and hiphens between the numbers using regular expression. If the length of the pin code is less than 6 then ignore that tag.
```python
def update_pincode(pin):
  updated_pin = re.sub(r'\D', "", pin)
  if unicode(updated_pin).isnumeric() and len(updated_pin) == 6:
    return updated_pin
  else:
    return None
```
```python
if tag['key'] in PINNAMES:
	tag['key'] = "pincode"
    new_pin = update_pincode(tag['value'])
    if new_pin:
      tag['value'] = new_pin
    else:
      tag = {}
      return tag
```

### Phone/Fax Numbers
I removed all spaces and hiphens between numbers. In some values multiple phone numbers are there separated by `;` and `,`. It returns only first phone number. If the length is less, ignore those values.
```python
def update_phone_fax(tagvalue):
  updated_phone = re.sub(r'\D', "", tagvalue)
  if len(updated_phone) < 12:
    return None
  else:
    updated_phone = "+" + updated_phone[0:12]
  return updated_phone
```

### Street address
I removed all the extra address information. For example `Whitefield, Bangalore, Karnataka, India` will change to `Whitefield`. Now we have short and good street names without all extra information. I've used a dictionary of all short forms with their correct values. This will replace all short names to their full ones. For example `Rd` to `Road` and `St` to `street` etc.
```python
def strip_long_address(addr):
  short_addr = ", Bangalore"
  long_addr = ", Bangalore, Karnataka, India"
  if addr.endswith(short_addr):
    addr = addr[:-len(short_addr)]
  if addr.endswith(long_addr):
    addr = addr[:-len(long_addr)]
  return addr
```
```python
def update_words(addr):
  words = addr.split()
  for w in range(len(words)):
    if words[w] in MAPPING.keys():
      words[w] = MAPPING[words[w]]
  addr = " ".join(words)
  return addr
```
## Data Overview
This section contains basic statistics about the dataset, the SQL queries used to gather them, and some additional ideas about the data in context.

### File Sizes
```
bengaluru-india.osm ........ 638MB
nodes.csv .................. 237.7MB
nodes_tags.csv ............. 2.3MB
ways.csv ................... 39.8MB
ways_tags.csv .............. 23.5MB
ways_nodes.csv ............. 84.5MB 
```
### Number of Nodes
```sql
SELECT Count(*) 
FROM   nodes; 
```
2839263
### Number of Ways
```sql
SELECT Count(*) 
FROM   ways; 
```
652228
### Number of Unique Users
```sql
SELECT Count(DISTINCT( e.uid )) 
FROM   (SELECT uid 
        FROM   nodes 
        UNION ALL 
        SELECT uid 
        FROM   ways) e; 
```
1503
### Top 10 Contributing Users
```sql
SELECT e.user, 
       Count(*) AS num 
FROM   (SELECT user 
        FROM   nodes 
        UNION ALL 
        SELECT user 
        FROM   ways) e 
GROUP  BY e.user 
ORDER  BY num DESC 
LIMIT  10; 
```
```
jasvinderkaur,126271
akhilsai,119383
premkumar,116224
saikumar,115160
shekarn,100025
vamshikrishna,94415
himalay,88558
PlaneMad,87905
himabindhu,87439
sdivya,85301
```
### Number of Users who have only one post
```sql
SELECT Count(*) 
FROM   (SELECT e.user, 
               Count(*) AS num 
        FROM   (SELECT user 
                FROM   nodes 
                UNION ALL 
                SELECT user 
                FROM   ways) e 
        GROUP  BY e.user 
        HAVING num = 1) u;
```
352

## Additional Data Exploration
### Top 10 appearing amenities
```sql
SELECT value, 
       Count(*) AS num 
FROM   nodes_tags 
WHERE  key = 'amenity' 
GROUP  BY value 
ORDER  BY num DESC 
LIMIT  10;
``` 
```
restaurant,1202
atm,664
bank,614
place_of_worship,601
fast_food,407
pharmacy,319
school,306
hospital,293
cafe,286
fuel,265
```
### Biggest Religion
```sql
SELECT nodes_tags.value, 
       Count(*) AS num 
FROM   nodes_tags 
       JOIN (SELECT DISTINCT( id ) 
             FROM   nodes_tags 
             WHERE  value = 'place_of_worship') i 
         ON nodes_tags.id = i.id 
WHERE  nodes_tags.key = 'religion' 
GROUP  BY nodes_tags.value 
ORDER  BY num DESC 
LIMIT  1; 
```
```
hindu,394
```
### Most Popular Cuisine
```sql
SELECT nodes_tags.value, 
       Count(*) AS num 
FROM   nodes_tags 
       JOIN (SELECT DISTINCT( id ) 
             FROM   nodes_tags 
             WHERE  value = 'restaurant') i 
         ON nodes_tags.id = i.id 
WHERE  nodes_tags.key = 'cuisine' 
GROUP  BY nodes_tags.value 
ORDER  BY num DESC 
LIMIT  10;
```
```
indian,223
chinese,71
vegetarian,60
regional,56
pizza,34
international,33
italian,19
Andhra,14
ice_cream,12
burger,9
```
### How many Kannada names are there?
```sql
SELECT Count(*) 
FROM   nodes_tags 
WHERE  key = "kn";
```
```
1953
```
### How many Junctions are in Bangalore?
```sql
SELECT Count(*) 
FROM   nodes_tags 
WHERE  key = "junction" 
       AND value = "yes"; 
```
```
99
```
In Bangalore, people are facing lot of problems commuting to work. Let's see how many bus stops and traffic signals are there in Bangalore.
### Number of Bus stops

```sql
SELECT Count(*) 
FROM   nodes_tags 
WHERE  key = "highway" 
       AND value = "bus_stop";
```

```
2993
```
### Number of Traffic signals
```sql
SELECT Count(*) 
FROM   nodes_tags 
WHERE  key = "highway" 
       AND value = "traffic_signal";
```
```
455
```
### Most common shops
```sql
SELECT value, 
       Count(*) AS num 
FROM   nodes_tags 
WHERE  key = 'shop' 
GROUP  BY value 
ORDER  BY num DESC 
LIMIT  10;
```
```
clothes,435
supermarket,302
bakery,224
convenience,176
jewelry,91
electronics,84
shoes,80
hairdresser,78
motorcycle,72
greengrocer,69
```
### Most common land uses
```sql
SELECT value, 
       Count(*) AS num 
FROM   nodes_tags 
WHERE  key = 'landuse' 
GROUP  BY value 
ORDER  BY num DESC 
LIMIT  10;
```
```
commercial,93
residential,29
industrial,11
retail,11
cemetery,3
recreation_ground,3
military,2
farm,1
landfill,1
office,1
```
### Which banks have more presence in Bangalore?
```sql
SELECT nodes_tags.value, 
       Count(*) AS num 
FROM   nodes_tags 
       JOIN (SELECT DISTINCT( id ) 
             FROM   nodes_tags 
             WHERE  value = 'bank') i 
         ON nodes_tags.id = i.id 
WHERE  nodes_tags.key = 'name' 
GROUP  BY nodes_tags.value 
ORDER  BY num DESC 
LIMIT  10;
```
```
"State Bank of India",47
"Canara Bank",45
"ICICI Bank",38
"HDFC Bank",30
"Axis Bank",29
"Corporation Bank",24
"State Bank of Mysore",24
"Vijaya Bank",21
"Syndicate Bank",18
"Karnataka Bank",16
```
I am seeing lot of KFCs near my place. Let's see how many branches KFC have in Bangalore

### KFC Branches
```sql
SELECT Count(*) 
FROM   nodes_tags 
WHERE  value = "kfc";
```
```
29
```
I am new to Bangalore. Let's see how many historic places are there to visit in Bangalore.

### Historic Places
```sql
SELECT Count(*) 
FROM   nodes_tags 
WHERE  key = "historic";
```
```
44
```

## Conclusion
Bangalore is a big cosmopolitan city. It has huge diversity in all aspects. People use different languages and names things differently. This might have posed some problem in data collecting. Even after cleaning, the data is incomplete. The data was collected by different users who follow different naming conventions, like for "pincode" people write "postcode", "postal_code" etc. Another problem is the language. Some people write in local language, for example "veedhi" for street etc. 

I also think that there should be a method and ranking to appreciate contributors. There should be a validation process to validate some data. For example some government websites have reliable data for pincodes. We can cross check the data with that reliable sources. The benefits of having ranking criteria is that we can recognise top contributors and it also acts as a motivator for other people to contribute more. The only limitation is that having robust and better ranking criteria, like stackoverflow. We can minimise errors by having a good validation process. The limitations are having reliable sources. For some information, we can rely on government websites. But for most of the data, we don't have any reliable sources. And creating good scalable validation mechanisms is not an easy task.

I am sure we can create good data by following the above procedures and can contribute more to OpenStreetMap.
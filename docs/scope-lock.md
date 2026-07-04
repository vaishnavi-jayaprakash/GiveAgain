In scope features:
->Individual to NGO donations only
->Government-registry-backed NGO verification — NGOs verify using their Darpan ID (NITI Aayog registry) and 80G/12A certificates, not a self-declared checkbox. This is the platform's core trust layer.
->Need based matching — NGOs post specific requirements (item 
type, quantity, deadline, plus category-specific details like size or working 
condition); donors get notified automatically when their item matches an active 
need.
->list an item in under a minute; no need to research or 
individually contact NGOs yourself. 
->donors receive a simple record of what they gave and 
to which NGO, and what impact it made, reinforcing repeat donation behavior.
-> pincode/locality-based matching and pickup 
scheduling, so collection is always logistically realistic.  
-> Category (fixed list, extensible): Clothing, Footwear, Books, Toys & Kids' Items, 
Furniture, Electronics, Kitchenware, Stationery, Sports Equipment, Other 
->Category-specific attributes (shown conditionally based on selected category):  
o Clothing/Footwear → size, gender (if relevant) 
o Books → title/author (optional ISBN autofill in phase 2) 
o Electronics → working condition (Working / Minor issues / For parts), age 
o Furniture → dimensions, material 
o Everything → universal fields: condition tag, quantity, description, photos 
Store category-specific fields as a flexible JSON attributes column rather than separate 
hardcoded columns per category — this avoids a schema migration every time you add a 
new category, and is a stronger technical talking point ("designed an extensible attribute 
system") than hardcoding fields.

Out of scope:
->Only one city
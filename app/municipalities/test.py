import philadelphia

#result = philadelphia.get_trash_zone('100 WOLF ST', 19148 )
result = philadelphia.get_trash_zone('6940 Sherwood Rd', 19151 )

if result:
    day, zone = result
    print day
    print zone
else:
    print "Failed to find address and matching zip code in Philadelphia"

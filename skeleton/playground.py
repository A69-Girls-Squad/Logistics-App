# Use case #1
# A customer visits the company office in Sydney on Oct 8th. They bring a package that needs to be delivered to Melbourne.
# An employee of the company records the customer’s contact info, weighs the package at 45kg and then checks
# for a suitable delivery route. The system reports that there are two routes:
# -	Brisbane (Oct 10th 06:00h) → Sydney (Oct 10th 20:00h) → Melbourne (Oct 11th 18:00h)
# -	Sydney (Oct 12th 06:00h) → Melbourne (Oct 12th 20:00h) → Adelaide (Oct 13th 15:00h)
# Both routes' trucks have free capacity, and the employee suggests the first one, as the package will arrive one day
# earlier. The customer agrees and the employee uses the system to add the delivery package to the first route and to
# update the package’s expected arrival time to Oct 11th 18:00h.

# SYD: 08/10 -> MEL
# customer_info
# weight=45

# check for a suitable delivery route

# system report:
# -	Brisbane (Oct 10th 06:00h) → Sydney (Oct 10th 20:00h) → Melbourne (Oct 11th 18:00h) - free capacity - MEL 11/10
# -	Sydney (Oct 12th 06:00h) → Melbourne (Oct 12th 20:00h) → Adelaide (Oct 13th 15:00h) - free capacity - MEL 12/10

# add the package to the first route

# update package estimated arrival time -> 11/10 18:00

'''
createroute BRI,SYD,MEL 2025-10-10T06:00
createroute SYD,MEL,ADL 2025-10-12T06:00
createpackage SYD MEL 45 johnsmith@gmail.com
searchroute 1
UnassignPackageToRoute 1 1
assignpackagetoroute 2 1
showpackages all
exit
'''


# Use case #2
# Many packages with total weight of 23000kg have gathered in the hub in Alice Springs and an employee of the company
# uses the system to create a route that leaves on Sep 12th 06:00h with the following stops:
# -	Alice Springs → Adelaide → Melbourne → Sydney → Brisbane
# The system determines the route distance to 4041km and calculates estimated arrival times for each of the locations
# based on a predefined average speed of 87km/h. The employee then finds a free truck that meets the required range and
# capacity and proceeds to bulk assign the packages to the newly created route by using the route id and the packages’ ids.

'''
createroute ASP,ADL,MEL,SYD,BRI 2025-09-12T06:00
searchtruck 3
assigntrucktoroute 1001 3
showpackages all
bulkassignpackages 3 2 4
exit
'''

# Use case #3
# A manager at the company uses the system to find information about all delivery routes in progress. The system
# responds with information that contains each route’s stops, delivery weight, and the expected current stop based on
# the time of the day.

'''
settime 2025-02-23T06:30
createroute ASP,ADL,MEL,SYD,BRI 2025-02-25T00:17
showroutesinprogress
'''

# Use case #4
# A supervising employee uses the system to view information about each package that is not yet assigned to a delivery
# route. The system responds with a list of packages containing their IDs and locations

'''
showpackages assigned
'''

# Use case #5
# A customer contacts the office to request information about their package. The customer provides the id that they
# received when the package was created, and an employee enters the package id in the system. It responds with
# detailed information which is then emailed to the customer.

'''
sendpackageinfotocustomer 1
'''


# ALL INPUT
'''
createroute BRI,SYD,MEL 2025-10-10-06:00
createroute SYD,MEL,ADL 2025-10-12-06:00
createpackage SYD MEL 45 johnsmith@gmail.com
searchroute 1
assignpackagetoroute 1 1
UnassignPackageToRoute 1 1
showpackages all
createroute ASP,ADL,MEL,SYD,BRI 2025-09-12T06:00
searchtruck 1
assigntrucktoroute 1001 2
showpackages all
bulkassignpackages 3 2 4
createroute ASP,ADL,MEL,SYD,BRI 2025-02-25T00:17
showroutesinprogress
showpackages assigned
ShowPackageCommand
exit
'''
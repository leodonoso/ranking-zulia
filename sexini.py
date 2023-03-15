from datetime import datetime

lucina = 'Jun 25th, 2022'
sucol = 'Oct 23rd, 2022'
panter = 'Jul 24th, 2022'
bowser = 'Sep 18th, 2022'

suki = sucol.split(' ')

num = ''

for sech in suki[1]:
    if sech.isdigit():
        num = num + sech

suki[1] = num

awatus = ' '.join(suki)

wikiti = datetime.strptime(awatus, '%b %d %Y')

print(wikiti)


# sex = datetime.strptime(gaystring, '%b %dth, %Y')

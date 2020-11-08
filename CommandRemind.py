import LogTools as LT
import datetime as DT

logtag = 'CommandRemind: '

async def entry(cmdArgs, message):

    if len(cmdArgs) < 2:
        await message.channel.send('Invalid format, give at least [hh:mm time to wait] [reminder text]')
        return 
    
    # date [date] [clock time]
    if cmdArgs[0] == 'date':
        if len(cmdArgs) < 4:
            await message.channel.send('''Invalid format. Use "remind date [mm/dd/yyyy] [hh:mm] [reminder text]"''')
            return
        dateArg = cmdArgs[1]
        clocktimeArg = cmdArgs[2]
        #await remindDate(dateArg, clocktimeArg, ' '.join(cmdArgs[3:]), message)
        await createReminder('date', dateArg, clocktimeArg, ' '.join(cmdArgs[3:]), message)

    # time [clock time]
    elif cmdArgs[0] == 'time':
        if len(cmdArgs) < 3:
            await message.channel.send('''Invalid format. Use "remind time [hh:mm] [reminder text]"''')
        clocktimeArg = cmdArgs[1]
        #await remindTime(clocktimeArg, ' '.join(cmdArgs[2:]), message)
        await createReminder('clocktime', None, clocktimeArg, ' '.join(cmdArgs[2:]), message)

    # [time in hr:min]
    else:
        timeArg = cmdArgs[0]
        await remindRaw('time', None, timeArg, ' '.join(cmdArgs[1:]), message)


async def remindDate(dateStr, clocktimeStr, text, message):
    dateInt = []
    clocktimeInt = []
    # TODO Cut/format into useable date
    # Date formats to accpet:
    # 0(0)/0(0)/00(00), 0(0)-0(0)-00(00)
    # Time formats to accept:
    # 0(0):00(am/pm)
    dateStr = dateStr.replace('/', '-')
    dateStr = dateStr.split('-')
    for s in dateStr:
        dateInt.append(int(s)) # month, day, year, in ints
    if checkDateValid(dateInt) == False:
        await message.channel.send('Invalid date format')
        return
    # Now have valid dateInt array of [m,d,y] 
    
    minFlag = ':' in clocktimeStr
    ampmFlag = ('pm' in clocktimeStr) or ('am' in clocktimeStr)
    
    if ampmFlag:
        ampm = clocktimeStr[-2:]
        clocktimeStr = clocktimeStr[:-2]
        
    clocktimeStr = clocktimeStr.split(':')
    if minFlag == False:
        clocktimeStr.append('00')

    for s in clocktimeStr:
        clocktimeInt.append(int(s)) # hour, minute
    if checkClocktimeValid(clocktimeInt, ampm) == False:
        await message.channel.send('Invalid time format')
        return
    if ampmFlag and ampm == 'pm': # Process adding 12 hours if PM is specified
        if clocktimeInt[0] == 12:
            clocktimeInt[0] = 0
        else:
            clocktimeInt[0] += 12
    # Now have valid clocktimeInt array of [h,m] CONVERTED TO MILITARY BECAUSE IM NOT DEALING WITH AMPM
    
    await createReminder(dateInt, clocktimeInt, text, message)
 
async def remindTime(clocktimeStr, text, message):
    clocktimeInt = []
    
    minFlag = ':' in clocktimeStr
    ampmFlag = ('pm' in clocktimeStr) or ('am' in clocktimeStr)
    
    if ampmFlag:
        ampm = clocktimeStr[-2:]
        clocktimeStr = clocktimeStr[:-2]
        
    clocktimeStr = clocktimeStr.split(':')
    if minFlag == False:
        clocktimeStr.append('00')

    for s in clocktimeStr:
        clocktimeInt.append(int(s)) # hour, minute
    if checkClocktimeValid(clocktimeInt, ampm) == False:
        await message.channel.send('Invalid time format')
        return
    if ampmFlag and ampm == 'pm': # Process adding 12 hours if PM is specified
        if clocktimeInt[0] == 12:
            clocktimeInt[0] = 0
        else:
            clocktimeInt[0] += 12
    # Now have valid clocktimeInt array of [h,m] CONVERTED TO MILITARY BECAUSE IM NOT DEALING WITH AMPM

async def remindRaw(timeStr, text, message):
    pass 
    
async def createReminder(rType, dateArg, timeArg, text, message):
    timeInt = []
    clocktimeInt = []
    dateInt = []
    
    if rType == 'clocktime' or rType == 'date':

        minFlag = ':' in timeArg
        ampmFlag = ('pm' in timeArg) or ('am' in timeArg)
        
        if ampmFlag:
            ampm = timeArg[-2:]
            timeArg = timeArg[:-2]
            
        timeArg = timeArg.split(':')
        if minFlag == False:
            timeArg.append('00')
    
        for s in timeArg:
            clocktimeInt.append(int(s)) # hour, minute
        if checkClocktimeValid(timeArg, ampm) == False:
            await message.channel.send('Invalid time format')
            return
        if ampmFlag and ampm == 'pm': # Process adding 12 hours if PM is specified
            if clocktimeInt[0] == 12:
                clocktimeInt[0] = 0
            else:
                clocktimeInt[0] += 12
        # Now have valid clocktimeInt array of [h,m] CONVERTED TO MILITARY BECAUSE IM NOT DEALING WITH AMPM

    if rType == 'date':

        # TODO Cut/format into useable date
        # Date formats to accpet:
        # 0(0)/0(0)/00(00), 0(0)-0(0)-00(00)
        # Time formats to accept:
        # 0(0):00(am/pm)
        dateArg = dateArg.replace('/', '-')
        dateArg = dateArg.split('-')
        for s in dateArg:
            dateInt.append(int(s)) # month, day, year, in ints
        if checkDateValid(dateInt) == False:
            await message.channel.send('Invalid date format')
            return
        # Now have valid dateInt array of [m,d,y]
    
    # Raw timer hours to add
    if rType == 'time':

        minFlag = ':' in timeArg
        
        timeArg = timeArg.split(':')
        if minFlag == False:
            timeArg.append('00')
        for s in timeArg:
            timeInt.append(int(s))
        if checkTimeValid(timeArg) == False:
            await message.channel.send('Invalid timer format')
            return
    
    
    # Calculate date/time    
#    if rType == 'date':
        
#    elif rType == 'clocktime':
        
#    elif rType == 'time':
        
#    else:
#        LT.Log('Error with rType in createReminder()', logtag)
#        return
    
    
    
    
def checkDateValid(dateIntArray):
    if len(dateIntArray) != 3:
        return False
    year = dateIntArray[2]
    day = dateIntArray[1]
    month = dateIntArray[0]
    if day < 0:
        return False
    if month in [1,3,5,7,8,10,12] and day > 31:
        return False
    if month in [4,6,9,11] and day > 30:
        return False
    if month == 2:
        if year%4 and day > 29:
            return False
        elif day > 28:
            return False
    if DT.datetime.now().date().year > year:
        return False
            
    return True

def checkClocktimeValid(clocktimeIntArray, ampmStr):
    if len(clocktimeIntArray) != 2:
        return False
    hour = clocktimeIntArray[0]
    minute = clocktimeIntArray[1]
    if 'pm' in ampm:
        hour += 12
        if hour == 24:
            hour = 0
        elif hour > 24:
            return False
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return False
    
    return True

def checkTimeValid(timeIntArray):
    if len(timeIntArray) != 2:
        return False
    hour = timeIntArray[0]
    minute = timeIntArray[1]
    if hour < 0 or minute < 0 or minute > 59:
        return False
    
    return True
    


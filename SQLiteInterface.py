import sqlite3
import LogTools as LT

dbConnection = None
dbConnectionInitialized = False

reminderTableExists= False

# Initialize
def Initialize():
    err = False
    global dbConnection
    dbConnection = sqlite3.connect('SpaceraceDatabase.db')
    
    if dbConnection == None:
        err = True
    else:
        dbConnectionInitialized = True
        c = dbConnection.cursor()
        
        try:
            # Create reminder table if it doesn't exist
            c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='reminders' ''')
            count = c.fetchone()[0]
            if count == 1:
                LT.Log('System', 'Internal', 'SQLiteInterface', 'Reminder table found')
            elif count == 0:
                LT.Log('System', 'Internal', 'SQLiteInterface', 'Reminder table not found, creating...')
                c.execute(''' CREATE TABLE reminders (userid integer, dyear integer, dmonth integer, dday integer, thour integer, tmin integer, remindermessage text) ''')
                dbConnection.commit()
            else:
                LT.Log('System', 'Internal', 'SQLiteInterface', 'Error finding/creating reminder table')
                err = True
        except Exception:
            dbConnectionInitialized = False
            err = True 
    return err

# Check that a reminder exists for the requesting person, return boolean related
def reminderExists(userId):
    try:
        c = dbConnection.cursor()
        c.execute(''' SELECT count(name) FROM reminders WHERE userid=? ''', [userId])
        return c.fetchone()[0] > 0
    except Exception:
        LT.Log('System', 'Internal', 'SQLiteInterface', 'Error with reminderExists(' + str(userId) + ')')
        return False

# Add an entry to a table given input parameters
# Given ([mm,dd,yyyy,hh,mm], userId)
# userId, year, month, day, hour, minute, reminder text
def addReminder(fullReminder, userId):
    pass
    
# Remove an entry to a table given input parameters
def removeReminder():
    pass


from datetime import date
def age(dob):
    todays_date = date.today()
    
    time_diff = todays_date -  dob
    age = time_diff.days/365
    
    return int(age)
        
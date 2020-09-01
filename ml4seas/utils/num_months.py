def num_months(start_date='1979-01-01', dates=None):
    """
    calculates the number of months elapsed since date 
    given a datetime index of list of datetimes ... 
    
    useful potentially for linear detrending ... 
    """
    from datetime import datetime
    start = datetime.strptime(start_date, "%Y-%m-%d") 
    elapsed = [((x.year - start.year) * 12 + (x.month - start.month)) for x in dates]
    return elapsed  

from datetime import datetime, timedelta

def calculate_date_range(argumentDate):
    if argumentDate == "aujourd'hui":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date
        end_date = date + timedelta(days=1)
    elif argumentDate == "semaineEnCours":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=7)
    elif argumentDate == "semaineGlissante":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date - timedelta(days=date.weekday() - 1)
        end_date = start_date + timedelta(days=8)
    elif argumentDate == "moisEnCours":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date.replace(day=1)
        end_date = start_date.replace(month=start_date.month + 1)
    elif argumentDate == "moisGlissant":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date.replace(day=1) - timedelta(days=1)
        end_date = start_date.replace(month=start_date.month + 1)
    else:
        raise ValueError("Invalid argumentDate")

    return start_date, end_date

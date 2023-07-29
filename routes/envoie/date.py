from datetime import datetime, timedelta

def process_argument_date(argumentDate, debutDate, finDate):
    print(argumentDate)
    if argumentDate == "aujourd'hui":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date
        end_date = date + timedelta(days=1)
        return start_date, end_date
    elif argumentDate == "semaineEnCours":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=7)
        return start_date, end_date
    elif argumentDate == "semaineGlissante":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date - timedelta(days=date.weekday() - 1)
        end_date = start_date + timedelta(days=8)
        return start_date, end_date
    elif argumentDate == "moisEnCours":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date.replace(day=1)
        end_date = start_date.replace(month=start_date.month + 1)
        return start_date, end_date
    elif argumentDate == "moisGlissant":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date.replace(day=1) - timedelta(days=1)
        end_date = start_date.replace(month=start_date.month + 1)
        return start_date, end_date
    elif argumentDate == "choixLibre":
        start_date = datetime.fromisoformat(debutDate) if debutDate else None
        end_date = datetime.fromisoformat(finDate) if finDate else None
        return start_date, end_date
    else:
        return None, None



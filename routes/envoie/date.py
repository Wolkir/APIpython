from datetime import datetime, timedelta

def process_argument_date(argumentDate, debutDate, finDate):
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
        # Utilisez le format exact des dates de la requête (YYYY-MM-DDTHH:MM:SS.sssZ)
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        try:
            start_date = datetime.strptime(debutDate, date_format)
            finDate_cleaned = finDate.strip()  # Supprimer les espaces en début et fin de chaîne
            print("finDate_cleaned:", finDate_cleaned)  # Ajoutez ce log pour voir la valeur de finDate_cleaned
            end_date = datetime.strptime(finDate_cleaned, date_format)
            return start_date, end_date
        except ValueError as e:
            print("Erreur lors de la conversion des dates:", e)
            return None, None
    else:
        return None, None


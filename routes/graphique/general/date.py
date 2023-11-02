from datetime import datetime, timedelta

def process_argument_date(debutDate, finDate):
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    try:
        start_date = datetime.strptime(debutDate, date_format)
        finDate_cleaned = finDate.strip()
        print("finDate_cleaned:", finDate_cleaned)
        end_date = datetime.strptime(finDate_cleaned, date_format)
        return start_date, end_date
    except ValueError as e:
        print("Erreur lors de la conversion des dates:", e)
        return None, None



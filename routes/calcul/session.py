from datetime import datetime, time

def determine_session(data):
    sessions = []
    for doc in data:
        opening_time = datetime.strptime(doc['dateAndTimeOpening'], "%Y-%m-%d %H:%M:%S.%f")
        if time(0, 0) <= opening_time.time() < time(7, 0):
            session_value = "AS"
        elif time(8, 0) <= opening_time.time() < time(12, 0):
            session_value = "LD"
        elif time(13, 0) <= opening_time.time() < time(15, 0):
            session_value = "NY"
        else:
            session_value = "ND"

        sessions.append(session_value)

    return sessions



from .sensor import sense, cleanup

def main():
    try:
        sense(on_sit_down, on_get_up)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

def on_sit_down():
    pass

last_session_start_time = None
def on_get_up():
    pass


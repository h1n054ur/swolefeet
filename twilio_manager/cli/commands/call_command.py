from twilio_manager.core.voice import make_call

def initiate_call(from_number, to_number, voice_url):
    """Initiate a voice call.
    
    Args:
        from_number (str): Caller's phone number
        to_number (str): Recipient's phone number
        voice_url (str): TwiML URL for call handling
        
    Returns:
        bool: True if call was initiated successfully, False otherwise
    """
    return make_call(from_number, to_number, voice_url)

def get_recordings():
    """Get list of call recordings.
    
    Returns:
        list: List of recording dictionaries
    """
    from twilio_manager.core.voice import get_recordings as fetch_recordings
    return fetch_recordings()

def delete_recording(recording_sid):
    """Delete a recording by its SID.
    
    Args:
        recording_sid (str): Recording SID
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    from twilio_manager.core.voice import delete_recording as remove_recording
    return remove_recording(recording_sid)

def handle_manage_recordings():
    """Handle recording management."""
    from twilio_manager.cli.menus.recordings_menu import RecordingsMenu
    RecordingsMenu().show()

def list_conferences():
    """Get list of active conferences.
    
    Returns:
        list: List of conference dictionaries
    """
    from twilio_manager.core.voice import get_conferences
    return get_conferences()

def join_conference(conference_sid, from_number):
    """Join a conference call.
    
    Args:
        conference_sid (str): Conference SID
        from_number (str): Phone number to join with
        
    Returns:
        bool: True if join was successful, False otherwise
    """
    from twilio_manager.core.voice import join_conference as join_conf
    return join_conf(conference_sid, from_number)

def end_conference(conference_sid):
    """End a conference call.
    
    Args:
        conference_sid (str): Conference SID
        
    Returns:
        bool: True if conference was ended successfully, False otherwise
    """
    from twilio_manager.core.voice import end_conference as end_conf
    return end_conf(conference_sid)

def handle_conference_calls():
    """Handle conference call management."""
    from twilio_manager.cli.menus.conference_menu import ConferenceMenu
    ConferenceMenu().show()

def handle_make_call_command():
    """Handle making a voice call."""
    from twilio_manager.cli.menus.call.call_menu import CallMenu
    CallMenu().show()

def calculate_call_metrics(yaml_data):
    """Calculate overtalk and silence percentages from conversation data."""
    
    total_call_duration = 0  # Tracks total call duration
    overtalk_duration = 0  # Tracks duration of overlapping speech
    silence_duration = 0  # Tracks duration of silence
    last_end_time = None  # Stores the end time of the last speaker's turn

    for i, entry in enumerate(yaml_data):
        start_time = entry["stime"]
        end_time = entry["etime"]
        total_call_duration += end_time - start_time  # Accumulate total conversation time

        # Detect Overtalk (When two people speak simultaneously)
        if last_end_time and start_time < last_end_time:
            overtalk_duration += last_end_time - start_time  # Count overlapping time

        # Detect Silence (Gap between two conversations)
        if last_end_time and start_time > last_end_time:
            silence_duration += start_time - last_end_time  # Count silent gaps

        last_end_time = end_time  # Update last end time for the next iteration

    # Avoid division by zero if total duration is 0
    if total_call_duration == 0:
        return 0, 0  

    # Calculate percentages
    silence_percentage = (silence_duration / total_call_duration) * 100  
    overtalk_percentage = (overtalk_duration / total_call_duration) * 100  

    return silence_percentage, overtalk_percentage

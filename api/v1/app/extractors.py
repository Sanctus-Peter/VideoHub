from urllib.parse import urlparse, parse_qs


def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.

    Args:
        url (str): The YouTube URL from which the video ID needs to be extracted.

    Returns:
        str or None: The extracted video ID if found, or None if the video ID could not be extracted.

    Examples:
        >>> extract_video_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        'dQw4w9WgXcQ'

        >>> extract_video_id('https://youtu.be/dQw4w9WgXcQ')
        'dQw4w9WgXcQ'

        >>> extract_video_id('https://www.youtube.com/playlist?list=PL1234567890')
        'PL1234567890'

    Explanation:
        This function extracts the video ID from various types of YouTube URLs.

        - For URLs of the format 'https://youtu.be/<video_id>', it simply returns the <video_id> part.
        - For URLs of the format 'https://www.youtube.com/watch?v=<video_id>',
                                    it extracts the <video_id> from the query parameters.
        - For URLs of the format 'https://www.youtube.com/watch/<video_id>',
                                    it splits the path and returns the <video_id> part.
        - For URLs of the format 'https://www.youtube.com/embed/<video_id>',
                                    it splits the path and returns the <video_id> part.
        - For URLs of the format 'https://www.youtube.com/v/<video_id>',
                                    it splits the path and returns the <video_id> part.
        - For URLs of the format 'https://www.youtube.com/playlist?list=<playlist_id>',
                                    it extracts the <playlist_id> from the query parameters.

        If the URL does not match any of the expected formats or the video ID cannot be extracted,
                                    the function returns None.
    """

    parsed_url = urlparse(url)

    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]

    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            p = parse_qs(parsed_url.query)
            return p['v'][0]

        if parsed_url.path[:7] == '/watch/':
            return parsed_url.path.split('/')[1]

        if parsed_url.path[:7] == '/embed/':
            return parsed_url.path.split('/')[2]

        if parsed_url.path[:3] == '/v/':
            return parsed_url.path.split('/')[2]

        if parsed_url.path[:9] == '/playlist':
            return parse_qs(parsed_url.query)['list'][0]

    return None

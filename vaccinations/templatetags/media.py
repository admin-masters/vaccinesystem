from django import template
from urllib.parse import urlparse, parse_qs, urlencode
import re
import time

register = template.Library()
_YT_ID = re.compile(r'^[A-Za-z0-9_-]{11}$')

def _extract_youtube_id(url: str) -> str | None:
    """
    Enhanced YouTube ID extraction
    """
    if not url or not isinstance(url, str):
        return None
    
    url = url.strip()
    
    # Remove tracking parameters and clean URL
    if '&' in url:
        url = url.split('&')[0]
    if '?' in url and 'v=' in url:
        url = url.split('?')[0] + '?' + url.split('?')[1]
    
    patterns = [
        r'(?:youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/shorts/)([A-Za-z0-9_-]{11})',
        r'youtube\.com/watch\?.*v=([A-Za-z0-9_-]{11})',
        r'youtube\.com/attribution_link\?.*v%3D([A-Za-z0-9_-]{11})',
        r'^([A-Za-z0-9_-]{11})$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            if _YT_ID.match(video_id):
                return video_id
    
    return None

@register.simple_tag(takes_context=True)
def youtube_embed(context, url: str) -> str:
    """
    Return YouTube embed URL - SIMPLIFIED to fix Error 153
    """
    try:
        if not url:
            return ""
            
        vid = _extract_youtube_id(url)
        if not vid:
            return ""
        
        # NO PARAMETERS - simplest approach to avoid Error 153
        embed_url = f"https://www.youtube.com/embed/{vid}"
        
        return embed_url
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"YouTube embed error: {str(e)}")
        return ""

@register.filter
def youtube_id(url: str) -> str:
    """Extract YouTube ID for debugging"""
    return _extract_youtube_id(url) or "INVALID"
"""
Context processors for accounts app
"""

def user_theme(request):
    """
    Add user theme and background to template context.
    """
    theme = 'default'
    background_mode = 'none'
    background_url = None

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        profile = request.user.profile
        theme = profile.theme
        background_mode = profile.background_mode

        # Handle background image based on mode
        if background_mode == 'custom' and profile.background_image:
            background_url = profile.background_image.url
        elif background_mode == 'random':
            # Get a random background from the internet
            # Using Lorem Picsum for high-quality random images
            import time

            # Use timestamp-based seed for randomization (changes every page load)
            seed = int(time.time() * 1000)

            # Lorem Picsum provides random placeholder images
            # Grayscale option for subtle backgrounds: &grayscale
            # Blur option for softer backgrounds: &blur=2
            background_url = f'https://picsum.photos/1920/1080?random={seed}'

    return {
        'user_theme': theme,
        'user_background_mode': background_mode,
        'user_background_url': background_url,
    }

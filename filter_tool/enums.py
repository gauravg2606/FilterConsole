FILTER_TYPES = (
    (1, ("STORY_FACE_MASKS")),
    (2, ("STORY_GUIDE")),
    (3, ("STORIES_STICKERS")),
    (4, ("TEXT_STORIES_STICKERS")),
    (5, ("TEXT_STORIES_BG")),
    (6, ("STORY_STK_REACTION")),
    (7, ("SO_FILES")),
    (8, ("BIN_FILES"))
)

FACE_FILTER_EFFECT_TYPES = (
    (None,("NONE")),
    ("mask", ("MASK")),
    ("action", ("ACTION")),
    ("filter", ("FILTER")),
)

PLATFORM_TYPES = (
    ('android', ("ANDROID")),
    ('ios', ("IOS")),
)

OPERATION_TYPES = (
    (0,("ADDITION")),
    (1,("REMOVAL")),
)

AVAILABILITY_STATUS = (
    (1,("AVAILABLE")),
    (0,("REMOVED")),
)

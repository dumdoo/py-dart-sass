class OutputStyles:
    EXPANDED = "expanded"
    COMPRESSED = "compressed"


class SourceMapOptions:
    NO_SOURCE_MAP = "--no-source-map"
    SOURCE_MAP_URLS = "--source-map-urls"
    EMBED_SOURCES = "--embed-sources"
    EMBED_SOURCE_MAP = "--embed-source-map"


class InputOutput:
    STDIN = "--stdin"
    INDENTED = "--indented"
    NO_INDENTED = "--no-indented"
    LOAD_PATH = "--load-path"
    NO_CHARSET = "--no-charset"
    CHARSET = "--charset"
    ERROR_CSS = "--error-css"
    NO_ERROR_CSS = "--no-error-css"
    UPDATE = "--update"


class OtherOptions:
    WATCH = "--watch"
    POLL = "--poll"
    STOP_ON_ERROR = "--stop-on-error"

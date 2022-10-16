import textwrap

import htmlmin.minify
import html.parser


GS = b'\x1d'
ESC = b'\x1b'

BOLD_ON = ESC + b'\x45\x01'
BOLD_OFF = ESC + b'\x45\x00'
LARGE_FONT = GS + b'\x21\x31'
NORMAL_FONT =  GS + b'\x21\x00'
ENABLE_CUSTOM_FONTS = ESC + b'\x25\x01'
DISABLE_CUSTOM_FONTS = ESC + b'\x25\x00'

TICKBOX_CHAR = b'A'
TICKBOX = (
    LARGE_FONT +
    ENABLE_CUSTOM_FONTS +
    TICKBOX_CHAR +
    DISABLE_CUSTOM_FONTS +
    NORMAL_FONT
)

WIDTH = 32


class EM5820():
    def print(self, html):
        compressed_html = htmlmin.minify.html_minify(html.replace('\n',''))
        parser = EM5820HTMLParser()
        parser.feed(compressed_html)
        return parser.result


class EM5820HTMLParser(html.parser.HTMLParser):

    def __init__(self):
        super(EM5820HTMLParser, self).__init__()
        self._result = b''
        self._printing_task = False

    @property
    def result(self):
        return self._result

    def handle_starttag(self, tag, attrs):
        if tag == 'strong':
            self._result += BOLD_ON
        elif tag == 'br':
            self._result += b'\n'
        elif tag == 'li':
            self._result += TICKBOX + b' '
            self._printing_task = True
        elif tag == 'html':
            # TODO: Init and register tick box here
            self._result += (b'-' * WIDTH) + b'\n\n'

    def handle_endtag(self, tag):
        if tag == 'strong':
            self._result += BOLD_OFF
        elif tag == 'li':
            self._result += b'\n'
            self._printing_task = False
        elif tag == 'html':
            self._result = self._result.strip() + b'\n\n' + (b'-' * WIDTH) + (b'\n' * 4)

    def handle_data(self, data):
        if data.strip() == '':
            return

        wrapped = data
        if self._printing_task:
            lines = textwrap.wrap(data, width=WIDTH - 8)
            wrapped = lines[0]
            if len(lines) > 1:
                wrapped += '...'
        else:
            if len(data) > WIDTH:
                wrapped = '\n'.join(textwrap.wrap(data, width=WIDTH))

        self._result += wrapped.encode()

"""Pre-publication privacy guard: no active forms or remote page resources."""
from html.parser import HTMLParser
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
class Audit(HTMLParser):
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        assert tag != 'form', 'Enquiry form must remain offline until privacy information is complete'
        refs = [a.get('src', ''), a.get('srcset', ''), a.get('action', '')]
        if tag == 'link' and a.get('rel') in ('stylesheet', 'preconnect', 'dns-prefetch', 'preload'):
            refs.append(a.get('href', ''))
        assert not any(re.search(r'https?:|^//', v) for v in refs), ('External resource', tag, refs)
for p in ROOT.rglob('*.html'):
    source = p.read_text()
    assert not re.search(r'clarity\.ms|laura@|directly to Laura', source, re.I), p
    Audit().feed(source)
for p in (ROOT / 'assets').rglob('*.css'):
    assert not re.search(r'url\([\s\"\x27]*(?:https?:|//)', p.read_text()), p
print('Passed: no active public forms, remote HTML/CSS resources, Clarity or personal contact details.')

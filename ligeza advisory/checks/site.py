"""Validate the static site's links, form labels, metadata and rebrand. No dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.references = []
        self.labels = []
        self.controls = []
        self.headings = 0
        self.canonicals = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        assert len(a) == len(attrs), (self.path, 'duplicate attribute', tag)
        if 'id' in a:
            assert a['id'] not in self.ids, (self.path, 'duplicate ID', a['id'])
            self.ids.add(a['id'])
        if tag == 'h1':
            self.headings += 1
        if tag == 'label' and 'for' in a:
            self.labels.append(a['for'])
        if tag in ('input', 'select', 'textarea') and a.get('type') != 'hidden' and 'hidden' not in a:
            self.controls.append(a.get('id'))
        for attr in ('href', 'src'):
            if a.get(attr):
                self.references.append(a[attr])
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a['href'])

pages = {p.resolve(): Page(p) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
links = 0
for path, page in pages.items():
    assert page.headings == 1, (path, 'expected one h1')
    assert all(control in page.labels for control in page.controls), (path, 'unlabelled form control')
    assert all(label in page.ids for label in page.labels), (path, 'label without control')
    noindex = 'noindex' in path.read_text()
    assert len(page.canonicals) == 1 or noindex, (path, 'missing canonical')
    assert all(url.startswith('https://ligezaadvisory.com/') for url in page.canonicals), path
    for reference in page.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            continue
        target = ((ROOT / unquote(url.path).lstrip('/')) if url.path.startswith('/') else (path.parent / unquote(url.path))).resolve() if url.path else path
        if target.is_dir():
            target /= 'index.html'
        assert target.is_file(), (path, 'missing target', reference)
        if url.fragment and target in pages:
            assert unquote(url.fragment) in pages[target].ids, (path, 'missing anchor', reference)
        links += 1
    for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>', path.read_text(), re.S):
        json.loads(data)
for path in ROOT.rglob('*'):
    if not path.is_file() or path.suffix not in {'.html', '.css', '.js', '.xml', '.txt'} or '.git' in path.parts:
        continue
    assert not re.search(r'ligeza\s*linguistics', path.read_text(), re.I), ('old brand', path)
for path in ROOT.rglob('*.css'):
    for ref in re.findall(r'url\([\"\']?([^\)\"\']+)', path.read_text()):
        if not urlsplit(ref).scheme:
            assert (path.parent / ref).is_file(), (path, 'missing CSS asset', ref)
for url in ET.parse(ROOT / 'sitemap.xml').getroot():
    location = url[0].text
    assert location.startswith('https://ligezaadvisory.com/'), location
    target = ROOT / urlsplit(location).path.lstrip('/')
    if target.is_dir():
        target /= 'index.html'
    assert target.resolve() in pages, location
assert 'Sitemap: https://ligezaadvisory.com/sitemap.xml' in (ROOT / 'robots.txt').read_text()
print(f'Passed: {len(pages)} pages, {links} local links, form labels, structured data, sitemap and brand references.')

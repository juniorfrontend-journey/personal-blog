# -*- coding: utf-8 -*-
"""Build blog cá nhân Jackethee — bản Decap CMS.
- Bài viết là file Markdown trong content/posts/*.md (frontmatter YAML + body
  Markdown), do Decap CMS ghi khi Đại ca thêm/sửa/xóa trong trang /admin.
- Đọc template Stitch: home.html, article.html, about.html
- Thay header/footer bằng bản chuẩn (nav đúng trang active, link thật)
- Ảnh nằm trong images/ (repo root), không hotlink Google
- Trang danh sách, trang giới thiệu, RSS, trang chủ (bài tiêu điểm + lưới bài)
Chạy local:  python3 build.py            (ghi ra thư mục site/)
Chạy trên CI: python3 build.py --out .   (ghi thẳng ra repo root để Vercel phục vụ)
"""
import argparse
import glob
import json
import os
import re
import shutil
import sys

import markdown as md_lib
import yaml

BASE = os.path.dirname(os.path.abspath(__file__))
STITCH = os.path.join(BASE, "stitch")
SITE = os.path.join(BASE, "site")
IMG_MAP = json.load(open(os.path.join(STITCH, "image-map.json"), encoding="utf-8"))
SITE_URL = "https://blog.jackethee.dev"

# ---------------------------------------------------------------- load posts
LEAD_CLS = "font-body-lg text-body-lg text-secondary leading-relaxed mb-6"
P_CLS = "font-body-md text-body-md text-secondary leading-relaxed mb-6"
P_LAST_CLS = "font-body-md text-body-md text-secondary leading-relaxed mb-8"
H2_CLS = ("font-headline-md text-headline-md text-on-surface tracking-tight "
          "mt-10 mb-4 pb-2 border-b border-surface-container-highest")
H3_CLS = "font-headline-sm text-headline-sm text-on-surface mt-8 mb-3"
QUOTE_CLS = ("my-8 p-4 pl-5 border-l-2 border-primary-container "
             "bg-surface-container-lowest rounded-r-lg")
QUOTE_TXT_CLS = "font-body-lg text-body-lg text-on-surface font-medium italic mb-1"
QUOTE_CITE_CLS = ("block font-label-sm text-label-sm text-secondary not-italic "
                  "uppercase tracking-wider")


def _numlist_cards(ol_html):
    """Biến <ol> markdown thành các thẻ đánh số kiểu NUM_LIST của template."""
    items = re.findall(r'<li>(.*?)</li>', ol_html, flags=re.DOTALL)
    out = ['<div class="space-y-4 my-6">']
    for i, li in enumerate(items, 1):
        m = re.match(r'\s*<strong>(.*?)</strong>\s*—\s*(.*)', li, flags=re.DOTALL)
        if m:
            head, body = m.group(1), m.group(2)
        else:
            head, body = '', li
        out.append(
            '<div class="flex items-start space-x-3.5 p-3.5 bg-surface-container-lowest '
            'border border-surface-container-highest rounded-lg">'
            '<span class="inline-flex items-center justify-center w-6 h-6 rounded '
            'bg-surface-container font-label-sm text-label-sm text-primary font-bold '
            'flex-shrink-0">' + str(i) + '</span><div>'
            '<h3 class="font-headline-sm text-headline-sm text-on-surface mb-0.5">'
            + head + '</h3>'
            '<p class="font-body-sm text-body-sm text-secondary">' + body.strip() +
            '</p></div></div>')
    out.append('</div>')
    return ''.join(out)


def style_body(html):
    """Gắn class Jackey Editorial vào HTML mà python-markdown sinh ra."""
    quotes, lists, diagrams = [], [], []

    def _quote(m):
        inner = m.group(0)
        ps = re.findall(r'<p>(.*?)</p>', inner, flags=re.DOTALL)
        if len(ps) >= 2:
            txt, cite = ps[0], ps[1].lstrip('—').strip()
        elif ps:
            txt, cite = ps[0], ''
        else:
            txt, cite = '', ''
        out = ('<blockquote class="' + QUOTE_CLS + '">'
               '<p class="' + QUOTE_TXT_CLS + '">' + txt + '</p>')
        if cite:
            out += '<cite class="' + QUOTE_CITE_CLS + '">— ' + cite + '</cite>'
        out += '</blockquote>'
        quotes.append(out)
        return '@@QUOTE%d@@' % (len(quotes) - 1)

    def _list(m):
        lists.append(_numlist_cards(m.group(0)))
        return '@@LIST%d@@' % (len(lists) - 1)

    def _diagram(m):
        diagrams.append(m.group(0))
        return '@@DIAGRAM%d@@' % (len(diagrams) - 1)

    html = re.sub(r'<blockquote>.*?</blockquote>', _quote, html, flags=re.DOTALL)
    html = re.sub(r'<ol>.*?</ol>', _list, html, flags=re.DOTALL)
    html = re.sub(r'<div class="my-10 p-6.*?</p>\s*</div>', _diagram, html, flags=re.DOTALL)
    # đoạn văn: đoạn đầu là LEAD, các đoạn giữa mb-6, đoạn cuối mb-8
    # (duyệt ngược để vị trí các match trước không bị lệch)
    paras = list(re.finditer(r'<p>(.*?)</p>', html, flags=re.DOTALL))
    n = len(paras)
    for idx in range(n - 1, -1, -1):
        m = paras[idx]
        cls = LEAD_CLS if idx == 0 else (P_LAST_CLS if idx == n - 1 else P_CLS)
        html = (html[:m.start()] + '<p class="' + cls + '">' + m.group(1) + '</p>'
                + html[m.end():])
    html = re.sub(r'<h2>(.*?)</h2>',
                  lambda m: '<h2 class="' + H2_CLS + '">' + m.group(1) + '</h2>',
                  html, flags=re.DOTALL)
    html = re.sub(r'<h3>(.*?)</h3>',
                  lambda m: '<h3 class="' + H3_CLS + '">' + m.group(1) + '</h3>',
                  html, flags=re.DOTALL)
    html = re.sub(r'<ul>', '<ul class="list-disc pl-6 my-6 space-y-2 '
                           'font-body-md text-body-md text-secondary">', html)
    html = re.sub(r'<a href=', '<a class="text-primary hover:underline '
                               'underline-offset-4" href=', html)
    html = re.sub(r'<pre>', '<pre class="my-6 p-4 rounded-lg bg-surface-container '
                            'overflow-x-auto">', html)
    for i, q in enumerate(quotes):
        html = html.replace('@@QUOTE%d@@' % i, q)
    for i, li in enumerate(lists):
        html = html.replace('@@LIST%d@@' % i, li)
    for i, d in enumerate(diagrams):
        html = html.replace('@@DIAGRAM%d@@' % i, d)
    return html


def load_posts():
    posts = []
    for path in sorted(glob.glob(os.path.join(BASE, 'content', 'posts', '*.md'))):
        text = open(path, encoding='utf-8').read()
        if not text.startswith('---\n'):
            raise ValueError('%s thiếu frontmatter' % path)
        _, fm_text, body_md = text.split('---\n', 2)
        fm = yaml.safe_load(fm_text) or {}
        iso = fm.get('date')
        iso = iso.isoformat() if hasattr(iso, 'isoformat') else str(iso)
        iso = iso[:10]  # chỉ lấy phần ngày (Decap có thể ghi kèm giờ)
        y, m, d = iso.split('-')
        if fm.get('hero_image'):
            hero, hero_src = 'image', fm['hero_image']
            hero_alt = fm.get('hero_alt') or ''
            hero_caption = fm.get('hero_caption') or ''
            hero_icon, hero_label = '', ''
        else:
            hero, hero_src = 'icon', ''
            hero_alt, hero_caption = '', ''
            hero_icon = fm.get('hero_icon') or 'description'
            hero_label = fm.get('hero_label') or ''
        body_html = style_body(md_lib.markdown(body_md, extensions=['extra']))
        posts.append({
            'slug': fm.get('slug') or os.path.splitext(os.path.basename(path))[0],
            'title': fm.get('title') or '',
            'category': fm.get('category') or '',
            'date': '%s/%s/%s' % (d, m, y),
            '_iso': iso,
            'read': fm.get('read') or '',
            'excerpt': fm.get('excerpt') or '',
            'hero': hero,
            'hero_src': hero_src,
            'hero_alt': hero_alt,
            'hero_caption': hero_caption,
            'hero_icon': hero_icon,
            'hero_label': hero_label,
            'featured_src': fm.get('featured_image') or hero_src,
            'tags': fm.get('tags') or [],
            'body': body_html,
        })
    posts.sort(key=lambda p: p['_iso'], reverse=True)
    return posts


POSTS = load_posts()

# ---------------------------------------------------------------- helpers
def urls(depth):
    p = "" if depth == 0 else "../"
    return {
        "index": p + "index.html",
        "archive": p + "bai-viet.html",
        "about": p + "gioi-thieu.html",
        "rss": p + "rss.xml",
        "img": lambda name: p + "images/" + name,
        "article": (lambda slug: p + "bai-viet/" + slug + ".html") if depth == 0
                   else (lambda slug: slug + ".html"),
    }

ACTIVE = "text-primary font-label-md text-label-md border-b-2 border-primary pb-1"
INACTIVE = ("text-secondary font-label-md text-label-md hover:text-on-surface "
            "transition-colors duration-150")

def header(active, u):
    def link(name, href, is_active):
        cls = ACTIVE if is_active else INACTIVE
        return ('<a class="' + cls + '" href="' + href + '">\n            ' + name +
                '\n          </a>')
    return ('<header class="w-full bg-surface border-b border-surface-container-highest '
            'sticky top-0 z-50">\n'
            '<div class="w-full max-w-7xl mx-auto px-6 md:px-12 flex justify-between '
            'items-center h-20">\n'
            '<a class="font-headline-lg text-headline-lg font-bold tracking-tight '
            'text-on-surface transition-colors hover:text-primary-container" href="'
            + u["index"] + '">\n        Jackethee\n      </a>\n'
            '<div class="flex items-center space-x-6 md:space-x-8">\n'
            '<nav class="flex items-center space-x-6 md:space-x-8">\n'
            + link("Trang chủ", u["index"], active == "home") + '\n'
            + link("Bài viết", u["archive"], active == "archive") + '\n'
            + link("Giới thiệu", u["about"], active == "about") + '\n'
            '</nav>\n'
            '<button aria-label="Tìm kiếm" class="p-2 text-secondary '
            'hover:text-primary-container transition-colors duration-150 focus:outline-none" '
            'type="button">\n'
            '<span class="material-symbols-outlined text-[20px]" data-icon="search">search'
            '</span>\n</button>\n</div>\n</div>\n</header>')

def footer(u):
    return ('<footer class="w-full bg-surface border-t border-surface-container-highest">\n'
            '<div class="w-full max-w-7xl mx-auto px-6 md:px-12 py-12 flex flex-col '
            'md:flex-row justify-between items-center gap-6">\n'
            '<div class="text-center md:text-left space-y-1">\n'
            '<a class="font-headline-md text-headline-md font-bold text-on-surface '
            'hover:text-primary transition-colors" href="' + u["index"] + '">\n'
            '          Jackethee\n        </a>\n'
            '<p class="font-body-sm text-body-sm text-secondary">\n'
            '          Góc ghi chép của một sinh viên CNTT làm Business Analyst.\n'
            '        </p>\n</div>\n'
            '<div class="flex items-center space-x-6">\n'
            '<a class="text-secondary font-label-sm text-label-sm hover:text-primary '
            'transition-colors" href="https://github.com/juniorfrontend-journey" '
            'rel="noopener noreferrer" target="_blank">\n          GitHub\n        </a>\n'
            '<a class="text-secondary font-label-sm text-label-sm hover:text-primary '
            'transition-colors" href="mailto:lienhe@jackethee.dev">\n          Email\n'
            '        </a>\n'
            '<a class="text-secondary font-label-sm text-label-sm hover:text-primary '
            'transition-colors" href="' + u["archive"] + '">\n          Bài viết\n'
            '        </a>\n'
            '<a class="text-secondary font-label-sm text-label-sm hover:text-primary '
            'transition-colors" href="' + u["rss"] + '">\n          RSS\n        </a>\n'
            '</div>\n</div>\n'
            '<div class="w-full border-t border-surface-container-highest/60 py-4 text-center">\n'
            '<p class="font-body-sm text-body-sm text-secondary">\n'
            '        © 2026 Jackethee. All rights reserved.\n      </p>\n</div>\n</footer>')

def swap_chrome(html, active, u):
    html = re.sub(r'<header class="w-full bg-surface[^>]*>.*?</header>',
                  lambda m: header(active, u), html, count=1, flags=re.DOTALL)
    html = re.sub(r'<footer class="w-full bg-surface[^>]*>.*?</footer>',
                  lambda m: footer(u), html, count=1, flags=re.DOTALL)
    return html

def swap_images(html, u):
    for url, name in IMG_MAP.items():
        html = html.replace(url, u["img"](name))
    return html

# ---------------------------------------------------------------- cards
def card(post, url):
    return ('<article class="bg-surface-container-lowest border '
            'border-surface-container-highest rounded-xl p-6 flex flex-col justify-between '
            'hover:border-primary-container transition-colors duration-150">\n'
            '<div class="space-y-3">\n<div class="flex items-center justify-between">\n'
            '<span class="bg-[#FEF2F0] text-primary font-label-sm text-label-sm px-2 py-0.5 '
            'rounded-xl border border-outline-variant">\n                ' + post["category"] +
            '\n              </span>\n'
            '<span class="font-label-sm text-label-sm text-secondary">' + post["date"] +
            '</span>\n</div>\n'
            '<h3 class="font-headline-sm text-headline-sm text-on-surface hover:text-primary '
            'transition-colors">\n<a href="' + url + '">' + post["title"] + '</a>\n</h3>\n'
            '<p class="font-body-sm text-body-sm text-secondary line-clamp-3">\n              '
            + post["excerpt"] + '\n            </p>\n</div>\n'
            '<div class="pt-4 mt-6 border-t border-surface-container-high flex items-center '
            'justify-between font-label-sm text-label-sm text-secondary">\n'
            '<span class="flex items-center gap-1">\n'
            '<span class="material-symbols-outlined text-[14px]" data-icon="schedule">'
            'schedule</span>\n              ' + post["read"] + '\n            </span>\n'
            '<a class="text-primary hover:text-primary-container font-bold flex items-center '
            'gap-0.5" href="' + url + '">\n              Chi tiết →\n            </a>\n'
            '</div>\n</article>')

def featured_card(post, u):
    url = u["article"](post["slug"])
    if post["featured_src"]:
        fname = post["featured_src"].split("/")[-1]
        media = ('<img class="w-full h-full object-cover" data-alt="' + post["hero_alt"] +
                 '" src="' + u["img"](fname) + '"/>')
    else:
        media = ('<div class="w-full h-full flex flex-col items-center justify-center gap-3">'
                 '<span class="material-symbols-outlined text-[72px] text-primary-container" '
                 'data-icon="' + post["hero_icon"] + '">' + post["hero_icon"] + '</span>'
                 '<span class="font-label-md text-label-md text-secondary tracking-wider">'
                 + post["hero_label"] + '</span></div>')
    return ('<article class="bg-surface-container-lowest border '
            'border-surface-container-highest rounded-xl p-6 md:p-8 hover:border-primary-container '
            'transition-colors duration-200">\n'
            '<div class="grid grid-cols-1 md:grid-cols-12 gap-8 items-center">\n'
            '<!-- Image Placeholder -->\n'
            '<div class="md:col-span-6 overflow-hidden rounded-xl bg-surface-container-low '
            'aspect-[16/10] border border-surface-container-highest">\n'
            + media + '\n</div>\n'
            '<!-- Content Column -->\n'
            '<div class="md:col-span-6 flex flex-col justify-between space-y-4">\n'
            '<div class="space-y-3">\n'
            '<div class="flex items-center space-x-3">\n'
            '<span class="bg-[#FEF2F0] text-primary font-label-sm text-label-sm px-2.5 py-1 '
            'rounded-xl border border-outline-variant">\n                  ' + post["category"] +
            '\n                </span>\n'
            '<span class="font-label-sm text-label-sm text-secondary">\n                  '
            + post["date"] + '\n                </span>\n'
            '</div>\n'
            '<h3 class="font-headline-lg text-headline-lg text-on-surface hover:text-primary '
            'transition-colors leading-snug">\n'
            '<a href="' + url + '">' + post["title"] + '</a>\n</h3>\n'
            '<p class="font-body-md text-body-md text-secondary leading-relaxed">\n'
            '                ' + post["excerpt"] + '\n              </p>\n'
            '</div>\n'
            '<!-- Reading Meta & Action -->\n'
            '<div class="pt-4 border-t border-surface-container-high flex items-center '
            'justify-between font-label-md text-label-md">\n'
            '<span class="text-secondary flex items-center gap-1">\n'
            '<span class="material-symbols-outlined text-[16px]" data-icon="schedule">'
            'schedule</span>\n                ' + post["read"] + '\n              </span>\n'
            '<a class="text-primary font-bold hover:text-primary-container flex items-center '
            'gap-1 transition-colors" href="' + url + '">\n'
            '<span>Đọc tiếp</span>\n'
            '<span class="material-symbols-outlined text-[16px]" data-icon="arrow_right_alt">'
            'arrow_right_alt</span>\n'
            '</a>\n</div>\n</div>\n</div>\n</article>')

def related_card(post, url):
    return ('<article class="flex flex-col bg-surface-container-lowest border '
            'border-surface-container-highest rounded-xl p-5 hover:border-outline '
            'transition-colors group">\n'
            '<div class="flex items-center justify-between mb-3">\n'
            '<span class="inline-block px-2 py-0.5 rounded border border-outline-variant/60 '
            'font-label-sm text-label-sm text-primary">\n              ' + post["category"] +
            '\n            </span>\n'
            '<span class="font-label-sm text-label-sm text-secondary">' + post["date"] +
            '</span>\n</div>\n'
            '<h3 class="font-headline-sm text-headline-sm text-on-surface group-hover:text-primary '
            'transition-colors mb-2 line-clamp-2">\n<a href="' + url + '">' + post["title"] +
            '</a>\n</h3>\n'
            '<p class="font-body-sm text-body-sm text-secondary line-clamp-3 mb-4 flex-grow">\n'
            '            ' + post["excerpt"] + '\n          </p>\n'
            '<span class="font-label-sm text-label-sm text-secondary flex items-center gap-1">\n'
            '<span class="material-symbols-outlined text-xs" data-icon="schedule">schedule'
            '</span>\n            ' + post["read"] + '\n          </span>\n</article>')

def grid_cards(posts, u):
    out = []
    for i, post in enumerate(posts, 1):
        out.append('<!-- Card %d -->\n' % i + card(post, u["article"](post["slug"])))
    return '\n'.join(out)

# ---------------------------------------------------------------- home
def build_home():
    u = urls(0)
    h = open(os.path.join(STITCH, "home.html"), encoding="utf-8").read()
    h = swap_images(h, u)
    h = swap_chrome(h, "home", u)
    feat = POSTS[0]
    h = re.sub(r'<article class="bg-surface-container-lowest border '
               r'border-surface-container-highest rounded-xl p-6 md:p-8.*?</article>',
               lambda m: featured_card(feat, u), h, count=1, flags=re.DOTALL)
    d, m, y = feat["date"].split("/")
    h = h.replace("Tháng 11 / 2026", "Tháng %s / %s" % (m, y))
    h = re.sub(r'(<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">)'
               r'.*?(</div>\s*</section>)',
               lambda m: m.group(1) + "\n" + grid_cards(POSTS[1:], u) + "\n" + m.group(2),
               h, count=1, flags=re.DOTALL)
    h = h.replace("06 bài viết", "%02d bài viết" % len(POSTS))
    return h

# ---------------------------------------------------------------- archive
def build_archive():
    u = urls(0)
    h = open(os.path.join(STITCH, "home.html"), encoding="utf-8").read()
    h = swap_images(h, u)
    h = swap_chrome(h, "archive", u)
    start = h.index("<!-- HERO SECTION -->")
    end = h.index("<!-- LATEST ARTICLES (BÀI VIẾT MỚI NHẤT) -->")
    h = h[:start] + h[end:]
    h = re.sub(r'<title>.*?</title>',
               '<title>Tất cả bài viết - Jackethee</title>', h, count=1, flags=re.DOTALL)
    h = h.replace('<h2 class="font-headline-lg text-headline-lg text-on-surface">\n'
                  '            Bài viết mới nhất\n          </h2>',
                  '<h1 class="font-headline-lg text-headline-lg text-on-surface">\n'
                  '            Tất cả bài viết\n          </h1>')
    h = h.replace("Ghi chép chuyên sâu, case study thực tế và kinh nghiệm phát triển",
                  "Mọi bài viết trên blog — mới nhất trước.")
    h = re.sub(r'(<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">)'
               r'.*?(</div>\s*</section>)',
               lambda m: m.group(1) + "\n" + grid_cards(POSTS, u) + "\n" + m.group(2),
               h, count=1, flags=re.DOTALL)
    h = h.replace("06 bài viết", "%02d bài viết" % len(POSTS))
    return h

# ---------------------------------------------------------------- article
def breadcrumb(post, u):
    return ('<nav aria-label="Breadcrumb" class="flex items-center space-x-2 text-secondary '
            'font-label-sm text-label-sm mb-4">\n'
            '<a class="hover:text-primary transition-colors duration-150" href="'
            + u["index"] + '">Trang chủ</a>\n'
            '<span class="text-surface-variant">/</span>\n'
            '<a class="hover:text-primary transition-colors duration-150" href="'
            + u["archive"] + '">' + post["category"] + '</a>\n'
            '<span class="text-surface-variant">/</span>\n'
            '<span class="text-on-surface truncate">' + post["title"] + '</span>\n</nav>')

def hero_figure(post, u):
    if post["hero"] == "image":
        fname = post["hero_src"].split("/")[-1]
        return ('<figure class="max-w-4xl mx-auto mb-10 md:mb-14">\n'
                '<div class="w-full aspect-[16/9] overflow-hidden rounded-xl '
                'bg-surface-container border border-surface-container-highest">\n'
                '<img alt="' + post["hero_alt"] + '" class="w-full h-full object-cover" '
                'src="' + u["img"](fname) + '"/>\n</div>\n'
                '<figcaption class="mt-2.5 text-center font-body-sm text-body-sm '
                'text-secondary italic">\n        ' + post["hero_caption"] + '\n      '
                '</figcaption>\n</figure>')
    return ('<figure class="max-w-4xl mx-auto mb-10 md:mb-14">\n'
            '<div class="w-full aspect-[16/9] overflow-hidden rounded-xl bg-surface-container '
            'border border-surface-container-highest flex flex-col items-center '
            'justify-center gap-3">\n'
            '<span class="material-symbols-outlined text-[72px] text-primary-container" '
            'data-icon="' + post["hero_icon"] + '">' + post["hero_icon"] + '</span>\n'
            '<span class="font-label-md text-label-md text-secondary tracking-wider">'
            + post["hero_label"] + '</span>\n</div>\n</figure>')

def tags_row(post, u):
    out = ['<span class="font-label-sm text-label-sm text-secondary mr-2">Tags:</span>']
    for t in post["tags"]:
        out.append('<a class="px-2.5 py-1 rounded border border-surface-container-highest '
                   'text-secondary font-label-sm text-label-sm hover:border-primary-container '
                   'hover:text-primary transition-colors" href="' + u["archive"] + '">#' + t + '</a>')
    return "\n".join(out)

def prevnext_block(prev_post, next_post, u):
    def side(post, label, icon, align_right):
        if post is None:
            url, title = u["archive"], "Xem tất cả bài viết"
        else:
            url, title = u["article"](post["slug"]), post["title"]
        align = " text-left sm:text-right" if align_right else ""
        span_align = ("justify-start sm:justify-end " if align_right else "")
        if align_right:
            label_html = (label + '\n            <span class="material-symbols-outlined '
                          'text-sm" data-icon="' + icon + '">' + icon + '</span>')
        else:
            label_html = ('<span class="material-symbols-outlined text-sm" data-icon="'
                          + icon + '">' + icon + '</span>\n            ' + label)
        return ('<a class="group p-4 rounded-lg border border-surface-container-highest '
                'bg-surface-container-lowest hover:border-outline transition-colors block'
                + align + '" href="' + url + '">\n'
                '<span class="font-label-sm text-label-sm text-secondary flex items-center '
                + span_align + 'gap-1 mb-1 group-hover:text-primary">\n' + label_html +
                '\n</span>\n'
                '<p class="font-headline-sm text-headline-sm text-on-surface '
                'group-hover:text-primary transition-colors line-clamp-2">\n            '
                + title + '\n          </p>\n</a>')
    return ('<div class="my-10 grid grid-cols-1 sm:grid-cols-2 gap-4">\n'
            + side(prev_post, "Bài trước", "arrow_back", False) + '\n'
            + side(next_post, "Bài tiếp theo", "arrow_forward", True) + '\n</div>')

def related_section(post, u):
    others = [p for p in POSTS if p is not post]
    same = [p for p in others if p["category"] == post["category"]]
    rest = [p for p in others if p["category"] != post["category"]]
    rel = (same + rest)[:3]
    cards = "\n".join(related_card(p, u["article"](p["slug"])) for p in rel)
    return ('<section class="mt-16 pt-10 border-t border-surface-container-highest">\n'
            '<div class="flex items-center justify-between mb-6">\n'
            '<h2 class="font-headline-md text-headline-md text-on-surface">Bài liên quan</h2>\n'
            '<a class="font-label-md text-label-md text-secondary hover:text-primary '
            'transition-colors" href="' + u["archive"] + '">Xem tất cả bài viết →</a>\n'
            '</div>\n<div class="grid grid-cols-1 md:grid-cols-3 gap-6">\n' + cards +
            '\n</div>\n</section>')

def build_article(post, idx):
    u = urls(1)
    h = open(os.path.join(STITCH, "article.html"), encoding="utf-8").read()
    h = swap_images(h, u)
    h = swap_chrome(h, "archive", u)
    h = re.sub(r'<title>.*?</title>',
               '<title>' + post["title"] + ' - Jackethee</title>', h, count=1, flags=re.DOTALL)
    h = re.sub(r'<nav aria-label="Breadcrumb".*?</nav>',
               lambda m: breadcrumb(post, u), h, count=1, flags=re.DOTALL)
    h = re.sub(r'(<span class="inline-flex items-center px-2\.5 py-0\.5 rounded-lg border '
               r'border-outline-variant/60 bg-surface-container-low font-label-sm '
               r'text-label-sm text-primary tracking-wide">)\s*[^<]*\s*(</span>)',
               lambda m: m.group(1) + "\n          " + post["category"] + "\n        " + m.group(2),
               h, count=1)
    h = re.sub(r'(<h1 class="font-headline-lg md:font-display[^>]*>)\s*.*?\s*(</h1>)',
               lambda m: m.group(1) + "\n        " + post["title"] + "\n      " + m.group(2),
               h, count=1, flags=re.DOTALL)
    h = h.replace("<span>17/11/2026</span>", "<span>" + post["date"] + "</span>", 1)
    h = h.replace("6 phút đọc", post["read"], 1)
    h = re.sub(r'<figure class="max-w-4xl mx-auto mb-10 md:mb-14">.*?</figure>',
               lambda m: hero_figure(post, u), h, count=1, flags=re.DOTALL)
    if post["body"]:
        h = re.sub(r'(<article class="max-w-\[42rem\] mx-auto text-on-surface">).*?'
                   r'(<!-- Tags Row -->)',
                   lambda m: m.group(1) + "\n" + post["body"] + "\n" + m.group(2),
                   h, count=1, flags=re.DOTALL)
    h = re.sub(r'(<div class="pt-6 pb-2 border-t border-surface-container-highest '
               r'flex flex-wrap gap-2 items-center">).*?(</div>)',
               lambda m: m.group(1) + "\n" + tags_row(post, u) + "\n" + m.group(2),
               h, count=1, flags=re.DOTALL)
    h = h.replace('<a class="inline-flex items-center text-primary font-label-md '
                  'text-label-md hover:underline underline-offset-4 transition-colors" '
                  'href="#">',
                  '<a class="inline-flex items-center text-primary font-label-md '
                  'text-label-md hover:underline underline-offset-4 transition-colors" '
                  'href="' + u["archive"] + '">', 1)
    prev_post = POSTS[idx + 1] if idx + 1 < len(POSTS) else None
    next_post = POSTS[idx - 1] if idx - 1 >= 0 else None
    h = re.sub(r'<div class="my-10 grid grid-cols-1 sm:grid-cols-2 gap-4">.*?</div>\s*</article>',
               lambda m: prevnext_block(prev_post, next_post, u) + "\n</article>",
               h, count=1, flags=re.DOTALL)
    h = re.sub(r'<section class="mt-16 pt-10 border-t border-surface-container-highest">'
               r'.*?</section>',
               lambda m: related_section(post, u), h, count=1, flags=re.DOTALL)
    return h

# ---------------------------------------------------------------- about
def build_about():
    u = urls(0)
    h = open(os.path.join(STITCH, "about.html"), encoding="utf-8").read()
    h = swap_images(h, u)
    h = swap_chrome(h, "about", u)
    h = h.replace('href="#articles"', 'href="' + u["archive"] + '"')
    h = h.replace('href="#"', 'href="' + u["archive"] + '"')
    return h

# ---------------------------------------------------------------- rss
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def build_rss():
    items = []
    for p in POSTS:
        d, m, y = p["date"].split("/")
        pub = "%s, %s %s %s 12:00:00 +0700" % ("Mon", d, MONTHS[int(m) - 1], y)
        link = SITE_URL + "/bai-viet/" + p["slug"] + ".html"
        items.append(
            "  <item>\n    <title>" + p["title"] + "</title>\n"
            "    <link>" + link + "</link>\n"
            "    <guid>" + link + "</guid>\n"
            "    <pubDate>" + pub + "</pubDate>\n"
            "    <category>" + p["category"] + "</category>\n"
            "    <description>" + p["excerpt"] + "</description>\n  </item>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0">\n<channel>\n'
            "  <title>Jackethee — Blog cá nhân</title>\n"
            "  <link>" + SITE_URL + "</link>\n"
            "  <description>Góc ghi chép của một sinh viên CNTT làm Business Analyst.</description>\n"
            "  <language>vi</language>\n" + "\n".join(items) + "\n</channel>\n</rss>\n")

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="thư mục đích (mặc định: site/)")
    args = ap.parse_args()
    out = os.path.abspath(args.out) if args.out else SITE
    os.makedirs(os.path.join(out, "bai-viet"), exist_ok=True)
    os.makedirs(os.path.join(out, "images"), exist_ok=True)
    pages = {}
    pages["index.html"] = build_home()
    pages["bai-viet.html"] = build_archive()
    pages["gioi-thieu.html"] = build_about()
    for i, post in enumerate(POSTS):
        pages["bai-viet/" + post["slug"] + ".html"] = build_article(post, i)
    pages["rss.xml"] = build_rss()
    for rel, text in pages.items():
        path = os.path.join(out, rel)
        open(path, "w", encoding="utf-8").write(text)
        print("wrote %-45s %6d bytes" % (rel, len(text.encode("utf-8"))))
    # xóa trang của bài đã xóa (Decap xóa file .md nhưng HTML cũ vẫn nằm lại)
    keep = {"bai-viet/" + p["slug"] + ".html" for p in POSTS}
    art_dir = os.path.join(out, "bai-viet")
    for f in sorted(os.listdir(art_dir)):
        if f.endswith(".html") and ("bai-viet/" + f) not in keep:
            os.remove(os.path.join(art_dir, f))
            print("removed stale %-38s" % ("bai-viet/" + f))
    # ảnh nguồn (images/ ở repo root) -> thư mục đích, trừ khi đã trùng nhau
    src_img = os.path.join(BASE, "images")
    dst_img = os.path.join(out, "images")
    if os.path.isdir(src_img) and os.path.abspath(src_img) != os.path.abspath(dst_img):
        for f in sorted(os.listdir(src_img)):
            s, d = os.path.join(src_img, f), os.path.join(dst_img, f)
            if not os.path.exists(d) or open(s, 'rb').read() != open(d, 'rb').read():
                shutil.copy2(s, d)
    print("images:", sorted(os.listdir(dst_img)) if os.path.isdir(dst_img) else "—")
    # trang quản trị Decap (admin/) -> thư mục đích, trừ khi đã trùng nhau
    src_admin = os.path.join(BASE, "admin")
    dst_admin = os.path.join(out, "admin")
    if os.path.isdir(src_admin) and os.path.abspath(src_admin) != os.path.abspath(dst_admin):
        shutil.copytree(src_admin, dst_admin, dirs_exist_ok=True)
        print("admin: copied to", dst_admin)

if __name__ == "__main__":
    main()

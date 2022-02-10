import math

def make_button(href, label):
    klass = 'pure-button'
    if href == '#': klass += ' pure-button-disabled'
    return '''
    <a href="{0}" class="{1}">{2}</a>
    '''.format(href, klass, label)

def make_pager(page, total, per_page):
    # ページ数を計算
    page_count = math.ceil(total / per_page)
    s = '<div style="text-align:center;">'
    # 前へボタン
    prev_link = '?page=' + str(page - 1)
    if page <= 0: prev_link = '#'
    s += make_button(prev_link, '←前へ')
    # ページ番号
    s += '{0}/{1}'.format(page+1, page_count)
    # 次へボタン
    next_link = '?page=' + str(page + 1)
    if page >= page_count - 1: next_link = '#'
    s += make_button(next_link, '次へ→')
    s += '</div>'
    return s

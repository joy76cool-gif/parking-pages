import sys
src, top, out = sys.argv[1], sys.argv[2], sys.argv[3]
lines = open(src, encoding='utf8').read().split('\n')
body = '\n'.join(lines[1:])  # drop wrapper first line
body = body.rstrip()
assert body.endswith('</body></html>'); body = body[:-len('</body></html>')].rstrip()
t = open(top, encoding='utf8').read()
a = '<h1>停車標案總覽（只放招標中）</h1>'
assert body.count(a) == 1
body = body.replace(a, '<h1>停車標案總覽</h1>\n' + t, 1)
# move 名詞/meta lines stay inside; close details before unslop style
b = '<style id="unslop">'
assert body.count(b) == 1
body = body.replace(b, '</details>\n' + b, 1)
open(out, 'w', encoding='utf8').write(body)
print('ok', len(body))

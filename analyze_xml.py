from lxml import etree

tree = etree.parse("data.xml")
page_cnt = tree.xpath("count(/data/page)")

max_cnt, max_idx = 0, -1

for i in range(int(page_cnt)):
    cnt = tree.xpath("count(//page[{}]/fragment[@type='text'])".format(i + 1))
    if max_cnt < cnt:
        max_cnt = cnt
        max_idx = i + 1

max_cnt = int(max_cnt)
url = tree.xpath("string(/data/page[{}]/@url)".format(max_idx))

print max_idx, max_cnt, url
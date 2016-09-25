# CoolParser
Python lab project which helps to get specific information from html and store it in xml file

##Task 1
* Based on given URL site address, obtain text and graphic information from HTML tags of this site pages. Use XPATH to perform this task.
```Python
def parse_html(url):
    response = urllib2.urlopen(url)
    page = response.read()
    page = clean_html(page)

    tree = etree.HTML(page.decode('utf-8'))

    text = tree.xpath('//text()')
    text = process_text(text)

    images = tree.xpath('//img/@src')
    images = process_images(images)

    urls = tree.xpath('//a/@href')
    urls = process_urls(urls)

    return urls, text, images
```

* Generate XML node for given page

```Python
def generate_xml_page(page_url, text, images):
    page_elem = etree.Element("page", url=page_url)

    for elem in text:
        fragment = etree.Element("fragment", type="text")
        fragment.text = elem
        page_elem.append(fragment)

    for img in images:
        fragment = etree.Element("fragment", type="image")
        fragment.text = img
        page_elem.append(fragment)

    return page_elem
```

* Store parsed information in XML file

```Python
def generate_xml(filename):
    root = etree.Element("data")

    urls, _, _ = parse_html(BASE_URL)
    urls.insert(0, BASE_URL)

    for url in urls:
        _, text, images = parse_html(url)
        page_elem = generate_xml_page(url, text, images)
        root.append(page_elem)

    et = etree.ElementTree(root)
    et.write(filename, encoding="utf-8", xml_declaration=True, pretty_print=True)
```
##Task 2
By means of XPath find XML node with maximum number of text fragments

```Python
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
```
##Task 3
Analyze a content of Web store and fetch price, name, description and image of 20 products from that site. Use XPath and DOM-parser to find appropriate nodes.

```Python
def parse_html(url):
    response = urllib2.urlopen(BASE_URL + url)
    page = response.read()

    tree = etree.HTML(page.decode("cp1251").encode('utf-8'))

    name = tree.xpath("string(//div[@itemprop='name']/h1/text())")
    price = tree.xpath("string(//div[@id='optionPrice']/text())")
    image = tree.xpath("string(//img[@class='thumbnail']/@src)")
    desc = tree.xpath("//div[@style='overflow-x: auto']/span[@itemprop='description']//text()")

    process_text(desc)
    desc = reduce(lambda a, x: a + x, desc)

    return Product(name, price, desc, BASE_URL + image)
```
##Task 4
By means of XSLT language, convert obtained XML-file to XHTML page

<b>transform.py</b>
```Python
xslt_root = etree.parse("pattern.xsl")
transorm = etree.XSLT(xslt_root)
xml_root = etree.parse("products.xml")
result_tree = transorm(xml_root)
result = str(result_tree)
with open("products.xhtml", "w") as out:
    out.write(result)
```

<b>pattern.xsl</b>
```XSL
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>Products</h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th style="text-align:left">Name</th>
        <th style="text-align:left">Price</th>
        <th style="text-align:left">Description</th>
        <th style="text-align:left">Image url</th>
      </tr>
      <xsl:for-each select="data/product">
      <tr>
        <td><xsl:value-of select="name"/></td>
        <td><xsl:value-of select="price"/></td>
        <td><xsl:value-of select="description"/></td>
        <td><xsl:value-of select="image"/></td>
      </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>
```

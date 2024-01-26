#!/usr/bin/env python
print("Content-Type: text/html")
print()
print('''
<html>
<head>
    <title>Yeast Genome Broser</title>
    <style>
        .container { fill: #ffff; opacity: 0 }
        .container:hover{ fill: #ccc; opacity: 0.5 }
    </style>
</head>
<body>
<h2>My Yeast Genome Browser</h2>
<form>
    <p>Choose the yeast chromosome:
    <select name="chrom">
''')

#import relevant modules and connect to database
import cgi
import cgitb
cgitb.enable()
import sqlite3
conn = sqlite3.connect('gBrowser.sqlite')
c = conn.cursor()

form = cgi.FieldStorage()

#get length of all yeast chromosomes
length = { 'chrI':230218, 'chrII':813184, 'chrIII':316620, 'chrIV':1531933,
        'chrV':576874, 'chrVI':270161, 'chrVII':1090940, 'chrVIII':562643,
        'chrIX':439888, 'chrX':745751, 'chrXI':666816, 'chrXII':1078177,
        'chrXIII':924431, 'chrXIV':784333, 'chrXV':1091291, 'chrXVI':948066, 'chrmt':85779 }

chroNames = ['chrI', 'chrII', 'chrIII', 'chrIV', 'chrV', 'chrVI', 'chrVII', 'chrVIII',
            'chrIX', 'chrX', 'chrXI', 'chrXII', 'chrXIII', 'chrXIV', 'chrXV', 'chrXVI', 'chrmt']

#get coordinates to show
#if a gene name is provided start showing at the beginning of the gene -1000
if form.getvalue("geneName"):
    query = form.getvalue("geneName")
    c.execute('SELECT chrom, start FROM gff WHERE name=?',(query,))
    (chrom, start) = c.fetchone()
    start = int(start) - 1000
#else if the chromosome and position were given start there
elif form.getvalue("chrom") and form.getvalue("position"):
    chrom = form.getvalue("chrom")
    start = int(form.getvalue("position"))
elif form.getvalue("chrom"):
    chrom = form.getvalue("chrom")
    start = 1
#else go to default position
else:
    chrom = "chrI"
    start = 1
#fix coordinates to avoid showing more than the chromosome end or beginning
if start < 1:
    start = 1
elif (start + 5000) > length[chrom]:
    start = length[chrom] - 5000


for i in chroNames:
    if i == chrom:
        print('''<option value="{0}" selected="selected">{0}</option>'''.format(i))
    else:
        print('''<option value="{0}">{0}</option>'''.format(i))

print('''
    </select></p>
    <p>Enter coordinates: <input type="text" name="position"></p>

    <p>Or, enter a gene name: <input type="text" name="geneName"></p>
    <p><input type="submit" value="submit"></p>
    </form>
''')

#get genes in the coordinates
start = int(start)
end = int(start)+5000
c.execute("SELECT name, start, end, strand, feature FROM gff WHERE chrom = ? AND (start BETWEEN ? AND ? OR end BETWEEN ? AND ?)",(chrom, start, end, start, end))
results = c.fetchall()
hits = len(results)

#begin SVG
height = 100 + hits*25
print('''
<svg width="750" height="{0}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <rect x="150" y="50" width="500" height="20" fill="red" stroke="black" stroke-width="2" />
'''.format(height))
#draw tick lines
for i in range(11):
    print('<line x1="{0}" y1="50" x2="{0}" y2="40" stroke-width="2" stroke="black" />'.format(150+i*50))
for i in range(6):
    print('<line x1="{0}" y1="50" x2="{0}" y2="35" stroke-width="2" stroke="black" />'.format(150+i*100))
    print('<text x="{0}" y="34" stroke="black">{1}</text>'.format(150+i*100,start+i*1000))

#create link to navigate

previousPos = start - 1000
nextPos = start + 1000

if previousPos < 1:
    previousPos = 1

if nextPos + 5000 > length[chrom]:
    nextPos = length[chrom] - 5000

print('''
<a xlink:href="/cgi-bin/gbrowser/genBrowser.py?chrom={0}&position={1}">
<polygon points="50,60 120,35 120,85" fill="red" opacity="0.5" /></a>
<a xlink:href="/cgi-bin/gbrowser/genBrowser.py?chrom={0}&position={2}">
<polygon points="680,35 680,85 750,60" fill="red" opacity="0.5" /></a>
'''.format(chrom,previousPos,nextPos))

#draw genes and gene names
count = 0
for i in results:
    (name, gstart, gend, strand, feature) = i
    if gstart < start:
        gstart = start
    if gend > end:
        gend = end
    xst = 150 + (gstart - start)/10.
    xwidth = (gend - gstart)/10.
    yst = 100 + 25 * count
    if feature == "tRNA":
        fill = "green"
    else:
        fill = "blue"

    info = "Start={0}; End={1}".format(gstart,gend)
    print('''<a xlink:href="http://www.yeastgenome.org/locus/{0}" xlink:title="{1}" target="myFrame" >'''.format(name,info))
    print('''<rect x="0" y="{0}" width="750" height="25" stroke="none" class="container" />'''.format(yst))
    print('<text x="50" y="{0}" stroke="black">{1}</text>'.format(yst+20,name))

    if strand == "-":
        print('<rect x="{0}" y="{1}" width="{2}" height="20" fill="{3}" stroke="black" opacity=0.5 /></a>'.format(xst,yst+3,xwidth,fill))
    else:
        print('<rect x="{0}" y="{1}" width="{2}" height="20" fill="{3}" stroke="black" /></a>'.format(xst,yst+3,xwidth,fill))

    count += 1


print('''</svg>

<iframe name="myFrame" width="100%" height="400px"></iframe>

</body>
</html>
'''
)
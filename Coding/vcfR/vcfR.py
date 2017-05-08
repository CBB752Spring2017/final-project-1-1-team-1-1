__author__ = "Dingjue Ji"
__copyright__ = "Copyright 2017"
__credits__ = ["Dingjue Ji"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Dingjue Ji"
__email__ = "dingjue.ji@yale.edu"

### Usage:      python vcfR.py -i query.vcf -ref ref.vcf.gz (or Link of ref) -o output.vcf
### Note:       vcf Retriever
import re
import gzip
import codecs
import argparse
import urllib.request
parser = argparse.ArgumentParser(description='vcf parser')
parser.add_argument('-i', '--input', help='input vcf', dest = 'i', required=True)
parser.add_argument('-f', '--ref', help='reference vcf', dest = 'f', required=True)
parser.add_argument('-o', '--ouput', help='matched vcf', dest = 'o', required=True)
args = parser.parse_args()
query = args.i
ref = args.f
output = args.o
outfile = open(output, 'w')
if bool(re.search('://', ref)):
    request = urllib.request.Request(ref)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib.request.urlopen(request)
    zf = gzip.GzipFile(fileobj=response)
else:
    zf = gzip.open(ref, 'r')
matchedfile = open(query.split('.')[0]+'_matched.vcf', 'w')
queries = list()
qlines = list()
with open(query, 'r') as vcf:
    for line in vcf:
        if line.startswith('#'):
            pass
        else:
            tmp = line.strip().split()
            tmp[2] = '\S+'
            queries.append(tmp[0:5])
            qlines.append(line)
k = 0
reader = codecs.getreader('utf-8')
content = reader(zf)
for line in content:
    if line.startswith('##'):
        pass
    elif line.startswith('#C'):
        outfile.write(line)
    elif k == len(queries):
        break
    else:
        tmp = line.strip().split()
        if bool(re.search('^[^0-9]', line)):
            if(tmp[0] >= queries[k][0] and int(tmp[1]) > int(queries[k][1])):
                k = k + 1
                pass
        elif int(tmp[0]) >= int(queries[k][0]) and int(tmp[1]) > int(queries[k][1]):
            k = k + 1
            continue
        elif bool(re.search('\s+'.join(queries[k]), line)):
            matchedfile.write(qlines[k])
            k = k + 1
            outfile.write(line)
zf.close()


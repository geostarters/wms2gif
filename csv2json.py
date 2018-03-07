from __future__ import print_function
import argparse
import csv

# rowData, 1, 8, 12, 19, 16, 15
def createFeature(rowData, namePosition, idPosition, xMinPosition, yMinPosition, xMaxPosition, yMaxPosition):
    typeTag = "Feature"
    bbox = "{},{},{},{}".format(rowData[xMinPosition], rowData[yMinPosition], rowData[xMaxPosition], rowData[yMaxPosition])
    propertiesTag = '{{ "nom": "{}", "id": "{}", "bbox_3857": "{}" }}'.format(rowData[namePosition], rowData[idPosition], bbox)
    return '{{"type": "{}", "properties": {} }}'.format(typeTag, propertiesTag)

def features2geojson(featureList):
    typeTag = "FeatureCollection"
    crsTag = '{ "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::25831" }}'
    featureListStr = '[{}]'.format(', '.join(featureList))
    return '{{"type": "{}", "crs": {}, "features":{}}}'.format(typeTag, crsTag, featureListStr)

def processFile(input, output, namePosition, idPosition, xMinPosition, yMinPosition, xMaxPosition, yMaxPosition):
    with open(input) as csvFile:
        rows = csv.reader(csvFile, delimiter=';')
        index = 0
        features = []
        for row in rows:
            if index != 0:  # Jump the first line with column names
                features.append(createFeature(row, namePosition, idPosition, xMinPosition, yMinPosition, xMaxPosition, yMaxPosition))

            index += 1

        with open(output, 'w') as outFile:
            outFile.write(features2geojson(features))

parser = argparse.ArgumentParser(description="Parses a csv with a bbox in EPSG:3857 and converts it to a json file to be used by the gifGenerator.py script")
parser.add_argument('--file', nargs='?', const=None, default=None, help='The name of the CSV file to be processed')
parser.add_argument('--output', nargs='?', const=None, default=None, help='Output file name')
parser.add_argument('--namePos', nargs='?', const=None, default=None, help='The 0-based column index where the name is found')
parser.add_argument('--idPos', nargs='?', const=None, default=None, help='The 0-based column index where the id is found')
parser.add_argument('--xMinPos', nargs='?', const=None, default=None, help='The 0-based column index where the xMin is found')
parser.add_argument('--yMinPos', nargs='?', const=None, default=None, help='The 0-based column index where the yMin is found')
parser.add_argument('--xMaxPos', nargs='?', const=None, default=None, help='The 0-based column index where the xMax is found')
parser.add_argument('--yMaxPos', nargs='?', const=None, default=None, help='The 0-based column index where the yMax is found')

args = parser.parse_args()

namePos = 1
idPos = 8
xMinPos = 12
yMinPos = 19
xMaxPos = 16
yMaxPos = 15

if(args.namePos is None):
    print("--namePos parameter not present, using default namePos (1)")
else:
    namePos = args.namePos

if(args.idPos is None):
    print("--idPos parameter not present, using default idPos (8)")
else:
    idPos = args.idPos

if(args.xMinPos is None):
    print("--xMinPos parameter not present, using default xMinPos (12)")
else:
    xMinPos = args.xMinPos

if(args.yMinPos is None):
    print("--yMinPos parameter not present, using default yMinPos (19)")
else:
    yMinPos = args.yMinPos

if(args.xMaxPos is None):
    print("--xMaxPos parameter not present, using default xMaxPos (16)")
else:
    xMaxPos = args.xMaxPos

if(args.yMaxPos is None):
    print("--yMaxPos parameter not present, using default yMaxPos (15)")
else:
    yMaxPos = args.yMaxPos

if(args.file is not None and args.output is not None):
    print("Processing file " + args.file)
    print("Saving output to " + args.output)
    processFile(args.file, args.output, namePos, idPos, xMinPos, yMinPos, xMaxPos, yMaxPos)

else:
    print("Error: neither --file nor --output parameters specified")

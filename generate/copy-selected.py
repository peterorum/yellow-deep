import json

json_file = '../data/predictions.json'
train_file = '../data/manually-selected-palettes.json'

data = json.load(open(json_file))
train = json.load(open(train_file))

train = [x for x in train if 'image' in x]

data.extend(train)

selected = [x for x in data if x['selected']]

for x in selected:
    print(f'aws s3 cp s3://functal-images/{x['image']} s3://functals/{x['image']} --acl public-read')

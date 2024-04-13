import json

def load_index(filename):
    with open(filename, 'r') as f:
        try:
            index_dict = json.load(f)
        except:
            return {}
        
    return index_dict
def write_index(filename, index_dict):
    with open(filename, 'w') as f:        
        json.dump(index_dict, f, indent=2)
def manual_tags(filename):
    print('Input space separated tags for')
    print(filename)
    tags_str = input('tags: ')
    tags = list(set(tags_str.split(' ')))
    tags = [tag for tag in tags if len(tag) > 0]
    return tags
    
    

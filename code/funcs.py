import json
import hashlib

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
def hash_index(index_dict):
    index_json_bytes = json.dumps(index_dict, sort_keys=True).encode()
    index_hash = hashlib.md5(index_json_bytes).hexdigest()
    return index_hash
def manual_tags(filename):
    print('Input space separated tags for')
    print(filename)
    tags_str = input('tags: ')
    return tags_str.split(' ')
    
    

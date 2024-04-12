import typer
import os
import shutil
from pathlib import Path
import datetime
import uuid
import json

app = typer.Typer(pretty_exceptions_enable=False)

@app.command(name='commit')
def commit(
        ingress: str = typer.Option(),
        retrieve: str = typer.Option(),
        storage: str = typer.Option(),
        index: str = typer.Option(),
):    
    ingress_content = os.listdir(ingress)

    timestamp = str(datetime.datetime.now()).replace(' ', '_').replace(':', '-').replace('.', '-')
    unique_id = uuid.uuid4()
    commit_name = f'{timestamp}_{unique_id}'    
    commit_path = Path(storage).joinpath(commit_name)

    print(f'New commit {commit_path}')
    os.mkdir(commit_path)

    with open(index, 'r') as f:
        index_dict = json.load(f)
    
    for ingress_file in ingress_content:
        ingress_path_file = Path(ingress).joinpath(ingress_file)
        commit_path_file = Path(commit_path).joinpath(Path(ingress_file).name)        
        shutil.copy(ingress_path_file, commit_path_file)

        parent = Path(commit_path_file).parent.name
        name = Path(commit_path_file).name
        local_file_path = str(Path(parent).joinpath(name))

        index_dict[local_file_path] = [
            {'type': 'filename', 'value': Path(name).stem},
            {'type': 'ext', 'value': Path(name).suffix.replace('.','')},
        ]

    with open(index, 'w') as f:
        json.dump(index_dict, f)
        print(f'Updated {index}')

@app.command(name='list')
def list_content(
        index: str = typer.Option(),
):
    with open(index, 'r') as f:
        index_dict = json.load(f)
            
    for key, tags in index_dict.items():
        tag_vals = [tag['value'] for tag in tags]
        print(f'{key}: {tag_vals}')        

@app.command(name='test')
def test():
    print('Hi')

if __name__ == '__main__': app()

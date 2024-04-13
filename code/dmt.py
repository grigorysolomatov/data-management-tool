import typer
import os
import shutil
from pathlib import Path
import datetime
import json

import funcs

from typing import List

app = typer.Typer(pretty_exceptions_enable=False)

@app.command(name='commit')
def commit(
        ingress: List[str] = typer.Argument(),
        storage: str = typer.Option(),
        index: str = typer.Option(),
        no_tag: bool = typer.Option(False),
):    
    index_dict = funcs.load_index(index)
    # --------------------------------------------------------------------------
    timestamp = str(datetime.datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '.')
    unique_id = funcs.hash_index(index_dict)
    commit_name = f'{timestamp}.{unique_id}'    
    commit_path = Path(storage).joinpath(commit_name)    
    os.mkdir(commit_path)
    print(f'New commit {commit_path}')
    # --------------------------------------------------------------------------    
    for ingress_file in ingress:
        #ingress_path_file = Path(ingress).joinpath(ingress_file)
        commit_path_file = Path(commit_path).joinpath(Path(ingress_file).name)
        shutil.copy(ingress_file, commit_path_file)        
        
        parent = Path(commit_path_file).parent.name
        name = Path(commit_path_file).name
        local_file_path = str(Path(parent).joinpath(name))
        index_dict[local_file_path] = [] if no_tag else funcs.manual_tags(ingress_file)
    # --------------------------------------------------------------------------
    funcs.write_index(index, index_dict)
    print(f'Updated {index}')

@app.command(name='list')
def list_content(
        index: str = typer.Option(),
):
    with open(index, 'r') as f:
        index_dict = json.load(f)
            
    for key, tags in index_dict.items():
        print(f'{key}: {tags}')

@app.command(name='reset')
def reset(
        storage: str = typer.Option(),
        index: str = typer.Option(),
):
    funcs.write_index(index, {})    
    shutil.rmtree(storage)
    os.mkdir(storage)

    print(f'Reset {storage} and {index}')    

@app.command(name='test')
def test():
    print('Hi')

if __name__ == '__main__': app()

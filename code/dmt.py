import typer
import os
import shutil
from pathlib import Path
import datetime
import toml

import funcs

from typing import List

app = typer.Typer(pretty_exceptions_enable=False)

@app.command(name='commit')
def commit(
        ingress: List[str] = typer.Argument(),
        config: str = typer.Option('config.toml'),
        no_tags: bool = typer.Option(False),
):
    config = toml.load(config)    
    index_dict = funcs.load_index(config['index'])
    # --------------------------------------------------------------------------
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    commit_path = Path(config['storage']).joinpath(timestamp)
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
        index_dict[local_file_path] = [] if no_tags else funcs.manual_tags(ingress_file)
    # --------------------------------------------------------------------------
    funcs.write_index(config['index'], index_dict)
    print('Updated {index}'.format(
        index = config['index'],
    ))

@app.command(name='list')
def list_content(
        config: str = typer.Option('config.toml'),
        with_tags: bool = typer.Option(False),
        full_path: bool = typer.Option(False),
):
    config = toml.load(config)
    
    index_dict = funcs.load_index(config['index'])
            
    for key, tags in index_dict.items():
        if full_path: key = Path(os.path.abspath(config['storage'])).joinpath(key)
        
        if with_tags:
            print('{key} {tags}'.format(
                key=key,
                tags=' '.join(tags),
            ))
        else:
            print(key)

@app.command(name='reset')
def reset(
        config: str = typer.Option('config.toml'),
):
    config = toml.load(config)
    
    funcs.write_index(config['index'], {})    
    shutil.rmtree(config['storage'])
    os.mkdir(config['storage'])

    print('Reset {storage} and {index}'.format(
        storage = config['storage'],
        index = config['index'],
    ))

if __name__ == '__main__': app()

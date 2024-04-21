#!/usr/bin/env python3

import typer
import os
import shutil
from pathlib import Path
import datetime
import toml
import tabulate

import funcs

from typing import List

app = typer.Typer(pretty_exceptions_enable=False)

@app.command(name='add')
def command_add(
        files: List[str] = typer.Argument(),
        config: str = typer.Option('config.toml'),
        tags: str = typer.Option(''),
):
    config = toml.load(config)
    tags = [tag for tag in sorted(set(tags.split(' '))) if len(tag) > 0]
    index_dict = funcs.load_index(config['index'])
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    commit_path = Path(config['storage']).joinpath(timestamp)
    os.mkdir(commit_path)

    for file in files:
        commit_path_file = Path(commit_path).joinpath(Path(file).name)
        try:
            shutil.copy(file, commit_path_file)
        except:
            shutil.copytree(file, commit_path_file)
        
        parent = Path(commit_path_file).parent.name
        name = Path(commit_path_file).name
        local_filepath = str(Path(parent).joinpath(name))
        index_dict[local_filepath] = tags
    
    funcs.write_index(config['index'], index_dict)

@app.command(name='tags')
def command_tags(
        config: str = typer.Option(),
):
    config = toml.load(config)
    index_dict = funcs.load_index(config['index'])
    values = sorted(set(x for l in index_dict.values() for x in l))
    print(' '.join(values))

@app.command(name='get')
def command_get(
        config: str = typer.Option(),
        tags_any: str = typer.Option('', '--any'),
        tags_all: str = typer.Option('', '--all'),
        tags_none: str = typer.Option('', '--none'),
):
    config = toml.load(config)
    index_dict = funcs.load_index(config['index'])

    tags_any = [tag for tag in tags_any.split(' ') if len(tag) > 0]
    tags_all = [tag for tag in tags_all.split(' ') if len(tag) > 0]
    tags_none = [tag for tag in tags_none.split(' ') if len(tag) > 0]
    
    keys = list(index_dict.keys())

    if len(tags_any) > 0:
        keys = [
            key for key in keys
            if any(tag in index_dict[key] for tag in tags_any)
        ]
    if len(tags_all) > 0:
        keys = [
            key for key in keys
            if all(tag in index_dict[key] for tag in tags_all)
        ]
    if len(tags_none) > 0:
        keys = [
            key for key in keys
            if all(tag not in index_dict[key] for tag in tags_none)
        ]

    headers = ['Commit', 'File', 'Tags']
    rows = [[
        Path(key).parent, Path(key).name, ' '.join(index_dict[key])
    ] for key in keys]
    table = tabulate.tabulate(rows, headers) #tablefmt='rst'
    print(table)

@app.command(name='clear')
def command_clear(
        config: str = typer.Option('config.toml'),
):
    config = toml.load(config)
    
    funcs.write_index(config['index'], {})    
    shutil.rmtree(config['storage'])
    os.mkdir(config['storage'])

if __name__ == '__main__': app()

"""
Command line interface fot the test generator.

This is invoked by running python -m test_cl <command>
"""
#   Copyright 2023 RoaldO
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import typing as tg
from pathlib import Path

import click

from test_cl import TestGenerator


@click.group
def _cli():
    """ proxy function for the multiple commands that will be invocable """


@_cli.command()
@click.argument('project_root', required=False, default=None)
def generate(project_root: tg.Optional[str]):
    """ starts the process to generate all resources """
    TestGenerator(
        project_root=Path(project_root) if project_root else Path.cwd(),
    ).run()


_cli()

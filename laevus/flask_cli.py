# This file is part of Leavus.
#
# Leavus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leavus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leavus. If not, see <http://www.gnu.org/licenses/>.

# To use this script with Flask, you should assign its path to the FLASK_APP environment variable
#
#     > export FLASK_APP=/path/to/flask_cli.py
#
# then you can simply run `flask run`. See <http://flask.pocoo.org/docs/0.12/cli/> for more
# information.

import click

from laevus import create_app, read_config
from laevus.model import db

config = read_config()
app = create_app(config)


@app.cli.command()
def initdb():
    click.echo('-> Initializing database...')
    db.create_all()
    click.echo('-> Database initialized.')

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

from contextlib import contextmanager
import csv
import os

import click

from laevus import create_app, read_config
from laevus.model import db


config = read_config()
app = create_app(config)


@contextmanager
def sqla_raw_conn():
    """Context manager returning a raw SQLAlchemy connection to the current database."""
    cnx = db.engine.raw_connection()
    try:
        yield cnx
    except Exception:
        cnx.rollback()
        raise
    else:
        cnx.commit()
    finally:
        cnx.close()


@app.cli.command()
def initdb():
    click.echo('-> Initializing database...')
    db.create_all()
    click.echo('-> Database initialized.')


@app.cli.command()
@click.option('--src', prompt='Groups CSV file',
              help=('Path to the CSV file containing groups, their identifiers, their order, '
                    'and their relationships'))
def import_groups(src):
    srcpath = os.path.abspath(os.path.expanduser(src))
    click.echo('-> Importing groups from file {0}...'.format(srcpath))
    with open(srcpath) as f:
        dialect = csv.Sniffer().sniff(f.readline())
        with sqla_raw_conn() as cnx:
            with cnx.cursor() as cur:
                cur.copy_from(f, 'public.group', sep=dialect.delimiter, null='')
    click.echo('-> Groups imported.')

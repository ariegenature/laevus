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
import io
import os

import click

from laevus import create_app, read_config
from laevus.model import WildLifeGroup, db


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


@app.cli.command()
@click.option('--src', prompt='Taxons CSV file',
              help=('Path to the CSV file containing taxons, their identifiers, their groups, '
                    'and their names'))
def import_taxons(src):
    srcpath = os.path.abspath(os.path.expanduser(src))
    click.echo('-> Importing taxons from file {0}...'.format(srcpath))
    group_name2id = dict((group.name, group.id) for group in WildLifeGroup.query.all())
    if not group_name2id:
        raise RuntimeError('Empty group table. Please import groups first using the '
                           '`import_groups` command')
    with open(srcpath) as f:
        dialect = csv.Sniffer().sniff(f.readline())
    # First pass reading file to import only taxon table
    taxons_csv = io.StringIO()  # in-memory file that will be COPY FROM into db
    taxons_writer = csv.writer(taxons_csv, delimiter='\t')
    with open(srcpath) as f:
        dict_reader = csv.DictReader(f, dialect=dialect)
        for row_dict in dict_reader:
            taxons_writer.writerow([row_dict['taxref_id'], group_name2id[row_dict['group']]])
    # Second pass reading file to import names
    scientific_names_csv = io.StringIO()
    common_names_csv = io.StringIO()
    scientific_names_writer = csv.writer(scientific_names_csv, delimiter='\t')
    common_names_writer = csv.writer(common_names_csv, delimiter='\t')
    with open(srcpath) as f:
        dict_reader = csv.DictReader(f, dialect=dialect)
        for row_dict in dict_reader:
            taxref_id = row_dict['taxref_id']
            scientific_names_writer.writerow([row_dict['main_name'], True, taxref_id])
            for scientific_name in row_dict['scientific_names'].split(';'):
                if scientific_name:
                    scientific_names_writer.writerow([scientific_name, False, taxref_id])
            for common_name in row_dict['common_names'].split(';'):
                if common_name:
                    common_names_writer.writerow([common_name, taxref_id])
    taxons_csv.seek(0)
    scientific_names_csv.seek(0)
    common_names_csv.seek(0)
    with sqla_raw_conn() as cnx:
        with cnx.cursor() as cur:
            cur.copy_from(taxons_csv, 'public.taxon', columns=('id', 'group_id'))
            cur.copy_from(scientific_names_csv, 'public.scientific_name',
                          columns=('value', 'is_preferred', 'taxon_id'))
            cur.copy_from(common_names_csv, 'public.common_name', columns=('value', 'taxon_id'))
    click.echo('-> Taxons successfully imported.')

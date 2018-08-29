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
import subprocess

import anosql
import click

from laevus import create_app, read_config
from laevus.model import User, db
import laevus


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
@click.option('--data', prompt='Data folder',
              help=('Path to the folder containing SQL files with schema and initial data'))
def initdb(data):
    click.echo('-> Initializing database...')
    db.create_all()
    admin_user = User(username='admin', name='Administrator')
    admin_user.set_password('laevus')
    db.session.add(admin_user)
    db.session.commit()
    sql_queries = anosql.load_queries('postgres', os.path.join(data, 'schema.sql'))
    with sqla_raw_conn() as cnx:
        sql_queries.create_views(cnx)
    click.echo('-> Database initialized.')


@app.cli.command(name='import-groups')
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
                cur.copy_from(f, 'public.group', sep=dialect.delimiter, null='\\N')
    click.echo('-> Groups imported.')


@app.cli.command(name='import-taxons')
@click.option('--src', prompt='Taxons CSV file',
              help=('Path to the CSV file containing taxons, their identifiers, their groups, '
                    'and their names'))
def import_taxons(src):
    srcpath = os.path.abspath(os.path.expanduser(src))
    click.echo('-> Importing taxons from file {0}...'.format(srcpath))
    with open(srcpath) as f:
        dialect = csv.Sniffer().sniff(f.readline())
    # First pass reading file to import only taxon table
    taxons_csv = io.StringIO()  # in-memory file that will be COPY FROM into db
    taxons_writer = csv.writer(taxons_csv, delimiter='\t')
    with open(srcpath) as f:
        dict_reader = csv.DictReader(f, dialect=dialect)
        for row_dict in dict_reader:
            taxons_writer.writerow([row_dict['taxref_id'], row_dict['group']])
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


@app.cli.command(name='install-js-deps')
def install_js_deps():
    """Run ``npm install`` for the vue.js client in order to install its JavaScript dependencies."""
    click.echo('-> Installing JavaScript dependencies for the Vue.js client...')
    subprocess.check_call(['npm',
                           '--prefix={0}'.format(os.path.join(os.path.dirname(laevus.__file__),
                                                              'contributejs')),
                           'install'])
    click.echo('-> JavaScript dependencies succesfully installed.')


@app.cli.command(name='build-js-client')
def build_js_client():
    """Execute ``npm run build`` for the vue.js client to build it so that it can be served."""
    click.echo('-> Building the Vue.js client...')
    subprocess.check_call(['npm',
                           '--prefix={0}'.format(os.path.join(os.path.dirname(laevus.__file__),
                                                              'contributejs')),
                           'run',
                           'build'])
    click.echo('-> Vue.js client succesfully built.')

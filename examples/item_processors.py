#
# This file is part of BDC-Catalog.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Represent a basic example how to create a processor and relate with Item object."""

from bdc_catalog import BDCCatalog
from bdc_catalog.models import Collection, Item, Processor, db
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdc'
BDCCatalog(app)

with app.app_context():
    processor = Processor.query().filter(Processor.name == 'Sen2Cor').first()
    if processor is None:
        with db.session.begin_nested():
            processor = Processor()
            processor.name = 'Sen2Cor'
            processor.facility = 'Copernicus Sentinel-2 Level 2A'
            processor.level = 'L2A'
            processor.version = '2.10'
            processor.uri = 'https://step.esa.int/main/snap-supported-plugins/sen2cor/'
            processor.save(commit=False)
        db.session.commit()

    # Attach to an item: Find item
    collection = Collection().get_by_id('S2_L1C-1')
    item: Item = (
        Item.query()
        .filter(Item.collection_id == collection.id,
                Item.name == 'S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627')
        .first()
    )

    item.add_processor(processor)
    item.save()

    print(f'Item {item.name}:')
    print(f'-> Processors: {", ".join([p.name for p in item.processors])}')

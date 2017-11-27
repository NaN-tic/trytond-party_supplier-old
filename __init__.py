# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import party
from . import purchase
from . import product


def register():
    Pool.register(
        party.Party,
        purchase.Purchase,
        product.ProductSupplier,
        module='party_supplier', type_='model')

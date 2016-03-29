# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.tools import grouped_slice
from trytond.transaction import Transaction


__all__ = ['Party']


class Party:
    __metaclass__ = PoolMeta
    __name__ = 'party.party'

    supplier = fields.Boolean('Supplier')

    @classmethod
    def __setup__(cls):
        super(Party, cls).__setup__()
        cls._error_messages.update({
                'uncheck_supplier': ('You cannot uncheck the supplier for a '
                    'party which is associated to purchases.'),
                })
        cls._modify_supplier = [
            ('supplier', 'uncheck_supplier'),
            ]

    @classmethod
    def check_no_purchase(cls, parties, error):
        Purchase = Pool().get('purchase.purchase')
        for sub_parties in grouped_slice(parties):
            purchases = Purchase.search([
                    ('party', 'in', [t.id for t in sub_parties]),
                    ],
                limit=1, order=[])
            if purchases:
                cls.raise_user_error(error)

    @classmethod
    def write(cls, *args):
        if (Transaction().user != 0
                and Transaction().context.get('_check_access')):
            actions = iter(args)
            for parties, values in zip(actions, actions):
                for field, error in cls._modify_supplier:
                    if field in values:
                        cls.check_no_purchase(parties, error)
                        break
        super(Party, cls).write(*args)

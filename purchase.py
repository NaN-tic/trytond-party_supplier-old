# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['Purchase']


class Purchase:
    __metaclass__ = PoolMeta
    __name__ = 'purchase.purchase'

    @classmethod
    def __setup__(cls):
        super(Purchase, cls).__setup__()
        new_domain = ('supplier', '=', True)
        domain = cls.party.domain[:]
        if domain and new_domain not in domain:
            cls.party.domain.extend(new_domain)
        else:
            cls.party.domain = [new_domain]

from odoo import models, fields, api, exceptions
from typing import List, Dict, Any

import logging

_logger = logging.getLogger(__name__)


class Car(models.Model):
    _name = 'odoo_model_advanced.car'
    _description = 'Car'

    name = fields.Char(string='Model')
    license_plate = fields.Char(string='License plate')
    cv = fields.Float(string='CV')
    colour = fields.Char(string='Colour')
    liters = fields.Float(string='Liters')
    under_fuel = fields.Boolean(string='Need to refuel', default=False)
    customer = fields.Many2one(comodel_name='res.users', string='Customer')

    _sql_constraints = [
        ('license_plate_unique', 'UNIQUE(license_plate)', 'License plate must be unique')
    ]

    @api.constrains('cv')
    def _validate_cv(self) -> None:
        if self.cv <= 0:
            raise exceptions.ValidationError('CV cannot be equal or less than zero')

    @api.onchange('liters')
    def _check_under_fuel(self) -> None:
        if self.liters < 50:
            self.under_fuel = True

    @api.depends('liters', 'customer.phone')
    def _check_under_fuel(self) -> None:
        _logger.info('Executing depends...')
        if self.liters < 50:
            self.under_fuel = True

    @api.model_create_multi
    def create(self, values: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        records = super(Car, self).create(values)
        return records

    def create_cars(self):
        car_1 = {
            'name': 'Audo A4',
            'license_plate': 'HCN-456',
            'cv': 130,
            'colour': 'Red',
            'liters': 75
        }
        car_2 = {
            'name': 'Audo A4',
            'license_plate': 'H1N-134',
            'cv': 95,
            'colour': 'Blue',
            'liters': 13
        }
        self.env['odoo_model_advanced.car'].create([car_1, car_2])

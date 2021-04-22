from odoo import models, fields, api, exceptions


class Car(models.Model):
    _name = 'odoo_model_advanced.car'
    _description = 'Car'

    name = fields.Char(string='Model')
    license_plate = fields.Char(string='License plate')
    cv = fields.Float(string='CV')
    colour = fields.Char(string='Colour')
    liters = fields.Float(string='Liters')

    _sql_constraints = [
        ('license_plate_unique', 'UNIQUE(license_plate)', 'License plate must be unique')
    ]
from odoo import models, fields, api, exceptions

import logging as logger

logger.basicConfig(level=logger.INFO)


class Car(models.Model):
    _name = 'odoo_model_advanced.car'
    _description = 'Car'

    name = fields.Char(string='Model')
    license_plate = fields.Char(string='License plate')
    cv = fields.Float(string='CV')
    colour = fields.Char(string='Colour')
    liters = fields.Float(string='Liters')
    under_fuel = fields.Boolean(string='Need to refuel', compute='_compute_under_fuel')
    customer = fields.Many2one(comodel_name='res.users', string='Customer')
    group_id = fields.Integer(string='Group')

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
        else:
            self.under_fuel = False

    @api.depends('liters', 'customer.phone')
    def _check_under_fuel(self) -> None:
        _logger.info('Executing depends...')
        if self.liters < 50:
            self.under_fuel = True
        else:
            self.under_fuel = False

    @api.model_create_multi
    def create(self, values: list) -> list:
        records = super(Car, self).create(values)
        return records

    def create_cars(self) -> None:
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

    def _compute_under_fuel(self) -> None:
        if self.liters < 50:
            self.under_fuel = True
        else:
            self.under_fuel = False

    @api.model
    def create(self, car: dict) -> dict:
        car['colour'] = 'Black'
        record = super(Car, self).create(car)
        return record

    def filter(self) -> None:
        cars = self.env['odoo_model_advanced.car'].search([])
        filtered_cars = cars.filtered(lambda c: c.cv >= 90)
        self.print_cars(filtered_cars)

    def map(self) -> None:
        cars = self.env['odoo_model_advanced.car'].search([])
        mapped_cars = cars.mapped(lambda c: c.liters / 1000.0)
        logger.info(f'Mapped cars: {mapped_cars}')

    def sort(self) -> None:
        cars = self.env['odoo_model_advanced.car'].search([])
        sorted_cars = cars.sorted(key=lambda c: c.cv, reverse=True)
        self.print_cars(sorted_cars)

    def get_average_cv(self):
        grouped_cars = self.read_group([('cv', '>', '85')], ['cv:avg'], ['group_id'])
        logger.info(f'Grouped cars: {grouped_cars}')

    def print_cars(self, cars: list) -> None:
        for car in cars:
            logger.info(f'{car.name} {car.cv} {car.liters}')

    def recordset_operations(self) -> None:
        r1 = self.search([('group_id', '=', '1')])
        r2 = self.search([('group_id', '=', '1')])
        r3 = r1 + r2
        self.print_recordset(r3)
        logger.info('**********')
        logger.info(r1 == r2)

    def print_recordset(self, recordset: list) -> None:
        for record in recordset:
            logger.info(f'{record.name} {record.cv} {record.liters}')

    def get_average_cv_sql(self):
        sql = 'SELECT AVG(car.cv) FROM odoo_model_advanced_car AS car'
        self.env.cr.execute(sql)
        result = self.env.cr.fetchall()
        logger.info(result)

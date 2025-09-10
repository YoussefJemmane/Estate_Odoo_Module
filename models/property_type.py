from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name asc"

    name = fields.Char(string="Title", required=True, help="The main title for a property type")

    property_ids = fields.One2many(
            "estate.property",
            "property_type_id",
            string="Property"
    )

    _sql_constraints = [
            ("name_uniq", "unique(name)" , 'A property type with this name already exists.')
    ]


from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name asc"

    name = fields.Char(string="Title", required=True)
    
    property_ids = fields.Many2many("estate.property", string="Properties")
    
    _sql_constraints = [
            ("name_uniq", "unique(name)", "A property tag name must be unique.")
    ]


from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
            string = "Status",
            selection = [
                ("accepted", "Accepted"),
                ("refused", "Refused")
            ],
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    _sql_constraints = [
            ("check_price" , "CHECK(price >0)" , "The price must be positive")
    ]

    def action_accept(self):
        for offer in self:
            if "accepted" in offer.property_id.offer_ids.mapped("status"):
                raise UserError("An offer has already been accepted for this property") 

            offer.status = "accepted"

            offer.property_id.state="offer_accepted"
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True


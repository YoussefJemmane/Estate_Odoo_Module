from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(
        string="Title",
        required=True,
        help="The main title for the property."
    )
    description = fields.Text(
        string="Description",
        help="A detailed description of the property."
    )
    postcode = fields.Char(
        string="Postcode",
        help="The postal code of the property's location."
    )
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.today,
        help="The date from which the property is available for sale."
    )
    expected_price = fields.Float(
        string="Expected Price",
        required=True,
        help="The asking price for the property."
    )
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False,
        help="The final price the property was sold for. Set automatically when an offer is accepted."
    )
    bedrooms = fields.Integer(
        string="Bedrooms",
        default=2,
        help="The number of bedrooms in the property."
    )
    living_area = fields.Integer(
        string="Living Area (sqm)",
        help="The total habitable area in square meters."
    )
    garage = fields.Boolean(
        string="Garage",
        help="Check this box if the property includes a garage."
    )
    garden = fields.Boolean(
        string="Garden",
        help="Check this box if the property includes a garden."
    )
    garden_area = fields.Integer(
        string="Garden Area (sqm)",
        help="The area of the garden in square meters."
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new',
        help="The current status of the property."
    )
    
    property_type_id = fields.Many2one(
            "estate.property.type",
            string="Property Type",
            help="Categorize the property (e.g., House, Apartment)."
    )
    tag_ids = fields.Many2many(
            "estate.property.tag",
            string="Tags",
            help="Select tags that apply to this property (e.g., Cozy, Renovated)."
    )
    offer_ids = fields.One2many(
            "estate.property.offer",
            "property_id",
            string="Offers",
             help="A list of all offers received for this property."
    )
    
    total_area = fields.Integer(
            string="Total Area (sqm)",
            compute="_compute_total_area",
            help="Total area is the sum of the living area and the garden area. This is calculated automatically."
    )

    _sql_constraints = [
            ("check_expected_price", "CHECK(expected_price > 0)", 'The expected price must be strictly positive.')
            ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price must be positive.") 
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for prop in self:
            if prop.selling_price and prop.selling_price < prop.expected_price * 0.9:
                raise ValidationError("The selling price cannot be less than 90% of the expected price.")

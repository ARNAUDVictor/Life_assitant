from datetime import datetime
from models import db

class CrowdlendingPlatform(db.Model):
    __tablename__ = 'crowdlending_platform'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), default="#eeeeee")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE", name="fk_crowdlending_platform_user"), nullable=False)
    user = db.relationship("User", backref="crowdlending_platforms")


    def __repr__(self):
        return f"<CrowdlendingPlatform {self.name}>"
    

class CrowdlendingProject(db.Model):
    __tablename__ = "crowdlending_project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contract_number = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="en_cours")

    platform_id = db.Column(db.Integer, db.ForeignKey("crowdlending_platform.id", ondelete="CASCADE", name="fk_crowdlending_project_crowdlending_platform"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE", name="fk_crowdlending_project_user"), nullable=False)

    date = db.Column(db.Date, nullable=False)

    platform = db.relationship("CrowdlendingPlatform", backref="crowdlending_projects")
    user = db.relationship("User", backref="crowdlending_projects")

    def __repr__(self):
        return f"<CrowdlendingProject {self.name}>"
    

class CrowdlendingTransaction(db.Model):
    __tablename__ = "crowdlending_transation"
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    capital_reimbursed = db.Column(db.Numeric(10, 2), default=0)
    interests_reimbursed = db.Column(db.Numeric(10, 2), default=0)
    tax_deductions = db.Column(db.Numeric(10, 2), default=0)
    net_amount = db.Column(db.Numeric(10, 2), default=0)

    project_id = db.Column(db.Integer, db.ForeignKey("crowdlending_project.id", ondelete="CASCADE", name="fk_crowdlending_transaction_project"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE", name="fk_crowdlending_transaction_user"), nullable=False)

    #relations
    project = db.relationship("CrowdlendingProject", backref="crowdlending_transactions")
    user = db.relationship("User", backref="crowdlending_transactions")

    def __repr__(self):
        return f"<CrowdlendingTransaction {self.operation_type} {self.amount}€>"

    
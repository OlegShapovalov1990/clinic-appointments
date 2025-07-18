"""Initial tables

Revision ID: 70ab0924383d
Revises: 
Create Date: 2025-07-05 12:33:53.411752

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "70ab0924383d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "appointments",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("patient_name", sa.String(), nullable=False),
        sa.Column("doctor_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
        comment="Table for storing doctor appointments",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("appointments")
    # ### end Alembic commands ###

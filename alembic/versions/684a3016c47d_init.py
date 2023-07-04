"""init

Revision ID: 684a3016c47d
Revises: 
Create Date: 2023-07-04 17:17:48.083534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '684a3016c47d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('neural_models',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('responses',
    sa.Column('image_id', sa.String(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('recognized_image_id', sa.Integer(), nullable=False),
    sa.Column('generated_at', sa.DateTime(), nullable=False),
    sa.Column('model_id', sa.Uuid(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['model_id'], ['neural_models.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('image_id', 'model_id')
    )
    op.create_table('recognized_objects',
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('response_id', sa.Uuid(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['response_id'], ['responses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recognized_objects')
    op.drop_table('responses')
    op.drop_table('neural_models')
    # ### end Alembic commands ###

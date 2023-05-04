"""tabela fale-conosco

Revision ID: 0d35c5d13cbe
Revises: f39facfeaff2
Create Date: 2023-05-04 01:05:42.561914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d35c5d13cbe'
down_revision = 'f39facfeaff2'
branch_labels = None
depends_on = None


def upgrade():
    sql = """
    CREATE TABLE IF NOT EXISTS `contact_us` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(200) NOT NULL,
    `phone` VARCHAR(13) NOT NULL,
    `phone_is_whatsapp` TINYINT NOT NULL DEFAULT 1,
    `email` VARCHAR(200) NOT NULL,
    `reason` VARCHAR(200) NOT NULL,
    `description` TEXT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT now(),
    `updated_at` DATETIME NULL,
    PRIMARY KEY (`id`))"""
    op.execute(sql)
    


def downgrade():
    op.execute("DROP TABLE contact_us")

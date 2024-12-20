"""improve_article_versions

Revision ID: 3e1c63916599
Revises: 19da2bc01207
Create Date: 2024-10-22 16:01:13.776478

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e1c63916599"
down_revision: Union[str, None] = "19da2bc01207"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("articles", sa.Column("content", sa.String(), nullable=False))
    op.add_column("articles", sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.add_column("articles", sa.Column("author_id", sa.UUID(), nullable=False))
    op.drop_constraint(
        "articles_current_version_id_fkey", "articles", type_="foreignkey"
    )
    op.drop_constraint("articles_user_id_fkey", "articles", type_="foreignkey")
    op.create_foreign_key(None, "articles", "users", ["author_id"], ["id"])
    op.drop_column("articles", "tags")
    op.drop_column("articles", "user_id")
    op.drop_column("articles", "current_version_id")
    op.alter_column(
        "users",
        "motivation",
        existing_type=sa.TEXT(),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.add_column("versions", sa.Column("title", sa.String(), nullable=False))
    op.add_column("versions", sa.Column("section", sa.String(), nullable=True))
    op.add_column("versions", sa.Column("preview", sa.String(), nullable=False))
    op.add_column("versions", sa.Column("version_number", sa.Integer(), nullable=False))
    op.add_column("versions", sa.Column("article_id", sa.UUID(), nullable=False))
    op.add_column("versions", sa.Column("editor_id", sa.UUID(), nullable=False))
    op.alter_column(
        "versions",
        "content",
        existing_type=sa.TEXT(),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.drop_constraint("versions_user_id_fkey", "versions", type_="foreignkey")
    op.create_foreign_key(None, "versions", "users", ["editor_id"], ["id"])
    op.create_foreign_key(None, "versions", "articles", ["article_id"], ["id"])
    op.drop_column("versions", "user_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "versions", sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False)
    )
    op.drop_constraint(None, "versions", type_="foreignkey")
    op.drop_constraint(None, "versions", type_="foreignkey")
    op.create_foreign_key(
        "versions_user_id_fkey", "versions", "users", ["user_id"], ["id"]
    )
    op.alter_column(
        "versions",
        "content",
        existing_type=sa.String(),
        type_=sa.TEXT(),
        existing_nullable=False,
    )
    op.drop_column("versions", "editor_id")
    op.drop_column("versions", "article_id")
    op.drop_column("versions", "version_number")
    op.drop_column("versions", "preview")
    op.drop_column("versions", "section")
    op.drop_column("versions", "title")
    op.alter_column(
        "users",
        "motivation",
        existing_type=sa.String(),
        type_=sa.TEXT(),
        existing_nullable=False,
    )
    op.add_column(
        "articles",
        sa.Column("current_version_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "articles", sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False)
    )
    op.add_column(
        "articles", sa.Column("tags", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_constraint(None, "articles", type_="foreignkey")
    op.create_foreign_key(
        "articles_user_id_fkey", "articles", "users", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        "articles_current_version_id_fkey",
        "articles",
        "versions",
        ["current_version_id"],
        ["id"],
    )
    op.drop_column("articles", "author_id")
    op.drop_column("articles", "updated_at")
    op.drop_column("articles", "content")
    # ### end Alembic commands ###

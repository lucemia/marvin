"""Initial migration

Revision ID: 4d10660798b7
Revises: 
Create Date: 2023-04-01 17:39:22.762982

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op
from marvin.infra.database import JSONType

# revision identifiers, used by Alembic.
revision = "4d10660798b7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()

    # because people may have been using marvin prior to to this migration being
    # introduced, we need to make sure that the tables we're creating don't
    # already exist
    if "bot_config" not in tables:
        op.create_table(
            "bot_config",
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("plugins", JSONType(), server_default="[]", nullable=False),
            sa.Column(
                "input_transformers", JSONType(), server_default="[]", nullable=False
            ),
            sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column(
                "personality", sqlmodel.sql.sqltypes.AutoString(), nullable=False
            ),
            sa.Column(
                "instructions", sqlmodel.sql.sqltypes.AutoString(), nullable=False
            ),
            sa.Column(
                "profile_picture", sqlmodel.sql.sqltypes.AutoString(), nullable=True
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_bot_config")),
        )
        op.create_index(
            op.f("ix_bot_config__created_at"),
            "bot_config",
            ["created_at"],
            unique=False,
        )
        op.create_index(
            op.f("ix_bot_config__updated_at"),
            "bot_config",
            ["updated_at"],
            unique=False,
        )
        op.create_index("uq_bot_config__name", "bot_config", ["name"], unique=True)

    if "thread" not in tables:
        op.create_table(
            "thread",
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("context", JSONType(), server_default="{}", nullable=False),
            sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("lookup_key", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.Column("is_visible", sa.Boolean(), nullable=False),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_thread")),
        )
        op.create_index(
            op.f("ix_thread__created_at"), "thread", ["created_at"], unique=False
        )
        op.create_index(
            op.f("ix_thread__is_visible"), "thread", ["is_visible"], unique=False
        )
        op.create_index(
            op.f("ix_thread__updated_at"), "thread", ["updated_at"], unique=False
        )
        op.create_index("uq_thread__lookup_key", "thread", ["lookup_key"], unique=True)

    if "message" not in tables:
        op.create_table(
            "message",
            sa.Column(
                "timestamp",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("data", JSONType(), server_default="{}", nullable=False),
            sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("role", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("content", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.Column("bot_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.Column("thread_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.ForeignKeyConstraint(
                ["thread_id"],
                ["thread.id"],
                name=op.f("fk_message__thread_id__thread"),
                ondelete="CASCADE",
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_message")),
        )
        op.create_index(
            "ix_message__thread_id_timestamp",
            "message",
            ["thread_id", "timestamp"],
            unique=False,
        )
        op.create_index(
            op.f("ix_message__timestamp"), "message", ["timestamp"], unique=False
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_message__timestamp"), table_name="message")
    op.drop_index("ix_message__thread_id_timestamp", table_name="message")
    op.drop_table("message")
    op.drop_index("uq_thread__lookup_key", table_name="thread")
    op.drop_index(op.f("ix_thread__updated_at"), table_name="thread")
    op.drop_index(op.f("ix_thread__is_visible"), table_name="thread")
    op.drop_index(op.f("ix_thread__created_at"), table_name="thread")
    op.drop_table("thread")
    op.drop_index("uq_bot_config__name", table_name="bot_config")
    op.drop_index(op.f("ix_bot_config__updated_at"), table_name="bot_config")
    op.drop_index(op.f("ix_bot_config__created_at"), table_name="bot_config")
    op.drop_table("bot_config")
    # ### end Alembic commands ###

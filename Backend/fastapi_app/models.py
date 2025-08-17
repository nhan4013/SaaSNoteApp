from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class AuthGroup(Base):
    __tablename__ = 'auth_group'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='auth_group_pkey'),
        UniqueConstraint('name', name='auth_group_name_key'),
        Index('auth_group_name_a6ea08ec_like', 'name')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(150))

    auth_user_groups: Mapped[List['AuthUserGroups']] = relationship('AuthUserGroups', back_populates='group')
    auth_group_permissions: Mapped[List['AuthGroupPermissions']] = relationship('AuthGroupPermissions', back_populates='group')


class AuthUser(Base):
    __tablename__ = 'auth_user'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='auth_user_pkey'),
        UniqueConstraint('username', name='auth_user_username_key'),
        Index('auth_user_username_6821ab7c_like', 'username')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    password: Mapped[str] = mapped_column(String(128))
    is_superuser: Mapped[bool] = mapped_column(Boolean)
    username: Mapped[str] = mapped_column(String(150))
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(254))
    is_staff: Mapped[bool] = mapped_column(Boolean)
    is_active: Mapped[bool] = mapped_column(Boolean)
    date_joined: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    last_login: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    app_notes: Mapped[List['AppNotes']] = relationship('AppNotes', back_populates='user')
    app_tags: Mapped[List['AppTags']] = relationship('AppTags', back_populates='user')
    auth_user_groups: Mapped[List['AuthUserGroups']] = relationship('AuthUserGroups', back_populates='user')
    django_admin_log: Mapped[List['DjangoAdminLog']] = relationship('DjangoAdminLog', back_populates='user')
    auth_user_user_permissions: Mapped[List['AuthUserUserPermissions']] = relationship('AuthUserUserPermissions', back_populates='user')


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='django_content_type_pkey'),
        UniqueConstraint('app_label', 'model', name='django_content_type_app_label_model_76bd3d3b_uniq')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    app_label: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))

    auth_permission: Mapped[List['AuthPermission']] = relationship('AuthPermission', back_populates='content_type')
    django_admin_log: Mapped[List['DjangoAdminLog']] = relationship('DjangoAdminLog', back_populates='content_type')


class DjangoMigrations(Base):
    __tablename__ = 'django_migrations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='django_migrations_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    app: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    applied: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class DjangoSession(Base):
    __tablename__ = 'django_session'
    __table_args__ = (
        PrimaryKeyConstraint('session_key', name='django_session_pkey'),
        Index('django_session_expire_date_a5c62663', 'expire_date'),
        Index('django_session_session_key_c0390e0f_like', 'session_key')
    )

    session_key: Mapped[str] = mapped_column(String(40), primary_key=True)
    session_data: Mapped[str] = mapped_column(Text)
    expire_date: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class AppNotes(Base):
    __tablename__ = 'app_notes'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['auth_user.id'], deferrable=True, initially='DEFERRED', name='app_notes_user_id_09245a1b_fk_auth_user_id'),
        PrimaryKeyConstraint('id', name='app_notes_pkey'),
        Index('app_notes_user_id_09245a1b', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    user_id: Mapped[int] = mapped_column(Integer)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    user: Mapped['AuthUser'] = relationship('AuthUser', back_populates='app_notes')
    app_notes_tags: Mapped[List['AppNotesTags']] = relationship('AppNotesTags', back_populates='notes')


class AppTags(Base):
    __tablename__ = 'app_tags'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['auth_user.id'], deferrable=True, initially='DEFERRED', name='app_tags_user_id_10ce0f3c_fk_auth_user_id'),
        PrimaryKeyConstraint('id', name='app_tags_pkey'),
        Index('app_tags_user_id_10ce0f3c', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(Integer)
    user: Mapped['AuthUser'] = relationship('AuthUser', back_populates='app_tags')
    app_notes_tags: Mapped[List['AppNotesTags']] = relationship('AppNotesTags', back_populates='tags')


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        ForeignKeyConstraint(['content_type_id'], ['django_content_type.id'], deferrable=True, initially='DEFERRED', name='auth_permission_content_type_id_2f476e4b_fk_django_co'),
        PrimaryKeyConstraint('id', name='auth_permission_pkey'),
        UniqueConstraint('content_type_id', 'codename', name='auth_permission_content_type_id_codename_01ab375a_uniq'),
        Index('auth_permission_content_type_id_2f476e4b', 'content_type_id')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    content_type_id: Mapped[int] = mapped_column(Integer)
    codename: Mapped[str] = mapped_column(String(100))

    content_type: Mapped['DjangoContentType'] = relationship('DjangoContentType', back_populates='auth_permission')
    auth_group_permissions: Mapped[List['AuthGroupPermissions']] = relationship('AuthGroupPermissions', back_populates='permission')
    auth_user_user_permissions: Mapped[List['AuthUserUserPermissions']] = relationship('AuthUserUserPermissions', back_populates='permission')


class AuthUserGroups(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        ForeignKeyConstraint(['group_id'], ['auth_group.id'], deferrable=True, initially='DEFERRED', name='auth_user_groups_group_id_97559544_fk_auth_group_id'),
        ForeignKeyConstraint(['user_id'], ['auth_user.id'], deferrable=True, initially='DEFERRED', name='auth_user_groups_user_id_6a12ed8b_fk_auth_user_id'),
        PrimaryKeyConstraint('id', name='auth_user_groups_pkey'),
        UniqueConstraint('user_id', 'group_id', name='auth_user_groups_user_id_group_id_94350c0c_uniq'),
        Index('auth_user_groups_group_id_97559544', 'group_id'),
        Index('auth_user_groups_user_id_6a12ed8b', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(Integer)

    group: Mapped['AuthGroup'] = relationship('AuthGroup', back_populates='auth_user_groups')
    user: Mapped['AuthUser'] = relationship('AuthUser', back_populates='auth_user_groups')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        CheckConstraint('action_flag >= 0', name='django_admin_log_action_flag_check'),
        ForeignKeyConstraint(['content_type_id'], ['django_content_type.id'], deferrable=True, initially='DEFERRED', name='django_admin_log_content_type_id_c4bce8eb_fk_django_co'),
        ForeignKeyConstraint(['user_id'], ['auth_user.id'], deferrable=True, initially='DEFERRED', name='django_admin_log_user_id_c564eba6_fk_auth_user_id'),
        PrimaryKeyConstraint('id', name='django_admin_log_pkey'),
        Index('django_admin_log_content_type_id_c4bce8eb', 'content_type_id'),
        Index('django_admin_log_user_id_c564eba6', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    action_time: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    object_repr: Mapped[str] = mapped_column(String(200))
    action_flag: Mapped[int] = mapped_column(SmallInteger)
    change_message: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(Integer)
    object_id: Mapped[Optional[str]] = mapped_column(Text)
    content_type_id: Mapped[Optional[int]] = mapped_column(Integer)

    content_type: Mapped[Optional['DjangoContentType']] = relationship('DjangoContentType', back_populates='django_admin_log')
    user: Mapped['AuthUser'] = relationship('AuthUser', back_populates='django_admin_log')


class AppNotesTags(Base):
    __tablename__ = 'app_notes_tags'
    __table_args__ = (
        ForeignKeyConstraint(['notes_id'], ['app_notes.id'], deferrable=True, initially='DEFERRED', name='app_notes_tags_notes_id_85735509_fk_app_notes_id'),
        ForeignKeyConstraint(['tags_id'], ['app_tags.id'], deferrable=True, initially='DEFERRED', name='app_notes_tags_tags_id_d3ded705_fk_app_tags_id'),
        PrimaryKeyConstraint('id', name='app_notes_tags_pkey'),
        UniqueConstraint('notes_id', 'tags_id', name='app_notes_tags_notes_id_tags_id_95ddb8e1_uniq'),
        Index('app_notes_tags_notes_id_85735509', 'notes_id'),
        Index('app_notes_tags_tags_id_d3ded705', 'tags_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    notes_id: Mapped[int] = mapped_column(BigInteger)
    tags_id: Mapped[int] = mapped_column(BigInteger)

    notes: Mapped['AppNotes'] = relationship('AppNotes', back_populates='app_notes_tags')
    tags: Mapped['AppTags'] = relationship('AppTags', back_populates='app_notes_tags')


class AuthGroupPermissions(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        ForeignKeyConstraint(['group_id'], ['auth_group.id'], deferrable=True, initially='DEFERRED', name='auth_group_permissions_group_id_b120cbf9_fk_auth_group_id'),
        ForeignKeyConstraint(['permission_id'], ['auth_permission.id'], deferrable=True, initially='DEFERRED', name='auth_group_permissio_permission_id_84c5c92e_fk_auth_perm'),
        PrimaryKeyConstraint('id', name='auth_group_permissions_pkey'),
        UniqueConstraint('group_id', 'permission_id', name='auth_group_permissions_group_id_permission_id_0cd325b0_uniq'),
        Index('auth_group_permissions_group_id_b120cbf9', 'group_id'),
        Index('auth_group_permissions_permission_id_84c5c92e', 'permission_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer)
    permission_id: Mapped[int] = mapped_column(Integer)

    group: Mapped['AuthGroup'] = relationship('AuthGroup', back_populates='auth_group_permissions')
    permission: Mapped['AuthPermission'] = relationship('AuthPermission', back_populates='auth_group_permissions')


class AuthUserUserPermissions(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        ForeignKeyConstraint(['permission_id'], ['auth_permission.id'], deferrable=True, initially='DEFERRED', name='auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm'),
        ForeignKeyConstraint(['user_id'], ['auth_user.id'], deferrable=True, initially='DEFERRED', name='auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id'),
        PrimaryKeyConstraint('id', name='auth_user_user_permissions_pkey'),
        UniqueConstraint('user_id', 'permission_id', name='auth_user_user_permissions_user_id_permission_id_14a6b632_uniq'),
        Index('auth_user_user_permissions_permission_id_1fbb5f2c', 'permission_id'),
        Index('auth_user_user_permissions_user_id_a95ead1b', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    permission_id: Mapped[int] = mapped_column(Integer)

    permission: Mapped['AuthPermission'] = relationship('AuthPermission', back_populates='auth_user_user_permissions')
    user: Mapped['AuthUser'] = relationship('AuthUser', back_populates='auth_user_user_permissions')

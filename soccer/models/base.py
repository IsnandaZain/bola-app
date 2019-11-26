from flask_sqlalchemy import SQLAlchemy, BaseQuery, _BoundDeclarativeMeta, _QueryProperty, Model, Pagination
from sqlalchemy.ext.declarative import declarative_base

__author__ = "isnanda.muhammadzain@sebangsa.com"


class SoccerBaseQuery(BaseQuery):
    """Extending untuk menambahkan fungsionalitas query"""

    def paginate_limit(self, page=None, per_page=None, limit=None) -> Pagination:
        """Return paginate object

        Args:
            page: number of page
            per_page: item per page
            limit: limit item per page

        Returns:
            Pagination object
        """
        page = page or 1
        per_page = per_page or 12
        limit = limit if limit else per_page

        items = self.limit(limit).offset( (page-1) * per_page).all()

        # No need to count if we're on the first page and there are fewer
        # items than we expected
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = self.order_by(None).count()

        return Pagination(self, page, per_page, total, items)


class SoccerModel(Model):
    # Change query class with SoccerBaseQuery
    query_class = SoccerBaseQuery


class SoccerDB(SQLAlchemy):

    def __init__(self):
        super().__init__()
    
    def make_declarative_base(self, model, metadata=None):
        """change declarative base"""
        base = declarative_base(cls=SoccerModel, name='Model',
                                metadata=metadata,
                                metaclass=_BoundDeclarativeMeta)

        if not getattr(base, 'query_class', None):
            base.query_class = self.query_class
        
        base.query = _QueryProperty(self)
        return base

    def drop_all(self, bind="__all__", app=None):
        """Drops all tables

        .. versionchanged:: 0.12
            Parameters were added"""
        self.__memory_only(app=app)

        self._execute_for_all_tables(app, bind, "drop_all")

    def create_all(self, bind="__all__", app=None):
        """Creates all tables.

        .. versionchanged:: 0.12
            Parameters were added
        """
        self.__memory_only(app=app)

        self._execute_for_all_tables(app, bin, "create_all")

    def __memory_only(self, app):
        """Override to make sure only drop sqlite memory"""
        database_uri = self.get_app(app).config['SQLALCHEMY_DATABASE_URI']

        if database_uri != "sqlite:///:memory:":
            raise Exception("Cannot drop_all except sqlite:///:memory:")


db = SoccerDB()

__all__ = [db]
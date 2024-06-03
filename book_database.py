from sqlalchemy import MetaData, create_engine, Integer, String, Float, ForeignKey, Column
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

metadata = MetaData()  # Create the metadata variable.
engine = create_engine('sqlite:///book_database', connect_args={'check_same_thread': False}, echo=False)  # echo=False
Base = declarative_base()
db_session = sessionmaker(bind=engine)()  # Start the db_session so that the data can be queried from book_database.


# Table for books.
class Book(Base):
    __tablename__ = 'books'  # Point to the books table.
    # Set all of the columns to their specific variables for books.
    book_id = Column(Integer, primary_key=True)
    book_name = Column(String)
    book_summary = Column(String)
    book_genre = Column(String)
    book_details_data = relationship("BookDetails", backref="books")


# Table for book details.
class BookDetails(Base):
    __tablename__ = 'book_details'  # Point to the book_details table.
    # Set all of the columns to their specific variables for book_details.
    id = Column(Integer, primary_key=True)
    book_id = Column(ForeignKey('books.book_id'))
    book_text = Column(String)


# Retrieving data from the database
def get_books():  # Query all of the book details from the Book table above.
    return db_session.query(Book)


# Retrieving data from the database
def get_specific_book(id):  # Query specific book details from the Book table above based on the id the user chose.
    return db_session.query(Book).filter_by(book_id=id).all()


# Retrieving data from the database
def get_book_details(id):  # Query specific book details from the BookDetails table above based on the id the user chose.
    return db_session.query(BookDetails).filter_by(book_id=id).all()
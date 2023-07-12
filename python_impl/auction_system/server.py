#! /usr/bin/env python3

"""Server setup for Auction System"""
    
import Pyro4
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# SQLAlchemy setup
engine = create_engine("sqlite:///auction.db", connect_args={"check_same_thread": False}, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    auctions = relationship("Auction", back_populates="bidder")


class Auction(Base):
    __tablename__ = "auctions"
    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    current_price = Column(Float, nullable=False)
    bidder_id = Column(Integer, ForeignKey("users.id"))
    bidder = relationship("User", back_populates="auctions")


Base.metadata.create_all(bind=engine)



@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class AuctionServer(object):
    """Class Auction Server
        Defines the RMI Object details for the server
    """
        
    def create_user(self, name: str):
        session = Session()
        user = User(name=name)
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return user.id

    def create_auction(self, item_name, initial_price):
        """create_auction:
            Method for creating an auction
            Args:
                item_name (str) : name of Item
                initial_price (int) : initial price of auction item
            Returns:
                auction_id: id of the auctioned Item
        """
        session = Session()
        auction = Auction(item_name=item_name, current_price=initial_price)
        session.add(auction)
        session.commit()
        session.refresh(auction)
        session.close()
        return auction.id

    def place_bid(self, auction_id, bidder_id, bid_amount):
        """place bid:
            Method for placing a bid on auction
            Args:
                auction_id (int): auction Id
                bidder_id (int): bidder id
                bid_amount (int): bid amount
            Returns:
                Boolean true if bid is placed, false if bid is not placed"""
        session = Session()
        auction = session.query(Auction).get(auction_id)
        if auction:
            if bid_amount > auction.current_price:
                bidder = session.query(User).get(bidder_id)
                if bidder:
                    auction.current_price = bid_amount
                    auction.bidder = bidder
                    session.commit()
                    session.close()
                    return True
            else:
                session.close()
                return False
        else:
            session.close()
            raise ValueError("Invalid auction ID")

    def get_auction_info(self, auction_id):
        """ get auction_info:
            Method for getting information on auction
            Args: 
                auction_id (int): auction Id
            Returns:
                Action saved
        """
        session = Session()
        auction = session.query(Auction).get(auction_id)
        if auction:
            auction_info = {
                "id": auction.id,
                "item_name": auction.item_name,
                "current_price": auction.current_price,
                "bidder_name": auction.bidder.name if auction.bidder else None
                }
            session.close()
            return auction_info
        else:
            session.close()
            raise ValueError("Invalid auction ID")


def main():
    Pyro4.Daemon.serveSimple({
        AuctionServer: 'AuctionServer',
    }, host="127.0.0.1", port=5000, ns=True, verbose=True)


if __name__ == "__main__":
    main()
import pytest
from order_book import OrderBook
from order import Order
def test_unmatched_buy_order_rests_on_book():
    book = OrderBook()
    order = Order(
        order_id = '3749493',
        side = 'buy',
        price = 10000,
        quantity = 3,
        cancelled = False
    )
    book.submit_order(order)
    assert len(book.bids) == 1
    assert book.bids[0][2] == order
    assert len(book.asks) == 0
def test_unmatched_sell_order_rests_on_book():
    book = OrderBook()
    order = Order(
        order_id = '3749494',
        side = 'sell',
        price = 9000,
        quantity =3,
        cancelled = False
    )
    book.submit_order(order)
    assert len(book.bids) == 0
    assert len(book.asks) == 1
    assert book.asks[0][2] == order
def test_get_best_bids_when_empty():
    book = OrderBook()
    order = Order(
        order_id = '3749494',
        side = 'sell',
        price = 9000,
        quantity =3,
        cancelled = False
        )
    book.submit_order(order)
    best_bid = book.get_best_bid()
    assert best_bid is None
def test_get_best_bids_normal():
    book = OrderBook()
    order1 = Order(
        order_id = '1',
        side = 'buy',
        price = 5,
        quantity = 10,
        cancelled = False
    )
    order2 = Order(
        order_id = '2',
        side = 'buy',
        price = 9,
        quantity = 10,
        cancelled= False
    )
    order3 = Order(
        order_id = '3',
        side = 'buy',
        price = 4,
        quantity = 10,
        cancelled = False
    )
    order4 = Order(
        order_id = '4',
        side = 'buy',
        price = 8,
        quantity = 10,
        cancelled = False
    )
    book.submit_order(order1)
    book.submit_order(order2)
    book.submit_order(order3)
    book.submit_order(order4)
    best_bid = book.get_best_bid()
    assert best_bid.price == 9
def test_incoming_buy_partial_fills_resting_sell():
    book = OrderBook()
    order1 = Order(
        order_id = '1',
        side = 'sell',
        price = 100,
        quantity = 10,
        cancelled = False
    )
    order2 = Order(
        order_id = '2',
        side = 'buy',
        price = 100,
        quantity = 4,
        cancelled = False
    )
    book.submit_order(order1)
    book.submit_order(order2) 
    best_ask = book.get_best_ask()
    assert len(book.bids) == 0
    assert len(book.asks) == 1
    assert best_ask.quantity == 6
    assert best_ask.price == 100
    assert best_ask.order_id == '1'
def test_incoming_buy_consumes_resting_sell_and_sets_remainder():
    book = OrderBook()
    order1 = Order(
        order_id = '1',
        side = 'sell',
        price = 100,
        quantity = 10,
        cancelled = False
    )
    order2 = Order(
        order_id = '2',
        side = 'buy',
        price = 100,
        quantity = 40,
        cancelled = False
    )
    book.submit_order(order1)
    book.submit_order(order2) 
    best_bid = book.get_best_bid()
    assert len(book.asks) == 0
    assert len(book.bids) == 1
    assert best_bid.quantity == 30
    assert best_bid.price == 100
    assert best_bid.order_id == '2'

def test_first_in_first_out_buy():
        book = OrderBook()
        order1 = Order(
            order_id = '1',
            side = 'buy',
            quantity = 10,
            price = 100,
            cancelled = False
        )
        order2 = Order(
            order_id = '2',
            side = 'buy',
            quantity = 10,
            price = 100,
            cancelled = False
        )
        order3 = Order(
            order_id = '3',
            side = 'sell',
            quantity = 15,
            price = 100,
            cancelled = False
        )
        book.submit_order(order1)
        book.submit_order(order2)
        book.submit_order(order3)
        best_bid = book.get_best_bid()
        assert len(book.bids) == 1
        assert len(book.asks) == 0
        assert best_bid.order_id =='2'
        assert best_bid.quantity ==5
        assert best_bid.price == 100

def test_first_in_first_out_sell():
        book = OrderBook()
        order1 = Order(
            order_id = '1',
            side = 'sell',
            quantity = 10,
            price = 100,
            cancelled = False
        )
        order2 = Order(
            order_id = '2',
            side = 'sell',
            quantity = 10,
            price = 100,
            cancelled =False
        )
        order3 = Order(
            order_id = '3',
            side = 'buy',
            quantity = 15,
            price = 100,
            cancelled = False
        )
        book.submit_order(order1)
        book.submit_order(order2)
        book.submit_order(order3)
        best_ask = book.get_best_ask()
        assert len(book.bids) == 0
        assert len(book.asks) == 1
        assert best_ask.order_id =='2'
        assert best_ask.quantity ==5
        assert best_ask.price == 100

def test_best_price_executes_first_buy():
        book = OrderBook()
        order1 = Order(
            order_id = '1',
            side = 'sell',
            quantity = 10,
            price = 100,
            cancelled = False
        )
        order2 = Order(
            order_id = '2',
            side = 'sell',
            quantity = 10,
            price = 90,
            cancelled = False
        )
        order3 = Order(
            order_id = '3',
            side = 'buy',
            quantity = 15,
            price = 100,
            cancelled = False
        )
        book.submit_order(order1)
        book.submit_order(order2)
        book.submit_order(order3)
        best_ask = book.get_best_ask()
        assert len(book.bids) == 0
        assert len(book.asks) == 1
        assert best_ask.order_id =='1'
        assert best_ask.quantity ==5
        assert best_ask.price == 100
def test_best_price_executes_first_sell():
        book = OrderBook()
        order1 = Order(
            order_id = '1',
            side = 'buy',
            quantity = 10,
            price = 100,
            cancelled = False
        )
        order2 = Order(
            order_id = '2',
            side = 'buy',
            quantity = 10,
            price = 110,
            cancelled = False
        )
        order3 = Order(
            order_id = '3',
            side = 'sell',
            quantity = 15,
            price = 100,
            cancelled = False
        )
        book.submit_order(order1)
        book.submit_order(order2)
        book.submit_order(order3)
        best_bid = book.get_best_bid()
        assert len(book.bids) == 1
        assert len(book.asks) == 0
        assert best_bid.order_id =='1'
        assert best_bid.quantity ==5
        assert best_bid.price == 100
def test_multi_level_sweep():
    book = OrderBook()
    order1 = Order(
            order_id = '1',
            side = 'sell',
            price = 90,
            quantity = 2,
            cancelled = False
    )
    order2 = Order(
            order_id = '2',
            side = 'sell',
            price = 100,
            quantity = 3,
            cancelled = False
    )
    order3 = Order(
            order_id = '3',
            side = 'sell',
            price = 110,
            quantity = 5,
            cancelled = False
    )
    order4 = Order(
            order_id = '4',
            side = 'buy',
            price = 100,
            quantity = 4,
            cancelled = False 
      )
    book.submit_order(order1)
    book.submit_order(order2)
    book.submit_order(order3)
    book.submit_order(order4)
    best_ask = book.get_best_ask()
    assert len(book.bids) == 0
    assert len(book.asks) == 2
    assert best_ask.price == 100
    assert best_ask.quantity == 1
    assert book.asks[1][2] == order3
def test_trade_history():
     book = OrderBook()
     order1 = Order(
          order_id = '1',
          side = 'sell',
          price = 90,
          quantity = 10,
          cancelled = False
     )
     order2 = Order(
          order_id = '2',
          side = 'buy',
          price = 100,
          quantity = 4,
          cancelled = False
     )
     book.submit_order(order1)
     book.submit_order(order2)
     trade_history = book.trades
     assert trade_history[0]['buy_order'] == '2'
     assert trade_history[0]['sell_order'] == '1'
     assert trade_history[0]['execution_price'] == 90
     assert trade_history[0]['trade_volume'] == 4
def test_cancelled_buy_order_is_removed_from_active_book():
    book = OrderBook()
    order = Order(
        order_id="1",
        side="buy",
        price=100,
        quantity=10,
        cancelled = False
    )
    book.submit_order(order)
    book.cancel_order("1")
    assert book.get_best_bid() is None
def test_cancelled_order_doesnt_appear_at_best_price():
     book = OrderBook()
     order1 = Order(
          order_id = '1',
          side = 'buy',
          price = 100,
          quantity = 10,
          cancelled = False
     )
     order2 = Order(
          order_id = '2',
          side = 'buy',
          price = 50,
          quantity = 10,
          cancelled = False
     )
     book.submit_order(order1)
     book.submit_order(order2)
     book.cancel_order('1')
     best_bid = book.get_best_bid()
     assert best_bid.price == 50
def test_cancelled_order_doesnt_execute_buy():
     book = OrderBook()
     order1 = Order(
          order_id = '1',
          side = 'buy',
          price = 100,
          quantity = 10,
          cancelled = False
     )
     order2 = Order(
          order_id = '2',
          side = 'buy',
          price = 50,
          quantity = 10,
          cancelled = False
     )
     order3 = Order(
          order_id =  '3',
          side = 'sell',
          price = 25,
          quantity = 10,
          cancelled = False
     )
     book.submit_order(order1)
     book.submit_order(order2)
     book.cancel_order('1')
     book.submit_order(order3)
     trade_history = book.trades
     assert trade_history[0]['buy_order'] == '2'
     assert trade_history[0]['execution_price'] == 50
def test_cancelled_order_doesnt_execute_sell():
     book = OrderBook()
     order1 = Order(
          order_id = '1',
          side = 'sell',
          price = 100,
          quantity = 10,
          cancelled = False
     )
     order2 = Order(
          order_id = '2',
          side = 'sell',
          price = 50,
          quantity = 10,
          cancelled = False
     )
     order3 = Order(
          order_id =  '3',
          side = 'buy',
          price = 150,
          quantity = 10,
          cancelled = False
     )
     book.submit_order(order1)
     book.submit_order(order2)
     book.cancel_order('2')
     book.submit_order(order3)
     trade_history = book.trades
     assert trade_history[0]['sell_order'] == '1'
     assert trade_history[0]['execution_price'] == 100
def test_cancelling_already_filled_order_returns_False():
     book = OrderBook()
     order1 = Order(
          order_id = '1',
          side = 'sell',
          price = 100,
          quantity = 10,
          cancelled = False
     )
     order2 = Order(
          order_id = '2',
          side = 'sell',
          price = 50,
          quantity = 10,
          cancelled = False
     )
     order3 = Order(
          order_id =  '3',
          side = 'buy',
          price = 150,
          quantity = 10,
          cancelled = False
     )
     book.submit_order(order1)
     book.submit_order(order2)
     book.submit_order(order3)
     trades = book.trades
     assert trades[0]['buy_order'] == '3'
     assert book.cancel_order('3') is False
def test_market_order_buys_all_and_leaves_no_resting():
    book = OrderBook()
    order1 = Order(
          order_id = '1',
          side = 'sell',
          price = 100,
          quantity = 10,
          cancelled = False
    )
    order2 = Order(
          order_id = '2',
          side = 'sell',
          price = 50,
          quantity = 10,
          cancelled = False
    )
    order3 = Order(
         order_id = '3',
         side = 'buy',
         price = None,
         quantity = 25, 
         order_type = 'market'
    )
    book.submit_order(order1)
    book.submit_order(order2)
    book.submit_order(order3)
    assert book.get_best_bid() is None
    assert book.get_best_ask() is None
def test_market_sell_consumes_highest_price_first():
     book = OrderBook(
          
     )
     order1 = Order(
          order_id = '1',
          side = 'buy',
          price = 100,
          quantity = 10
     )
     order2 = Order(
          order_id = '2',
          side = 'buy',
          price = 200,
          quantity = 5
     )
     order3 = Order(
          order_id = '3',
          side = 'sell',
          price = None,
          quantity = 10,
          order_type = 'market'
     )
     book.submit_order(order1)
     book.submit_order(order2)
     book.submit_order(order3)
     trades = book.trades
     assert trades[0]['buy_order'] == '2'
     assert len(trades) == 2
def test_empty_book_produces_nothing():
     book = OrderBook()
     order = Order(
          order_id = '1',
          side = 'buy',
          price = None,
          quantity = 100,
          order_type = 'market'
     )
     book.submit_order(order)
     assert len(book.trades) == 0
     assert len(book.bids) == 0
from order import Order
import heapq
import itertools
class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []
        self.trades = []
        self.orders = {}
        self.counter = itertools.count()
    def submit_order(self, order: Order):
        count = next(self.counter)
        if order.side == 'buy':
            while self.asks and self.asks[0][2].cancelled:
                heapq.heappop(self.asks)
            while self.asks and order.quantity >0 and (order.order_type == 'market' or order.price >= self.asks[0][0]):
                best_ask = self.asks[0][2]
                trade_volume = min(best_ask.quantity, order.quantity)
                order.quantity -= trade_volume
                best_ask.quantity -= trade_volume
                self.trades.append({'buy_order': order.order_id,
                                    'sell_order': best_ask.order_id,
                                    'trade_volume': trade_volume,
                                     'execution_price': best_ask.price
                                     })
                if best_ask.quantity ==0:
                    heapq.heappop(self.asks)
                    self.orders.pop(best_ask.order_id, None)
            if order.quantity > 0 and order.order_type == 'limit':
                heapq.heappush(self.bids, (-order.price, count, order))
                self.orders[order.order_id] = order
        elif order.side == 'sell':
            while self.bids and self.bids[0][2].cancelled:
                heapq.heappop(self.bids)
            while self.bids and order.quantity > 0 and (order.order_type == 'market' or order.price <= -self.bids[0][0]):
                best_bid = self.bids[0][2]
                trade_volume = min(best_bid.quantity, order.quantity)
                self.trades.append({'buy_order': best_bid.order_id,
                                    'sell_order': order.order_id,
                                    'trade_volume': trade_volume,
                                     'execution_price': best_bid.price
                                     })
                order.quantity -=trade_volume
                best_bid.quantity -=trade_volume
                if best_bid.quantity ==0:
                    heapq.heappop(self.bids)
                    self.orders.pop(best_bid.order_id, None)
            if order.quantity >0 and order.order_type == 'limit':
                heapq.heappush(self.asks, (order.price, count, order))
                self.orders[order.order_id] = order
        else:
            raise ValueError("Side must be 'buy' or 'sell'")
    def cancel_order(self, order_id):
        order = self.orders.get(order_id)
        if order is None:
            return False
        order.cancelled = True
        del self.orders[order_id]

    def get_best_bid(self):
        while self.bids and self.bids[0][2].cancelled:
            heapq.heappop(self.bids)
        if self.bids:
            return self.bids[0][2]
        else:
            return None
    def get_best_ask(self):
        while self.asks and self.asks[0][2].cancelled:
            heapq.heappop(self.asks)
        if self.asks:
            return self.asks[0][2]
        else:
            return None
    
    
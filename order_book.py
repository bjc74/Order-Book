from order import Order
import heapq
import itertools
from collections import deque
class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []
        self.ask_levels = {}
        self.bid_levels = {}
        self.trades = []
        self.orders = {}
        self.counter = itertools.count()
    def submit_order(self, order: Order):
        if order.side == 'buy':
            while self.asks and order.quantity >0:
                best_price = self.asks[0]
                queue = self.ask_levels[best_price]
                while queue and queue[0].cancelled:
                    queue.popleft()
                if not queue:
                    heapq.heappop(self.asks)
                    del self.ask_levels[best_price]
                    continue
                if not self.asks:
                    break
                if order.order_type == 'limit' and order.price < self.asks[0]:
                    break
                best_ask = queue[0]
                trade_volume = min(best_ask.quantity, order.quantity)
                order.quantity -= trade_volume
                best_ask.quantity -= trade_volume
                self.trades.append({'buy_order': order.order_id,
                                    'sell_order': best_ask.order_id,
                                    'trade_volume': trade_volume,
                                     'execution_price': best_ask.price
                                     })
                if best_ask.quantity == 0:
                    queue.popleft()
                    self.orders.pop(best_ask.order_id, None)
                    if not queue:
                        heapq.heappop(self.asks)
                        del self.ask_levels[best_price]
            if order.quantity > 0 and order.order_type == 'limit':
                if order.price not in self.bid_levels:
                    heapq.heappush(self.bids, (-order.price))
                    self.bid_levels[order.price] = deque()
                self.bid_levels[order.price].append(order) 
                self.orders[order.order_id] = order
        elif order.side == 'sell':
            while self.bids and order.quantity > 0:
                best_price = -self.bids[0]
                queue = self.bid_levels[best_price]
                while queue and queue[0].cancelled:
                    queue.popleft()
                if not queue:
                    heapq.heappop(self.bids)
                    del self.bid_levels[best_price]
                    continue
                if not self.bids:
                    break
                if order.order_type == 'limit' and order.price > -self.bids[0]:
                    break
                best_bid = queue[0]
                trade_volume = min(best_bid.quantity, order.quantity)
                self.trades.append({'buy_order': best_bid.order_id,
                                    'sell_order': order.order_id,
                                    'trade_volume': trade_volume,
                                     'execution_price': best_bid.price
                                     })
                order.quantity -=trade_volume
                best_bid.quantity -=trade_volume
                if best_bid.quantity == 0:
                    queue.popleft()
                    self.orders.pop(best_bid.order_id, None)
                    if not queue:
                        heapq.heappop(self.bids)
                        del self.bid_levels[best_price]
            if order.quantity >0 and order.order_type == 'limit':
                if order.price not in self.ask_levels:
                    self.ask_levels[order.price] = deque()
                    heapq.heappush(self.asks, (order.price))
                self.ask_levels[order.price].append(order)
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
        while self.bids:
            best_price = -self.bids[0]
            queue = self.bid_levels[best_price]
            while queue and queue[0].cancelled:
                queue.popleft()
            if not queue:
                heapq.heappop(self.bids)
                del self.bid_levels[best_price]
                continue
            return queue[0]
        return None
    def get_best_ask(self):
        while self.asks:
            best_price = self.asks[0]
            queue = self.ask_levels[best_price]

            while queue and queue[0].cancelled:
                queue.popleft()

            if not queue:
                heapq.heappop(self.asks)
                del self.ask_levels[best_price]
                continue

            return queue[0]

        return None
        
    
    
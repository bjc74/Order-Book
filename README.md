# Limit Order Book Matching Engine

A Python implementation of a limit order book matching engine with
price-time priority.

## Features

- Limit and market orders
- Bid and ask matching
- Price-time priority
- Partial fills
- Order cancellation
- Trade history
- Price-level order queues
- FIFO priority within each price level
- Automated tests with Pytest

## Design

The order book stores active bid and ask price levels using heaps.

Orders at each price level are stored in FIFO deques to preserve
time priority, while a hash map provides direct lookup of active
orders by order ID.

This separates:

- **price priority** — maintained by the bid/ask heaps
- **time priority** — maintained by FIFO queues within each price level
- **order lookup** — maintained by the order-ID dictionary

Cancelled orders are removed lazily when encountered during matching
or best-price queries.

## Running the tests

```bash
pytest
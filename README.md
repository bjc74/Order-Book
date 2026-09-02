# Limit Order Book Matching Engine

A Python implementation of a limit order book and matching engine using price-time priority.

## Features

- Limit and market orders
- Bid/ask matching
- Price-time priority
- FIFO execution within price levels
- Partial fills
- Order cancellation
- Order amendments
- Aggregated market depth
- Trade history
- Direct order lookup by ID
- Pytest regression coverage

## Design

The order book uses separate data structures for price priority, time priority and order lookup:

- **Price priority** — bid and ask price levels are maintained using heaps
- **Time priority** — orders at each price level are stored in FIFO `deque`s
- **Order lookup** — active orders are tracked in a hash map keyed by order ID

This allows best-price access while preserving FIFO execution between orders at the same price.

Cancelled and exhausted price levels are cleaned up lazily when encountered during matching or best-price queries.

## Matching

Incoming orders are matched against the best available opposing price.

For limit orders, matching continues while the opposing price satisfies the order's limit price.

Market orders continue matching until either:

- the order is fully filled, or
- there is no opposing liquidity remaining.

Partial fills are supported on both incoming and resting orders.

Each execution is recorded in the trade history.

## Market Depth

The order book can return aggregated depth for the bid or ask side, reporting the total resting quantity available at each price level.

## Performance

The engine was benchmarked using reproducible synthetic workloads with `random.seed(67)`.

Approximate throughput on 1,000,000 order workloads:

| Workload | Throughput |
|---|---:|
| Matching-heavy / crossing | ~1.1M order submissions/s |
| Passive / deep book | ~2.0M order submissions/s |

The matching-heavy workload generates frequent executions, while the passive workload builds a large resting book without crossing orders.

Fresh `OrderBook` and `Order` objects are created for each benchmark run, and timing begins immediately before the submission loop.

`cProfile` was used separately for profiling and not for throughput measurement because profiler overhead significantly affects timings.

## Testing

The project includes Pytest regression tests covering matching behaviour, partial fills, cancellations, amendments, depth and other core order-book operations.

Run the test suite with:

```bash
pytest
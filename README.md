# Box Packing
This is my proposed solution to the box packing problem

## Getting Started

###### Quick Start

Download the project (via clone or as a zip file), and run pack.py with no arguments. This will 'pack' the items from the included CSV file into boxes.

###### Prerequisites

- [Python 2.7.15 or higher](https://www.python.org/downloads/release/python-2715/)

## Considerations

#### How do you know your solution is not assigning too many items into a box?

I have implemented a check to ensure the used space of any given box never exceeds its capacity by volume.

#### Is it easy for you to determine how full an average box is?

Yes, at the end of the script I get the sum of the efficiencies of all boxes, then divide by the number of boxes used, giving me the average efficiency (percent of capacity utilized by volume) per box.

#### Would you rethink your solution if the items.csv file has 5 million records?

Yes, the following ideas come to mind:

###### Batch Processing

The number of items processed per batch would be determined by comparing benchmarks to the hardware of the server this service was to be ran on.

###### Full Box Removal

Whenever a box achieves 100% efficiency (all capacity by volume utilized with zero free space remaining), it would be removed from the iterable and moved to an intermediary (likely another class such as Shipment)

###### Pattern Caching

Operating under the assumption that we would often be shipping the same groupings of items (i.e. a recurring shipment of Mountain Dew), we can store the number of boxes required to ship a given amount of said items.

Along the same lines, whenever we encounter a pattern of items that provides 100% efficiency when packed, we can immediately repeat the pattern until we run out of items to satisfy the pattern, after which we would remove all packed boxes (since they achieved 100% efficiency).

#### What are other applications of a 'box packing' problem in the supply chain?

###### Inventory Optimization

A similar algorithm could be used to maximize the efficiency of warehouse usage, potentially cutting down on property costs.

###### Production 

Assuming we produce our own products in house, a variant of the box packing algorithm could be implemented to minimize raw material waste (i.e. what is the max number of cans that can be cut from this piece of raw aluminum).

###### Consumer Facing Packaging

Along the same vein as the production application, we would also likely implement some variant of this algorithm to determine the optimal way to create packaging for products we produce in house (i.e. what is smallest container we can sell 12 packs of paper towels in).

###### Shipment Optimization

Taking the algorithm a step past box packing, we can use an extended version to optimize the way the boxes are packed onto palettes / into shipping containers. We would likely also extend the algorithm to include weight distribution optimization. The exact method of distribution would depend on the way shipping costs are calculated. (My assumption would be that the most even distribution of weight would be optimal, as heavy containers are likely to pose problems, and light containers are likely below some kind of flat rate)

###### Employee Scheduling

Assuming that somewhere along the supply chain are relatively consistent tasks (i.e. how long it takes to load a shipping container from empty to full), this algorithm could be used to anticipate the labor costs of doing any given task that has an established time precedent.

###### Store Stocking

We can use this algorithm to predict how many units of any given product can fit onto the shelves of brick and mortar stores - or vice versa - how much floor space we will need to sell X units of product.

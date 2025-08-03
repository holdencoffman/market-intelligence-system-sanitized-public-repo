## Pending Model Build

This folder will house the Volume-Feasibility Link (VFL), or bridge layer, that I describe in my blueprint paper. It will be a model that simluates seasonal job flow in advance of the season in order to enable the optimization loop to pair customer volume to provider volume. Here's an excerpt from my whitepaper explaining the problem this bridge layer solves:

One of the key challenges in this optimization problem is the fundamental difference in how customer and provider interactions take place. Customer negotiations take place at an annualized level per store per trade. Provider negotiations take place daily on a job-by-job basis. This difference in granularity between the two models forms a challenging difficulty around how the two models’ outputs will be linked. We will need a bridge layer – like an adapter between the two models – that translates the output of one into terms which are consistent with the structure of the other.


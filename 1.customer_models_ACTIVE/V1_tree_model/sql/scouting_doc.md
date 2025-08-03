# Revenue Scouting Log

**Date:** 2025-06-26

## Starting Ideas to Explore

1. [Jane Doe]'s query, see if she incorporates any revenue features (probably not but you may find some useful tables here) - skip for now
2. Look in our BI reports for any reports that deal with revenue and note what tables they're pulling from
3. See if you can poke around on GitHub or anywhere else to figure out what tables other people might be pulling from...no need to reinvent the wheel, figure out what is considered the source of truth for this
   - As part of this, definitely need to get that Snowflake map from [Jane Doe] - done, doesn't exist.
   - Talk to [John Doe] as well - done.
4. Ask [John Doe] where he would pull from
   - [John Doe] helped me today and confirmed that pretty much everything I need is in the [DUMMY_TABLE]
5. Should ask [John Doe] for his [Dummy Name - Revenue Actuals Analysis] query to see what tables he's pulling from there

### Takeaway

- Main point here is you just need to start exploring and pulling threads...just cruise around, note the different tables and schemas you find, and start to build a mental map of where data is at

## Tables to Explore

- prod.DUMMY_SCHEMA.DUMMY_TABLE
- prod.DUMMY_SCHEMA.V_DUMMY_VIEW

## Schema Map (Working Draft)

- `DUMMY_SCHEMA.DUMMY_TABLE` --> Table containing accepted source of truth for revenue at the ticket level, goes back to [dummy date]
- `PROD.DUMMY_SCHEMA.V_DUMMY_VIEW` --> View that cleans DUMMY_TABLE data for sales team use, goes back to [dummy date]
- `PROD.DUMMY_SCHEMA.DUMMY_TABLE` --> Table that houses the data from the above view
- `PROD.DUMMY_SCHEMA.V_DUMMY_VIEW` --> View created by [John Doe] that arranges the above table in a consumer ready format

## Discoveries/Observations

- Ok so here's what I'm discovering. My friend [John Doe] shared a view that he created: V_DUMMY_VIEW, which draws revenue data from DUMMY_TABLE, which draws data from a view called V_DUMMY_VIEW, which draws data from the DUMMY_TABLE that Finance maintains. DUMMY_TABLE is the company accepted source of revenue data, but [John Doe] said it's really messy so sales has this DUMMY_TABLE table they use which cleans the DUMMY_TABLE data and then they analyze from there. So evidently [John Doe]'s view takes DUMMY_TABLE and performs some sort of manipulation on it to conform it for his uses. But the real magic is in whatever DUMMY_TABLE is doing to "clean" the DUMMY_TABLE data. I want to look at [John Doe]'s view real quick, then have GPT-4 explain it to me, and then we're going to jump into the actual DUMMY_TABLE table that's cleaning the DUMMY_TABLE to see what it's doing.
- Looks like the DUMMY_TABLE table only goes back to [dummy date], even though the DUMMY_TABLE goes back to [dummy date]...but our prior bid Non Routine data goes back all the way to mid [dummy year].

## Thoughts for Next Steps

Ingredients:
1. Need to flag total revenue per trade per site in a 6 month block, starting 1 month after RFP submission
2. To do so, will have to build a query that sums revenue by trade by site, and then somehow have it dynamically adjust its date window for each site on each RFP - `progress as of 6/26 work session was I uploaded all of the [dummy database ]Non Routine data into Snowflake: PROD.DUMMY_SCHEMA.DUMMY_TABLE`
3. Future state, I'll have to build my own table that goes as far back as possible, preferrably [dummy date]
   - This is going to entail studying the original logic in the [DUMMY_TABLE] transformation to understand what they're doing to clean the [DUMMY_TABLE] data, then potentially copy/pasting and adjusting the dates so it can go back at least to [dummy date]. But ideally we would want to get all the wy back to mid [dummy year]...which reaches back further than the [DUMMY_TABLE], so that will be a pretty big lift

## Plan

1. Link revenue to historical bids using [John Doe]'s data
2. Develop your own version of [DUMMY_TABLE] that goes back further than [dummy year], then use that to link revenue to historical bids
3. Eventually, explore how you could get data older than [dummy date]

## Working Notes

**2025-06-28**
- The [DUMMY_TABLE] uses our usual property ID's (you can tell if they are CRM ID's by -redacted-), but [DUMMY_TABLE] drops those in favor of the new ID's. Going to have to use `V_DUMMY_VIEW` to link prior bid IDs to [John Doe]'s table.
- `Here's what we need to do:`
  1. Use [DUMMY_TABLE] to link historical bid properties to properties in [DUMMY_TABLE]
  2. Make your window of time (6 months starting 1 month after the bid) link to ticket creation date, not revenue payment date. We're concerned with when they called us for work, not when AP sent over payment for completed work...`hmm, not sure about this. Curious though because I noticed some tickets in [John Doe]'s view that have ticket creation dates in [dummy year] and revenue dates in [dummy year] or even [dummy year]`
     - Solution to this is to use revenue date as your identifier because this is when revenue was recognized (not necessarily when it was paid, that could be later on. But this should be the period of time to which that revenue was attributed), `BUT, limit it to tickets that were created after the date the bid was submitted`
  3. There will be some challenges around linking service lines correctly...nomenclature doesn't exactly match so I'll have to make a fix for that. ⚠️ **Handoff Point:** *This will be our starting point next time*

**2025-06-30**
- Update, talked to [John Doe] today and we're going to use `V_DUMMY_VIEW`. It has all ticket data reaching back to [dummy year] so has everything I need. It also has the original property ID's in it which makes things easier.
- Okay so I got the query finished and it should be mapping total revenue per trade per store during a 6 month period beginning 1 month after the submission of a bid for that trade

**2025-07-02**

Update on V_DUMMY_VIEW
- So as it turns out, V_DUMMY_VIEW is [John Doe]'s attempt to deduplicate property IDs. Basically what he did is he went through and created a unique "deduped ID" that should be 1:1 with each property. He assigned one of these deduped IDs to each unique property in the system, and then uses things like lat/lon and confidence scores to link all our source property IDs to their corresponding deduped ID. The ultimate result is a view that serves as a master lookup...all IDs in existence for all time are listed, with their corresponding deduped ID which should be 1:1 per property. That way you can use the deduped ID as the unique identifier for a property.
- So the view has multiples of each deuped ID, but only one row for each company ID (since there are many company IDs to one deduped ID, so the deduped IDs often appear in multiple rows to link to the various company IDs for that location)

Questions/Observations on Property IDs in Snowflake
- [John Doe]'s V_DUMMY_VIEW has about [dummy number] unique properties. Total rows are [dummy number] so it seems like the overall ratio of source property IDs to actual properties is about [dummy ratio]
  - `This is true.`
- EDW.PROPERTIES has [dummy number] rows, about the same as the total amount of unique properties in V_DUMMY_VIEW. So [DUMMY_TABLE] is likely just a list of all active source property IDs, while V_DUMMY_VIEW has all source property IDs for all time [(dummy number)]
  - `This is actually not true. [DUMMY_TABLE] contains all IDs that exist within [company system]. Of these [number], [number] are marked inactive and [number] are marked deleted. So total active IDs in [company system] are [number]. [John Doe]'s V_DUMMY_VIEW estimates there to be [number] total unique properties in [company system]. So maybe, just maybe those numbers are close because of the ongoing efforts of [P&E team] to move sites to inactive or deleted that are marked as duplicates.`
- Question: the source table for V_DUMMY VIEW has [large number] rows [(DUMMY_TABLE)]. How can it have so many rows?

Working Session Actual Notes
- Completed the query today...super excited. Rewrote it to link revenue to sites based on [John Doe]'s unique deduped ID number, and also adjusted the window to a 12 month window starting immediately on the bid date (I did some investigating of a few sample bids and it seems that the date we enter in prior bid typically corresponds to the actual award date). Also I put a cutoff so no bids are examined that are not 12 months since award (don't want to underreport revenue)
- Did some analysis inside SQL on the resulting data, surprisingly found that like [dummy %] of sites marked as wins/primary did not receive any revenue for that service line in the 12 month window after award. `That may suggest that revenue data is missing here...but it may also just confirm the hypothesis that a signed rate sheet does not always or even often convert to actual revenue.`
- A decent analysis piece for the future would be to look at the primary/zero revenue trend and see if it's heavier for smaller customers than for larger ones. In other words, does the democratized store level job decision making hypothesis hold up for most large [large business pillar] type accounts? Because if so then our model's vision is actually right on track.

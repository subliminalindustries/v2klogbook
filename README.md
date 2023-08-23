# v2klogbook

A logbook parser for victims of neuroweapons.

## Format

Every day when you start logging, add a single line with the date like:

`date: 23-8-2023`

After this, add a line for each record, in the format:

`HH:MM {microwave auditory effect subjective loudness - see below}, your entry in text form`

Example:

`12:31 medium, I was making toast and felt a sharp pain in my left hand, the voices said my bread is poisoned.`

## Details for creating an entry:

### Keywords

The script tests whether the words "pain", "threat", "taunt", "paraesthesia",
or "contraction" are present in each line.

### Tinnitus score

For tinnitus, the following statements can be added to a line:
- "tinnitus start(ed)"
- "tinnitus continue(s)"
- "tinnitus increase(d)"
- "tinnitus decrease(d)"
- "tinnitus start(ed)"

This script will follow the degree of tinnitus and encode it.

### Microwave auditory effect subjective loudness

For microwave auditory effect (v2k) subjective loudness, the following
can be added after the time and before the rest of the line terminated by a comma (','):
- "low"
- "medium"
- "high"
- "extreme"


